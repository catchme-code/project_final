import FinanceDataReader as fdr # pip install finance-datareader 설치 
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet     #pip install prophet 설치 
from datetime import datetime
import oracledb as db 

class graf:
    def create_plot(name):
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
                
        now=datetime.now()# 현재날짜
        time=now.strftime('%H-%M')# 현재 날짜 형식변환
        if time >='09-00' and time<='18-00': 

            GS = fdr.DataReader(code,'2024-01-01',now.strftime('%Y-%m-%d'))#20240101~현재 데이터 가져오기
            df = pd.DataFrame({'ds':GS.index,'y':GS['Close']})
            Day=now.strftime('%Y-%m-%d')
            Today=df.index.get_loc(Day)
            weekday = now.weekday()
        
            m = Prophet()#예측값 구현 알고리즘
            m.fit(df)
            
            future = m.make_future_dataframe(periods=6,freq='ME',include_history='False')
                                                        #ㄴ개월(ME[month end])
            forecast = m.predict(future)
            
            fig = plt.figure(figsize=(12, 6))
            ax = fig.add_subplot(311) #그래프 칸 나누기 (행,열,순서)
            ax.plot(forecast['ds'][Today:], forecast['yhat'][Today:], label='pred(6Mouth)', color='red', linewidth=5.0)#(x축,y축,제목 )
            ax.set_title("6Mouth")#제목
            ax.set_xlabel('Date')#x축제목
            ax.set_ylabel('stock price')#y축제목
            ax.legend()
            
            for i in range(0,5):
                if weekday==i:
                    future = m.make_future_dataframe(periods=5-i,freq='d',include_history='False')#5일 예측
                if weekday==5 or weekday==6:                    #  ㄴ일(day)     
                    return False # 주말에 어플을 켰을 때
            forecast = m.predict(future)
            
            ax = fig.add_subplot(313)#그래프 칸 나누기  행,열,순서)
            ax.plot(forecast['ds'][Today:], forecast['yhat'][Today:], label='pred(weekday)', color='red', linewidth=5.0)#(x축,y축,제목 )
            ax.set_title("weekday")#제목
            ax.set_xlabel('Date')#x축제목
            ax.set_ylabel('stock price')#y축제목
            ax.legend()

            plt.show()
            return fig
        else:
            return False # 9시 이전, 6시 이후에 어플을 켰을 때
        
        