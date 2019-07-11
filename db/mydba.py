
import pymysql

from DBUtils.PooledDB import PooledDB, SharedDBConnection

localpcPOOL = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
    maxshared=3,  # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    ping=0,
    # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    host='10.6.12.90',
    port=3306,
    user='root',
    password='Cr648546845',
    database='communitydetecting',
    charset='utf8'
)


class dbutil:
    def __init__(self, pool):
        self.POOL = pool

    def insertItem(self, item):
        # insert into student_info(stuName,stuAge) values('liutao',13)
        table = item["table"]
        column_list = []
        value_list = []
        s_list = []
        for k, v in item["params"].items():
            column_list.append(k)
            value_list.append(v)
            s_list.append("%s")

        sql = "insert into %s(%s) VALUES(%s)" % (table, ",".join(column_list), ",".join(s_list))
        print(sql, value_list)
        # self.exe_sql(sql, tuple(value_list))

    def getDics(self, sql, params=None):
        conn = self.POOL.connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        if params is None:
            cursor.execute(sql)
        else :
            cursor.execute(sql, params)
        result = cursor.fetchall()
        conn.close()
        return result

    def getTuples(self, sql, params=None):
        conn = self.POOL.connection()
        cursor = conn.cursor()
        if params is None:
            cursor.execute(sql)
        else :
            cursor.execute(sql, params)
        result = cursor.fetchall()
        conn.close()
        return result

    def exe_sql(self, sql, params=None):
        conn = self.POOL.connection()
        cursor = conn.cursor()
        if params is None:
            r = cursor.execute(sql)
        else:
            r = cursor.execute(sql, params)
        conn.commit()
        conn.close()
        return r

    def exe_many(self, sql, li=None):
        conn = self.POOL.connection()
        cursor = conn.cursor()
        if li is None:
            r = cursor.execute(sql)
        else:
            r = cursor.executemany(sql, li)
        conn.commit()
        conn.close()
        return r


db_localpc = dbutil(localpcPOOL)

