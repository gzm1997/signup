import mysql.connector


"""
conn = mysql.connector.connect(user='root', password='Gzm20125', database='ikdeer_user')
"""



class sql_manager(object):
    """docstring for sql_manager"""
    def __init__(self, account, password):
        self._conn = mysql.connector.connect(user = account, password = password, database = "ikdeer_user")
    
    def _clear(self):
        cursor = self._conn.cursor()
        cursor.execute("delete from user;")
        cursor.execute("delete from raw_user;")
        self._conn.commit()
        cursor.close()        

    def _search_r_user(self, email = "", username = "", vertifycode = ""):
        cursor = self._conn.cursor(dictionary = True)
    
        sql_word = "select * from raw_user where "
        variables = []

        if email != "":
            sql_word = sql_word + "email = %s "
            variables.append(email)

        if username != "" and sql_word.find("email") == -1:
            sql_word = sql_word + "username = %s "
            variables.append(username)
        elif username != "" and sql_word.find("email") != -1:
            sql_word = sql_word + "and username = %s "
            variables.append(username)
            
        if vertifycode != "" and sql_word.find("email") == -1 and sql_word.find("username") == -1:
            sql_word = sql_word + "vertifycode = %s"
            variables.append(vertifycode)
        elif vertifycode != "" and (sql_word.find("email") != -1 or sql_word.find("username") != -1):
            sql_word = sql_word + "and vertifycode = %s"
            variables.append(vertifycode)            

        sql_word = sql_word + ";"
        cursor.execute(sql_word, variables)

        result = cursor.fetchall()
        self._conn.commit()
        cursor.close()
        if len(result):
            return result[0]
        else:
            return {}


    def _search_user(self, email = "", username = ""):
        cursor = self._conn.cursor(dictionary = True)
    
        sql_word = "select * from user where "
        variables = []

        if email != "":
            sql_word = sql_word + "email = %s "
            variables.append(email)

        if username != "" and sql_word.find("email") == -1:
            sql_word = sql_word + "username = %s "
            variables.append(username)
        elif username != "" and sql_word.find("email") != -1:
            sql_word = sql_word + "and username = %s "
            variables.append(username)        

        sql_word = sql_word + ";"
        cursor.execute(sql_word, variables)

        result = cursor.fetchall()
        self._conn.commit()
        cursor.close()
        if len(result):
            return result[0]
        else:
            return {}
    #0表示添加成功，1表示emai已被用添加失败，2表示username被用添加失败, 3表示邮箱已注册但未认证
    def _insert_r_user(self, email, username, password, vertifycode):
        if self._search_r_user(email = email) != {}:
            self._delete_r_user(email = email)
        if self._search_user(username = username) != {}:
            return 2
        if self._search_user(email = email) != {}:
            return 1
        cursor = self._conn.cursor()
        cursor.execute("insert into raw_user value(%s, %s, %s, %s)", [email, username, password, vertifycode])
        self._conn.commit()
        cursor.close()
        return 0

    def _delete_r_user(self, email):
        cursor = self._conn.cursor()
        cursor.execute("delete from raw_user where email = %s", [email])
        self._conn.commit()
        cursor.close()        
    
    #返回False表示添加失败，否则成功
    def _insert_user(self, email, username, password):
        if self._search_r_user(email = email, username = username) == {}:
            return False
        cursor = self._conn.cursor()
        self._delete_r_user(email)
        cursor.execute("insert into user value(%s, %s, %s)", [email, username, password])
        self._conn.commit()
        cursor.close()    
        return True




if __name__ == "__main__":
    m = sql_manager("root", "Gzm20125")

    print("user", m._search_user(username = "gzm1997"))
    print("user", m._search_user(email = "16178923429@qq.com"))

    print("raw_user", m._search_r_user(username = "gzm1997", vertifycode = "Gzm20125"))

    print("raw_user", m._search_r_user(username = "gzm1997", vertifycode = "123"))
    print("insert")

    print(m._insert_r_user("1762@qq.com", "asd", "dsa", "43311"))

    print("insert user")
    print(m._insert_user("1762@qq.com", "asd", "dsa"))