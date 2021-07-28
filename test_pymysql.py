import pymysql
db = pymysql.connect(user="root",
                     password="2333",
                     database="sanguo",
                     charset="utf8")

cur=db.cursor()

print(cur)