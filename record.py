from flask import request, session, json
import time


from db.mydba import db_localpc


class Record:
    def __init__(self):
        self.map = {
            "login": self.login,
            "admin": self.admin,
            "add": self.add,
            "logging": self.logging,
        }
        self.catalog = {

            "admin": {"add": "用户管理-添加账号页面", "accounts": "用户管理-查看所有账号",
                      "setting-spider": "爬虫管理-爬虫参数设置页面", "data": "爬虫管理-查看爬取日志",
                      "logging": "日志管理-查看用户日志"},
            "login": {"check": "用户登陆-登陆检查", "logout": "退出登录"},
            "logging": {"getdata": "日志管理-查看用户日志-日志列表"},
            "add": {"insert": "添加账号-插入数据", "data": "添加账号-查看10项最近添加数据"},
        }

    def login(self, lis, response):
        print(lis)
        if lis:
            item = self.getItem(response)
            item["description"] = "用户登陆页面"
            if len(lis) > 1 and lis[1] in self.catalog[lis[0]]:
                item["description"] = self.catalog[lis[0]][lis[1]]

            records = {"table": "web_log", "params": item}
            db_localpc.insertItem(records)
        pass

    def add(self, lis, response):
        if len(lis) > 1 and lis[1] in self.catalog[lis[0]].keys():
            item = self.getItem(response)
            item["description"] = self.catalog[lis[0]][lis[1]]

            records = {"table": "web_log", "params": item}
            db_localpc.insertItem(records)
        pass

    def logging(self, lis, response):
        if len(lis) > 1 and lis[1] in self.catalog[lis[0]].keys():
            item = self.getItem(response)
            item["description"] = self.catalog[lis[0]][lis[1]]

            records = {"table": "web_log", "params": item}
            db_localpc.insertItem(records)
        pass

    def admin(self, lis, response):
        if lis:
            item = self.getItem(response)
            item["description"] = "用户管理"
            if len(lis) > 1 and lis[1] in self.catalog[lis[0]]:
                item["description"] = self.catalog[lis[0]][lis[1]]

            records = {"table": "web_log", "params": item}
            db_localpc.insertItem(records)

    def getCatalog(self):
        url = request.url.replace(request.url_root, "")
        index = url.find('?')
        if index >= 0:
            return url[:index].split("/")
        else:
            return url.split("/")

    def getData(self, response):
        res = dict()
        res["status_code"] = response._status_code
        res["type"] = "html"
        try:
            temp = response.response[0]
            if temp:
                try:
                    res["resp"] = json.loads(str(temp, encoding='utf8'))
                    res["type"] = "dict"
                    return res
                except Exception as e:
                    print(e)
                    return res
        except Exception as e:
            print(e)
            return res
        return res

    def getItem(self, response):

        data = self.getData(response)

        item = dict()
        item["ip"] = request.remote_addr
        dic = dict()
        for k in request.form:
            dic[k] = request.form[k]
        item["form"] = str(dic)
        item["url"] = request.url
        item["status"] = str(data["status_code"])
        item["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if 'username' in session:
            item["user"] = session['account']
        else:
            item["user"] = "NULL"
        if data["type"] == "dict":
            item["info"] = data["resp"]["msg"]
        return item


r = Record()

