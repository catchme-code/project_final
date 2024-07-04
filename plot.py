import FinanceDataReader as fdr
from datetime import datetime,timedelta
import oracledb as db

class real_plot:
    def data(name):
        try:
            con = db.connect(dsn="127.0.0.1:1521/xe", user="C##STOCK", password="1234")
            cursor = con.cursor() 
            
            cursor.execute(f"select code from stock where id = '{name}'")
            stock_data = cursor.fetchall()
            code = stock_data[0][0]
        
            con.commit
            cursor.close
            con.close
        except db.DatabaseError as e:
            print(e) 
                        
        reality=datetime.now()#현재날짜
        now=datetime.now()-timedelta(days=30)# 현재날짜 - 30일 
        
        R=reality.strftime('%Y-%m-%d')# 날짜 형식 변환
        
        N=now.strftime('%Y-%m-%d')
        
        GS = fdr.DataReader(code,N,R)#(종목코드,시작날짜,끝날짜)
        
        x=GS.index
        y=GS['Close']
        
       
        del GS['Change']
        
        return x,y,GS
    