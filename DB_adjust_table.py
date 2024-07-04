from selenium import webdriver as web
from selenium.webdriver.chrome.options import Options # 크롬의 옵션기능 import
from selenium.webdriver.common.by import By # By=Class를 위해 명시
from selenium.common.exceptions import NoSuchElementException #Element 의 값이 없을때
import FinanceDataReader as fdr # pip install finance-datareader 주식정보 라이브러리
import oracledb as db # 오라클 데이터베이스

class ad_table:
    def adjust_code(name): # 주식종목을 code로 변환
        op = Options()
        op.add_argument('--headless') #브라우저가 뜨지 않고 실행됩니다.
        
        driver = web.Chrome(options=op) #웹 브라우저 가져오기
        driver.get("http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201") #메일경제 한국 주식 인기 검색 코스피
        driver.implicitly_wait(3) # 묵시적 기다림
    
        driver.find_element(By.XPATH, '//*[@id="jsTotSch"]').send_keys(name)
        driver.find_element(By.XPATH, '//*[@id="jsTotSchBtn"]').click()
        
        try: # 검색 할 Element가 없을때 종료
            code = driver.find_element(By.XPATH, '//*[@id="isuInfoTitle"]/label').text[-7:-1] # 코드 출력
        except NoSuchElementException as e:
            code = None
        
        return code

    def create_table(name): # table 생성
        code = ad_table.adjust_code(name)
        if code is None:
            return None        
        
        try: # 2024 1월 데이터 여부
                sto_data = fdr.DataReader(code,'2024-01-01','2024-01-05')
                sto_data['Open'].iloc[0]
                
                try:
                    con = db.connect(dsn="127.0.0.1:1521/xe", user="C##STOCK", password="1234")
                    cursor = con.cursor() # DB상호작용 메소드
                    
                    cursor.execute("SELECT ID FROM STOCK")
                    data = cursor.fetchall()
                    for i in data:
                        if i[0] == name:
                            return 'equ'
                    cursor.execute("INSERT INTO STOCK VALUES(:NAME, :CODE)", NAME=name, CODE=code)
                    
                    con.commit()
                    cursor.close()
                    con.close()
                    
                    return 'complete'
                        
                except db.DatabaseError as e:
                    con.commit()
                    cursor.close()
                    con.close()
                    return 'equ' #db error가 테이블 중복
                    
        except IndexError as e:
            return 'not_data' # 2024년 데이터가 없을 시
        
    
    def delete_table(name): # table 삭제
        code = ad_table.adjust_code(name)
        if code is None:
            return None 
        
        try:
            con = db.connect(dsn="127.0.0.1:1521/xe", user="C##STOCK", password="1234")
            cursor = con.cursor() # DB상호작용 메소드

            cursor.execute("DELETE FROM STOCK WHERE ID = :NAME", NAME=name)
            
        except db.DatabaseError as e:
            con.commit()
            cursor.close()
            con.close()
            return 'not_data'
        
        con.commit()
        cursor.close()
        con.close()
        return 'complete'