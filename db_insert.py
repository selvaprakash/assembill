import MySQLdb
import pandas as pd

db = MySQLdb.connect("selvaprakash.mysql.pythonanywhere-services.com","selvaprakash","selmysql1","selvaprakash$BILLD" )
cursor = db.cursor()
sql = """INSERT INTO BILL_DETAILS(
         ITEM_NAME, QTY, PRICE, AMOUNT)
         VALUES ('OIL', '1', 20, 20)"""
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

# disconnect from server