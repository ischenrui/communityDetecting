from db.mydba import db_localpc


class adminService:

    def get_web_log(self, params):
        sql = "SELECT * FROM web_log LIMIT %s, %s" % ((params['curPage']-1)*params['pageSize'], params['pageSize'])
        data = db_localpc.getDics(sql)
        res_data = []
        index = 1
        for i in data:
            i['time'] = str(i['time'])
            i['index'] = index
            index += 1
            res_data.append(i)

        sql_2 = "SELECT COUNT(*) AS total FROM web_log"
        length = db_localpc.getDics(sql_2)

        result = dict()
        result["total"] = length[0]['total']
        result["data"] = res_data
        return result

    def get_accounts(self, params):
        sql = "SELECT * FROM account ORDER BY create_time DESC LIMIT %s, %s" % ((params['curPage']-1)*params['pageSize'], params['pageSize'])
        data = db_localpc.getDics(sql)
        res_data = []
        index = 1
        for i in data:
            i['create_time'] = str(i['create_time']) if i['create_time'] else None
            i['modify_time'] = str(i['modify_time']) if i['modify_time'] else None
            i['index'] = index
            index += 1
            res_data.append(i)
        sql_2 = "SELECT COUNT(*) AS total FROM account"
        length = db_localpc.getDics(sql_2)

        result = dict()
        result["total"] = length[0]['total']
        result["data"] = res_data

        return result

    def delete_account(self, params):
        sql = "DELETE FROM account WHERE id=%s"
        result = db_localpc.exe_sql(sql, params)
        # result = 1
        print(sql, params)
        return result

    def update_account(self, params):
        sql = "UPDATE account SET name=%s, psd=%s, status=%s, modify_time=NOW() WHERE id=%s"
        print(sql, params)
        result = db_localpc.exe_sql(sql, params)
        return result

    def get_latest_accounts(self, param):
        sql = "SELECT * FROM account WHERE create_account=%s ORDER BY create_time DESC LIMIT 10"
        data = db_localpc.getDics(sql, param)
        res_data = []
        index = 1
        for i in data:
            i['create_time'] = str(i['create_time']) if i['create_time'] else None
            i['modify_time'] = str(i['modify_time']) if i['modify_time'] else None
            i['index'] = index
            index += 1
            res_data.append(i)
        return res_data

    def insert_account(self, params):
        sql = "INSERT INTO account(id, name, psd, status, create_time, create_account) VALUES(%s,%s,%s,%s,now(),%s)"
        try:
            re = db_localpc.exe_sql(sql, params)
        except Exception as e:
            re = e.args[0]

        return re


admin_service = adminService()
