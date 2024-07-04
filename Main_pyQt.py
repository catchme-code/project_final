import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap # 이미지
import oracledb as db # 오라클 데이터베이스

from DB_adjust_table import ad_table
import DB_stock
from login_join import login
from stock_plot import graf
from plot import real_plot

class MainWindow(QMainWindow):  
    def __init__(self):
        super(MainWindow, self).__init__()
        # .ui 파일의 경로를 지정
        main_file_path = os.path.join(os.path.dirname(__file__), './ui/main_page.ui')
        loadUi(main_file_path, self)
        
        try:
            con = db.connect(dsn="127.0.0.1:1521/xe", user="C##STOCK", password="1234")
            cursor = con.cursor() # DB상호작용 메소드
            
            cursor.execute("SELECT ID FROM STOCK")
            data_stock = cursor.fetchall()
            
            for i in data_stock:
                self.list_stock.addItem(QListWidgetItem(i[0])) # 변수를 listWidget에 적재
       
        except db.DatabaseError as e:
            print(e)
        con.commit()
        cursor.close()
        con.close()
        
        pixmap = QPixmap('./img/stock_img.png')
        self.label_stock_img.setPixmap(pixmap)
         
        self.list_stock.itemClicked.connect(self.ch_label) # listWidget의 항목을 클릭하였을때
        self.butt_select.clicked.connect(self.select_stock) # butt_select를 클릭 했을 때
        self.butt_insert.clicked.connect(self.insert_stock) 
        self.butt_delete.clicked.connect(self.delete_stock) 
        self.butt_reset.clicked.connect(self.reset_stock) 
        
    def ch_label(self, item): #리스트를 클릭했을때
        selected_text = item.text() #클릭한 item의 text를 selected_text에 저장
        self.label.setText(f"{selected_text}") # label을 f"Selected item: {selected_text}"로 변환
        
    def select_stock(self): # 2번째 창으로 이동.
        stock_name = self.label.text()
        if stock_name != '선택명':
            self.second = insert_page(stock_name) # self.second라는 이름에 insert_page() 클라스 호출 등록
            self.second.show()
            
            
        else:
            QMessageBox.about(self, "Error", "종목을 선택해 주세요.")
            
    def alert_wait(self):
        alert = QMessageBox(self)
        alert.setWindowTitle("wait")
    
        return alert
        
    def reset_stock(self): # reset
        self.hide()
        alert = self.alert_wait()
        alert.show()
        DB_stock.ext()
        self.list_stock.clear()
        try:
            con = db.connect(dsn="127.0.0.1:1521/xe", user="C##STOCK", password="1234")
            cursor = con.cursor() # DB상호작용 메소드
            
            cursor.execute("SELECT ID FROM STOCK")
            data_stock = cursor.fetchall()
            
            for i in data_stock:
                self.list_stock.addItem(QListWidgetItem(i[0])) # 변수를 listWidget에 적재
        except db.DatabaseError as e:
            print(e)
        alert.close()
        self.show()
        QMessageBox.about(self, "Success", "리스트 갱신에 성공했습니다.") # alert창 [메세지 title], [내용]
        con.commit()
        cursor.close()
        con.close()

    def insert_stock(self): # insert
        self.hide()
        alert = self.alert_wait()
        alert.show()
        stock_name = self.input_stock.text() #input_stock에 입력한 데이터 가져옴 type=str

        # 주식 종목 추가
        self.create_table = ad_table.create_table(stock_name) # 1년전 데이터가 없으면 None 값 적재완료되면 'complete' 
        if self.create_table is None:
            QMessageBox.about(self, "Error", "해당하는 주식 종목이 없습니다.") # alert창 [메세지 title], [내용]
            alert.close()
            self.show()
        elif self.create_table == 'not_data':
            QMessageBox.about(self, "Error", "주식 정보가 많지않아 예측하기 어렵습니다.")
            alert.close()
            self.show()
        elif self.create_table == 'equ':
            QMessageBox.about(self, "Error", "중복된 주식 종목이 존재합니다.")
            alert.close()
            self.show()
        else:
            self.list_stock.clear()
            try:
                con = db.connect(dsn="127.0.0.1:1521/xe", user="C##STOCK", password="1234")
                cursor = con.cursor() # DB상호작용 메소드
                
                cursor.execute("SELECT ID FROM STOCK")
                data_stock = cursor.fetchall()
                
                for i in data_stock:
                    self.list_stock.addItem(QListWidgetItem(i[0])) # 변수를 listWidget에 적재
            except db.DatabaseError as e:
                print(e)
            alert.close()
            self.show()
            QMessageBox.about(self, "Success", "종목이 추가되었습니다.")
            con.commit()
            cursor.close()
            con.close()

    def delete_stock(self):
        self.hide()
        alert = self.alert_wait()
        alert.show()
        stock_name = self.input_stock.text() #input_stock에 입력한 데이터 가져옴 type=str
        
        # 주식 종목 제거
        delete_table = ad_table.delete_table(stock_name) 
        if delete_table is None:
            QMessageBox.about(self, "Error", "해당하는 주식 종목이 없습니다.") # alert창 [메세지 title], [내용]
            alert.close()
            self.show()
        elif delete_table == 'not_data':
            QMessageBox.about(self, "Error", "존재하는 테이블이 없습니다.")
            alert.close()
            self.show()
        else:
            self.list_stock.clear()
            try:
                con = db.connect(dsn="127.0.0.1:1521/xe", user="C##STOCK", password="1234")
                cursor = con.cursor() # DB상호작용 메소드
                
                cursor.execute("SELECT ID FROM STOCK")
                data_stock = cursor.fetchall()
                
                for i in data_stock:
                    self.list_stock.addItem(QListWidgetItem(i[0])) # 변수를 listWidget에 적재
            except db.DatabaseError as e:
                print(e)
            alert.close()
            self.show()
            QMessageBox.about(self, "Success", "삭제 되었습니다.")
            con.commit()
            cursor.close()
            con.close()
         
