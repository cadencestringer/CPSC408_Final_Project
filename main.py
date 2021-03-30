import generateData
import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password:
    database = "Cookies"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW TABLES;")
tablesData = pd.DataFrame(mycursor.fetchall())
tables = []

for i in range(len(tablesData)):
    tables.append(tablesData[0][i])

print(tables)


def printTable(tableName):
    mycursor.execute("SELECT * FROM %s;", (tableName,))
    data = mycursor.fetchall()
    df = pd.DataFrame(data)
    print(df)

def addNewRecord(tableName):
    print(1)
