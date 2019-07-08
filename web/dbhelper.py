import pymysql.cursors
from config import DBConfig

class DBhelper(object):
    # 数据库连接配置
    def __init__(self, user, password, database, host='127.0.0.1', port=3306, **kw):
        self.connect = pymysql.connect(
            host = host,  # 数据库地址
            port = port,  # 数据库端口
            db = database,  # 数据库名
            user = user,  # 数据库用户名
            passwd = password,  # 数据库密码
        )
        self.cursor = self.connect.cursor()
        # 通过cursor执行增删查改
        # cursor = connect.cursor()
    
    def execute(self,sql,errorMsg="has error"):
        try:
            # 执行 sql 语句
            self.cursor.execute(sql)

            """
                data type : ((a1,b1,..),(a2,...),...)
            """
            data = self.cursor.fetchall()

            # 提交 sql 语句
            self.connect.commit()
            
            return data

        except Exception as e:
            print(errorMsg,e)
            return False

DBConnecter = DBhelper(**DBConfig)

if __name__ == '__main__':
    print(DBConnecter.execute("select * from es_institution limit 10"))