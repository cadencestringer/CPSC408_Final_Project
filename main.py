import mysql.connector
import csv
import datetime
import pandas as pd
from datetime import timedelta
from datetime import datetime

db = mysql.connector.connect(
    host="35.235.87.251", # updated
    user="cookies_user",
    password="gloopybloopy",
    database="Cookies"
)
mycursor = db.cursor()

def validInput(inputStr):
    return type(inputStr) == int and 0 < inputStr < 7

def printMenu():
    print("COOKIES DATABASE MENU\n")
    print("\n1. Print/display records"
          "\n2. Add record"
          "\n3. Delete record"
          "\n4. Update record"
          "\n5. Generate report"
          "\n6. Query with filters")
    choice = input("Please enter 1-6, or 'Exit' to leave the database")
    while not validInput(choice) and not choice.lower() == "exit":
        choice = input("Please enter valid input 1-6 or 'Exit': ")

    if choice.lower() == "exit":
        # EXIT PROGRAM
        print('exiting')
    else:
        choiceInt = int(choice)
        return choiceInt




#
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
    db.commit()


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
    db.commit()


query("Cookie","cookieID",1)