class insert_page(QWidget): 
    def __init__(self, stock_name):
        super(insert_page, self).__init__()
        insert_file_path = os.path.join(os.path.dirname(__file__), './ui/insert_page.ui')
        loadUi(insert_file_path, self)
 
        self.butt_predict.clicked.connect(self.predict_stock) 
        x,y,veiw=real_plot.data(stock_name)
        self.plot(x, y)
        start, end = self.tree(veiw)
        self.label_stock_name.setText(f"{stock_name}")
        self.label_stock_start.setText(f"{start}")
        self.label_stock_end.setText(f"{end}")

    def plot(self, x, y):
        self.graphWidget.plot(x,y)
        self.graphWidget.getPlotItem().showAxis('bottom', show=False)
        
    def predict_stock(self):
        stock_name = self.label_stock_name.text()
        ch = graf.create_plot(stock_name)
        if ch == False:
            QMessageBox.about(self, "Error", "주식장이 열리지 않았습니다.")
    def tree(self,da):
        end = ''; start=''; cnt=1
        for j in range(len(da['Open'].index)):
            li = []
            li.append(str(da.index.values[j])[:10])
            end = str(da.index.values[j])[:10]
            if cnt == 1:
                start = str(da.index.values[j])[:10]
                cnt +=1
            for i in da:
                li.append(str(da[i][j]))
            item = QTreeWidgetItem(self.treeWidget,li)
        return start, end

class login_page(QMainWindow):
    def __init__(self):
        super(login_page, self).__init__()
        login_file_path = os.path.join(os.path.dirname(__file__), './ui/login.ui')
        loadUi(login_file_path, self)
        self.setFixedSize(851, 551)
        pixmap = QPixmap('./img/login.png')
        self.label.setPixmap(pixmap)
        self.input_pw.setEchoMode(QLineEdit.Password)
        
        self.butt_login.clicked.connect(self.login_click) # butt_select를 클릭 했을 때
        self.butt_join.clicked.connect(self.join_click)
    
    def login_click(self):
        id = self.input_id.text().upper()
        pw = self.input_pw.text()

        result = login.log(id, pw)
        
        if result == True:
            self.hide()
            self.window = MainWindow()
            self.window.show() # GUI를 보여준다.
        else:
            QMessageBox.about(self, "Error", "id, pw가 맞지 않습니다.")
            
    def join_click(self):
        self.hide()
        self.join_window = join_page()
        self.join_window.show()
        
class join_page(QWidget):
    def __init__(self):
        super(join_page, self).__init__()
        join_file_path = os.path.join(os.path.dirname(__file__), './ui/join.ui')
        loadUi(join_file_path, self)
        self.setFixedSize(851, 551)
        pixmap = QPixmap('./img/join.png')
        self.label.setPixmap(pixmap)
        self.input2_pw.setEchoMode(QLineEdit.Password)
        
        self.butt_login.clicked.connect(self.login_click) # butt_select를 클릭 했을 때
        self.butt_join.clicked.connect(self.join_click)
        
    def join_click(self):
        name = self.input2_name.text()
        id = self.input2_id.text().upper()
        pw = self.input2_pw.text()
        
        result = login.join(id, pw, name)
        if result == 'fail_1':
            QMessageBox.about(self, "Error", "중복된 ID가 존재합니다.")
        elif result == 'fail_2':
            QMessageBox.about(self, "Error", "이름은 한글로 2~4자 써주세요.")
        else:
            QMessageBox.about(self, "Success", "회원가입이 완료되었습니다.")
            
            self.login_window = login_page()
            self.login_window.show()
            self.hide()
            
    def login_click(self):
        self.login_window = login_page()
        self.login_window.show()
        self.hide()

def window():
    # 현재 파일의 경로로 작업 디렉토리를 변경
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = QApplication(sys.argv)
    login_window = login_page()
    login_window.show()
    
    
    sys.exit(app.exec_())
