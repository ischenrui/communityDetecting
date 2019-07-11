from db.mydba import db_localpc


class userService:

    def get_user(self, params):
        sql = "SELECT * FROM account WHERE id=%s"
        data = db_localpc.getDics(sql, params)
        if not data:
            return {}
        return data[0]


user_service = userService()
