import mysql.connector
import re
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


# Checks for valid input

def validInput(inputStr):
    return type(inputStr) == int and 0 < inputStr < 7


# Checks for float

def isFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# Checks for a valid phone number

def valid_phone_num(val):
    pattern = "\(\d{3}\)-\d{3}-\d{4}"
    patternExt = "\(\d{3}\)-\d{3}-\d{4}x\d"
    isPhone = re.match(pattern, val)
    isPhoneExt = re.match(patternExt, val)
    if isPhone or isPhoneExt:
        return True
    return False


def menuSelection():
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
        print("Exiting database.")
        # EXIT PROGRAM **
    else:
        choiceInt = int(choice)
        return choiceInt


# Query in each table using ID

def queryID(tableName, filterBy):
    if tableName == "Cookie":
        mycursor.execute("SELECT * FROM Cookie "
                         "WHERE cookieID = %s;", (filterBy,))
    elif tableName == "Customer":
        mycursor.execute("SELECT * FROM Customer "
                         "WHERE customerID = %s;", (filterBy,))
    elif tableName == "CustomerOrder":
        mycursor.execute("SELECT * FROM CustomerOrder "
                         "WHERE orderID = %s;", (filterBy,))
    elif tableName == "OrderDetails":
        mycursor.execute("SELECT * FROM OrderDetails "
                         "WHERE detailID = %s;", (filterBy,))
    elif tableName == "Store":
        mycursor.execute("SELECT * FROM Store "
                         "WHERE storeID = %s;", (filterBy,))
    tablesData = pd.DataFrame(mycursor.fetchall())
    print(tablesData)


# Queries using the name of a customer, store, or cookie

def queryName(tableName, filterBy):
    if tableName == "Cookie":
        mycursor.execute("SELECT * FROM Cookie "
                         "WHERE flavor = %s;", (filterBy,))
    elif tableName == "Customer":
        mycursor.execute("SELECT * FROM Customer "
                         "WHERE fName = %s;", (filterBy,))
    elif tableName == "Store":
        mycursor.execute("SELECT * FROM Store "
                         "WHERE name = %s;", (filterBy,))
    tablesData = pd.DataFrame(mycursor.fetchall())
    print(tablesData)


# Soft delete based on table and ID
# NOT WORKING ***
# def delete(tableName, ID):
#     if tableName == "Cookie":
#         mycursor.execute("UPDATE Cookie SET deleted = 1"
#                          "WHERE cookieID = %s;", (ID,))
#     elif tableName == "Customer":
#         mycursor.execute("UPDATE Customer SET deleted = 1"
#                          "WHERE customerID = %s;", (ID,))
#     elif tableName == "CustomerOrder":
#         mycursor.execute("UPDATE CustomerOrder SET deleted = 1"
#                          "WHERE cookieID = %s;", (ID,))
#     elif tableName == "OrderDetails":
#         mycursor.execute("UPDATE OrderDetails SET deleted = 1"
#                          "WHERE detailID = %s;", (ID,))
#     elif tableName == "Store":
#         mycursor.execute("UPDATE Store SET deleted = 1"
#                          "WHERE storeID = %s;", (ID,))
#     db.commit()


# Updates a value using an ID
# NOT WORKING ***
# def update(tableName, ID, columnName, newVal):
#     if tableName == "Cookie":
#         mycursor.execute("UPDATE Cookie SET %s = %s"
#                          "WHERE cookieID = %s;", (columnName, newVal, ID))
#     elif tableName == "Customer":
#         mycursor.execute("UPDATE Customer SET %s = %s"
#                          "WHERE customerID = %s;", (columnName, newVal, ID))
#     elif tableName == "CustomerOrder":
#         mycursor.execute("UPDATE CustomerOrder SET %s = %s"
#                          "WHERE orderID = %s;", (columnName, newVal, ID))
#     elif tableName == "Store":
#         mycursor.execute("UPDATE Store SET %s = %s"
#                          "WHERE storeID = %s;", (columnName, newVal, ID))
#     db.commit()


# Adds a new cookie record

def addCookie():
    flavor = input("What is the cookie's flavor?")
    cost = input("What is the cookie's cost?")
    while not isFloat(cost) and not cost.isnumeric():
        cost = input("Please enter a numeric cookie cost:")
    cost = float(cost)
    mycursor.execute("INSERT INTO Cookie (flavor,cost,deleted) VALUES (%s,%s,%s);", (flavor, cost, 0))
    db.commit()
    id = mycursor.lastrowid
    return id


# Adds a new customer record

def addCustomer():
    fName = input("What is the customer's first name?")
    lName = input("What is the customer's first name?")
    sex = input("What is the customer's gender? Enter 0 for female, 1 for male")
    while not (sex == '0' or sex == '1'):
        sex = input("Please enter either a 0 for female or 1 for male:")
    sex = chr(sex)
    age = input("What is the customer's age?")
    while not type(age) == int:
        age = input("Please enter a numeric age:")
    age = int(age)
    mycursor.execute("INSERT INTO Customer(fName,lName,sex,age,deleted) VALUES (%s,%s,%s,%s,%s);", (fName, lName, sex, age, 0))
    db.commit()
    id = mycursor.lastrowid
    return id


# Adds a new store record

