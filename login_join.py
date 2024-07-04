import bcrypt #pip install bcrypt
import re #정규화식
import oracledb as db 

class login:
    def join(id ,pw, name): # 회원가입
        bytes_pw = pw.encode('utf-8')
        bytes_salt = bcrypt.gensalt() # 무작위 솔트 생성
        bytes_hashed_pw = bcrypt.hashpw(bytes_pw, bytes_salt) # 비밀번호 해싱
        
        pattern = r'^[가-힣]{2,4}$'
        
        if re.match(pattern, name): # 이름이 한글이고, 2자 ~ 4자 일때
            try:
                con=db.connect(dsn='127.0.0.1:1521/xe',user='C##STOCK',password='1234')
                cursor=con.cursor()
                
                cursor.execute("select * from login")
                log_data = cursor.fetchall()
                for i in log_data: # 중복 방지
                    if i[2]==id:
                        cursor.close()
                        con.close()
                        return 'fail_1' #아이디가 중복됩니다.
  
                cursor.execute("insert into login values(:hashed_pw, :salt, :id, :name)", hashed_pw=bytes_hashed_pw, salt=bytes_salt, id=id, name=name)
       
            except db.DatabaseError as e:
                print(e)
            con.commit()
            cursor.close()
            con.close()
            return 'success' # 정상적인 회원가입
        else:
            return 'fail_2' # 이름이 정규식에 해당 안 될때.

    def log(id, pw): # 로그인
        bytes_pw = pw.encode('utf-8')
        
        try:
            con=db.connect(dsn='127.0.0.1:1521/xe',user='C##STOCK',password='1234')
            cursor=con.cursor()
            cursor.execute(f"SELECT hashed_pw, salt, id FROM LOGIN where ID = '{id}'")
            log_data = cursor.fetchall()
            
            for i in log_data:
                bytes_DB_salt = i[1].read()
                hashed_pw = bcrypt.hashpw(bytes_pw, bytes_DB_salt) # 현재 로그인 한 해싱
                bytes_DB_hashed = i[0].read() # DB에 저장된 해싱
                
                if bytes_DB_hashed == hashed_pw and i[2] == id:
                    con.commit()
                    cursor.close()
                    con.close()
                    return True #로그인 되었습니다.
        
        except db.DatabaseError as e:
            print(e)
        con.commit()
        cursor.close()
        con.close()
        return False # 로그인이 실패되었습니다.
