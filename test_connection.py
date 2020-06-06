import psycopg2
from psycopg2 import sql
from config import *


connection = psycopg2.connect(dbname=POSTGRES_DBNAME,
                              user=POSTGRES_USER,
                              host=POSTGRES_HOST,
                              password=POSTGRES_PASSWORD)

cursor = connection.cursor()
cursor.execute(sql.SQL("select * from users;"))

mobile_records = cursor.fetchall()

for i in mobile_records:
    print(i[0], i[1], i[2])


connection.commit()
cursor.close()
connection.close()