def addStore():
    name = input("What is the store's name? Stores are named after their location.")
    state = input("What is the full name of the state the store is located in?")
    phoneNum = input("What is the store's phone number, and extension if applicable? Enter in (000)-000-0000 format OR with extension (000)-000-0000x111")
    while not valid_phone_num(phoneNum):
        phoneNum = input("Please enter phone number in (000)-000-0000 format OR with extension (000)-000-0000x111:")
    mycursor.execute("INSERT INTO Store (name, state, phoneNum, deleted) VALUES (%s,%s,%s,%s);", (name, state, phoneNum, 0))
    db.commit()
    id = mycursor.lastrowid
    return id


# Checks that a record exists in a table to ensure referential integrity

def integrityCheck(tableName, idNum):
    idNum = int(idNum)
    if tableName == "Customer":
        mycursor.execute("SELECT COUNT(*) FROM Customer WHERE Customer.customerID = %s;", (idNum,))
    elif tableName == "Cookie":
        mycursor.execute("SELECT COUNT(*) FROM Cookie WHERE Cookie.cookieID = %s;", (idNum,))
    elif tableName == "Store":
        mycursor.execute("SELECT COUNT(*) FROM Store WHERE Store.storeID = %s;", (idNum,))
    result = mycursor.fetchall()
    return result[0][0]


def fixError(tableName):
    print("The " + tableName + " ID you entered does not exist in the database.")
    choice = input("Would you like to 1. Create a new record or 2. Enter a new ID? Please enter 1 or 2:")
    result = 0
    if choice == "1":
        if tableName == "Cookie":
            id = addCookie()
        elif tableName == "Customer":
            id = addCustomer()
        else:
            id = addStore()
    else:
        while not result > 0:
            id = input("Enter the new ID number:")
            result = integrityCheck(tableName,id)
    return id


# Adds a new order record (adding to both CustomerOrder and OrderDetails tables)

def addOrder(): # make sure the store exists, make sure the customer exists, make sure the cookie exists
    customerID = input("What is the ID of the customer who placed the order?")
    customerCheck = integrityCheck("Customer",customerID)
    if customerCheck == 0:
        customerID = fixError("Customer")

    storeID = input("What is the ID of the store the order was placed at?")
    storeCheck = integrityCheck("Store",storeID)
    if storeCheck == 0:
        storeID = fixError("Store")

    orderDate = input("What is the date the order was made?")

    mycursor.execute("INSERT INTO CustomerOrder(customerID,storeID,orderDate,deleted) VALUES (%s,%s,%s,%s);", (customerID, storeID, orderDate, 0))
    db.commit()
    orderID = mycursor.lastrowid

    numCookies = input("How many different cookie flavors were in this order?")
    while not numCookies.isdigit():
        numCookies = input("Please enter an integer for number of cookie flavors bought:")
    numCookies = int(numCookies)
    for x in range(numCookies):
        print("COOKIE " + str(x+1))
        cookieID = input("What is the cookie ID?")
        cookieCheck = integrityCheck("Cookie", cookieID)
        if cookieCheck == 0:
            cookieID = fixError("Cookie")
        numCookies = input("How many of this cookie flavor did they buy?")
        mycursor.execute("INSERT INTO OrderDetails(orderID, cookieID, quantity, deleted) VALUES (%s,%s,%s,%s);", (orderID, cookieID, numCookies, 0))
        db.commit()

    print('Order added.')

def get_total_sales(filter):
    if filter == 'all':
        mycursor.execute("SELECT Sum(quantity*price) as total_sales FROM OrderDetails "
                         "where deleted = 0;")
    elif filter == 'store':
        mycursor.execute("SELECT DISTINCT s.name as store_name, SUM(5*od.quantity) as total_sales "
                         "FROM Store as s left join CustomerOrder as co on co.storeID= s.storeID "
                         "left join OrderDetails as od on od.orderID = co.orderID "
                         "where od.deleted = 0 "
                         "and co.deleted = 0 "
                         "and s.deleted = 0 "
                         "GROUP BY 1 ORDER BY 1;")
    elif filter == 'state':
        mycursor.execute("SELECT DISTINCT s.state as state, SUM(5*od.quantity) as total_sales "
                         "FROM Store as s left join CustomerOrder as co on co.storeID= s.storeID "
                         "left join OrderDetails as od on od.orderID = co.orderID "
                         "where od.deleted = 0 "
                         "and co.deleted = 0 "
                         "and s.deleted = 0 "
                         "GROUP BY 1 ORDER BY 1;")
    elif filter == 'date':
        mycursor.execute("SELECT DISTINCT DATE_FORMAT(co.orderDate, '%y-%m-%d') as day, SUM(5*od.quantity) as total_sales "
                         "FROM Store as s "
                         "left join CustomerOrder as co on co.storeID= s.storeID "
                         "left join OrderDetails as od on od.orderID = co.orderID "
                         "where od.deleted = 0 "
                         "and co.deleted = 0 "
                         "and s.deleted = 0 "
                         "GROUP BY 1 ORDER BY 1;")

    else:
        print("Invalid Filter")
        exit(0)
    salesData = pd.DataFrame(mycursor.fetchall())
    print(salesData)
    export = input("Would you like to export this data? (y/n): ")
    if export == 'y':
        exportData(salesData)


def exportData(dataframe):
    filename = input("What file would you like this data exported to (make sure to include .csv or .xlsx): ")
    while not ".csv" in filename and not ".xlsx" in filename:
        filename = input("What file would you like this data exported to (make sure to include .csv or .xlsx): ")
    if ".csv" in filename:
        dataframe.to_csv(filename)
    else:
        dataframe.to_excel(filename)


# TESTING

# query("Cookie","cookieID",1)
# query("Customer","customerID",1)
delete("Cookie",1)
# addOrder()
