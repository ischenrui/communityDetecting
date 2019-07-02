import pymysql.cursors
from spider.baiduxueshu.baiduxueshu.settings import DB_SETTING
from spider.baiduxueshu.baiduxueshu.settings import CRAWL_SETTING
from spider.baiduxueshu.baiduxueshu.settings import ENGLISH_PAPER,name
import random
import uuid
# 连接数据库
class DB(object):
    connectdic={
        # "aliyun": pymysql.Connect(
        #     host='47.104.236.183',
        #     port=3306,
        #     user='root',
        #     password='SLX..eds123',
        #     db='communitydetecting',
        #     charset='utf8'
        # ),
        # "LiWei": pymysql.Connect(
        #     host='10.6.11.44',
        #     port=3306,
        #     user='root',
        #     password='1111',
        #     db='englishpaper',
        #     charset='utf8'
        # ),
        # "feng3": pymysql.Connect(
        #     host='10.6.11.40',
        #     port=3306,
        #     user='root',
        #     password='zdf.0126',
        #     db='eds',
        #     charset='utf8'
        # ),
        "chen": pymysql.Connect(
            host='10.6.12.90',
            port=3306,
            user='root',
            password='Cr648546845',
            db='communitydetecting',
            charset='utf8'
        ),
    }
    def __init__(self,name):
        self.connect=self.connectdic[name]
        self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)

    # 插入论文
    def InsertPaper(self, item):
        sql = "INSERT INTO eds_paper VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        params = (str(uuid.uuid1()),
            item['name'], item['url'], item['abstract'], item['org'], item['year'], item['cited_num'],
            item['source'],
            item['source_url'], item['keyword'], item['author'], item['author_id'], item['cited_url'],
            item['reference_url'], item['paper_md5'])
        self.cursor.execute(sql, params)
        self.connect.commit()


    def getDics(self, sql, params=None):
        cursor = self.cursor
        if params is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, params)
        result = cursor.fetchall()
        return result

    def exe_sql(self, sql, params=None):
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, params)
        self.connect.commit()

