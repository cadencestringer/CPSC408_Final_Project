import mysql.connector
from faker import Faker
import csv
import datetime
import pandas as pd
from datetime import timedelta
from datetime import datetime

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="Meadow18!",
#     database = "Cookies"
# )

db = mysql.connector.connect(
    host="35.235.87.251", # updated
    user="myappuser",
    password="gloopybloopy",
    database="Students"
)
mycursor = db.cursor()


def genData(numRows):
    fake = Faker()
    csv_file = open("cookiedata.csv", "w")
    writer = csv.writer(csv_file)
    writer.writerow(["FirstName", "LastName", "Street", "City", "State", "Zip"])
    for i in range(0, numRows):
        writer.writerow([fake.first_name(),
                    fake.last_name(),
                    fake.street_address(),
                    fake.city(),
                    fake.state(),
                    fake.zipcode()])


def importData(fileName):
    mycursor = db.cursor()

    with open(fileName) as csvfile: #"with" will close the file stream for you!
        reader = csv.DictReader(csvfile)
        print("students imported")
        for row in reader:
            mycursor.execute('INSERT INTO Student(FirstName, LastName)'
                             'VALUES (%s,%s);', (row['FirstName'], row['LastName']))
            db.commit()
            stuID = mycursor.lastrowid
            mycursor.execute('INSERT INTO StudentAddress(StudentID, Street, City, State, Zip)'
                             'VALUES (%s,%s,%s,%s,%s);', (stuID, row['Street'], row['City'], row['State'], row['Zip']))
            db.commit()

genData(20)
importData("mydata.csv")

    # mycursor = db.cursor()
    # mycursor.execute('SELECT * FROM StudentTable;')
    # data = mycursor.fetchall()
    # db.commit()

# mycursor = db.cursor()
# mycursor.execute('SELECT * FROM StudentTable;')
# data = mycursor.fetchall()
#
# for d in data:
#     print(d[1])
#     print(d[4])
#
#
# mycursor.execute('INSERT INTO StudentTable(FirstName,LastName,Major,GPA)'
#                  'VALUES (%s,%s,%s,%s);', ('bar','foo','Math',3.9))
# db.commit()
# studentId = mycursor.lastrowid
#
# print("created new student", studentId)
#
# mycursor.execute('UPDATE StudentTable SET Major = %s'
#                  'WHERE StudentID = %s;', ('Economics',2))
# db.commit()
# print("student updated")








# OLD

mycursor.execute("SHOW TABLES;")
tablesData = pd.DataFrame(mycursor.fetchall())
tables = []

for i in range(len(tablesData)):
    tables.append(tablesData[0][i])

print(tables)

# Query for data/results with various parameters/filters

def query(tableName, columnName, filterBy):
    if tableName == "Cookie":
        mycursor.execute("SELECT * FROM Cookie "
                         "WHERE cookieID = %s;", (filterBy,))
    elif tableName == "Customer":
        mycursor.execute("SELECT * FROM Customer "
                         "WHERE %s = %s;", (columnName, filterBy,))
    elif tableName == "CustomerOrder":
        mycursor.execute("SELECT * FROM CustomerOrder "
                         "WHERE %s = %s;", (columnName, filterBy,))
    elif tableName == "Store":
        mycursor.execute("SELECT * FROM Store "
                         "WHERE %s = %s;", (columnName, filterBy,))
    tablesData = pd.DataFrame(mycursor.fetchall())
    print(tablesData)

# Soft delete based on table and ID

def delete(tableName, ID):
    if tableName == "Cookie":
        mycursor.execute("UPDATE Cookie SET deleted = 1"
                         "WHERE cookieID = %s;", ID)
    elif tableName == "Customer":
        mycursor.execute("UPDATE Customer SET deleted = 1"
                         "WHERE customerID = %s;", ID)
    elif tableName == "CustomerOrder":
        mycursor.execute("UPDATE CustomerOrder SET deleted = 1"
                         "WHERE cookieID = %s;", ID)
    elif tableName == "Store":
        mycursor.execute("UPDATE Store SET deleted = 1"
                         "WHERE storeID = %s;", ID)
    mydb.commit()


def update(tableName, ID, columnName, newVal):
    if tableName == "Cookie":
        mycursor.execute("UPDATE Cookie SET %s = %s"
                         "WHERE cookieID = %s;", (columnName, newVal, ID))
    elif tableName == "Customer":
        mycursor.execute("UPDATE Customer SET %s = %s"
                         "WHERE customerID = %s;", (columnName, newVal, ID))
    elif tableName == "CustomerOrder":
        mycursor.execute("UPDATE CustomerOrder SET %s = %s"
                         "WHERE orderID = %s;", (columnName, newVal, ID))
    elif tableName == "Store":
        mycursor.execute("UPDATE Store SET %s = %s"
                         "WHERE storeID = %s;", (columnName, newVal, ID))
    mydb.commit()


query("Cookie","cookieID",1)
