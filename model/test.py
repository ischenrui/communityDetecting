from db.mydba import db_crpc,db_eds_base,db_localpc

sql = 'select * from es_teacher limit 10;'
for node in db_localpc.getDics(sql):
    print(node)