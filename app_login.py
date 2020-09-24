from MySQLdb import _mysql

conn = _mysql.connect(db='selvaprakash$default', user='selvaprakash', host='selvaprakash.mysql.pythonanywhere-services.com', passwd='selvamysql1')


conn.query("select * from users")

res = conn.store_result()

for row in  (res.fetch_row(maxrows=0)):
    if (row[1].decode("utf-8") )=='admin':
        print (row[2].decode("utf-8") )


