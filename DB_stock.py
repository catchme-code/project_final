from selenium import webdriver as web
from selenium.webdriver.chrome.options import Options # 크롬의 옵션기능 import
from selenium.webdriver.common.by import By # By=Class를 위해 명시
import FinanceDataReader as fdr # pip install finance-datareader 주식정보 라이브러리, pip install plotly
from selenium.common.exceptions import NoSuchElementException #Element 의 값이 없을때

import oracledb as db # 오라클 데이터베이스

class ext:
    def __init__(self): 
        op = Options()
        op.add_argument('--headless') #브라우저가 뜨지 않고 실행됩니다.
        
        driver = web.Chrome(options=op) #웹 브라우저 가져오기
        driver.get("https://stock.mk.co.kr/domestic/popular?type=kospi") #메일경제 한국 주식 인기 검색 코스피
        driver.implicitly_wait(3) # 묵시적 기다림
        
        try:
            con = db.connect(dsn="127.0.0.1:1521/xe", user="C##STOCK", password="1234")
            cursor = con.cursor() # DB상호작용 메소드

            cursor.execute("truncate table stock")
            cnt = 1; data_cnt = 0   
            
            while data_cnt != 15:
                try: # 검색 할 Element가 없을때 종료
                    code = driver.find_element(By.XPATH, '//*[@id="kospi"]/section/table/tbody/tr['+str(cnt)+']/td[2]/span/a').text
                except NoSuchElementException as e:
                    break
                
                try: # 2024년 1월 데이터가 없을때 재 검색
                    sto_data = fdr.DataReader(code,'2024-01-02','2024-01-05')
                    sto_data['Open'].iloc[0]
                    id = driver.find_element(By.XPATH, '//*[@id="kospi"]/section/table/tbody/tr['+str(cnt)+']/td[3]/span/a').text
                    
                    cursor.execute("Insert into stock values(:data1, :data2)", data1=id, data2=code)
                    data_cnt += 1; cnt+=1
                except IndexError as e:
                    cnt+=1
                    
        except db.DatabaseError as e:
            print(e)
            
        print('데이터베이스 적재 완료')
        con.commit()
        cursor.close()
        con.close()