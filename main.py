import mysql.connector
import re
import csv
import datetime
import pandas as pd
from IPython.display import HTML
from datetime import timedelta
from datetime import datetime

# https://stackoverflow.com/questions/5010042/mysql-get-column-name-or-alias-from-query

db = mysql.connector.connect(
    host="35.235.87.251",  # updated
    user="cookies_user",
    password="gloopybloopy",
    database="Cookies"
)
mycursor = db.cursor()


# Checks for float

def isFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# Checks for valid input

def validInput(inputStr, maxSize):
    if isInt(inputStr):
        inputStr = int(inputStr)
        if 0 < inputStr <= maxSize:
            return True
        else:
            return False
    else:
        return False


# Checks for int

def isInt(s):
    try:
        int(s)
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


# Prints menu and returns user selection

def menuSelection():
    print("\nCOOKIES DATABASE MENU")
    print("1. Print/display records"
          "\n2. Add record"
          "\n3. Delete record"
          "\n4. Update record"
          "\n5. Query with filters"
          "\n6. Display sales data")
    choice = input("Please enter 1-6, or 'Exit' to leave the database: ")
    while not validInput(choice, 6) and not choice.lower() == "exit":
        choice = input("Please enter valid input 1-6 or 'Exit': ")

    if choice.lower() == "exit":
        print("Exiting database.")
        return 0
    else:
        choiceInt = int(choice)
        return choiceInt


# Print all table data

def printTable(tableName):
    if tableName == "Cookie":
        print("\nCOOKIE TABLE")
        mycursor.execute("SELECT * FROM Cookie WHERE deleted = 0;")
    elif tableName == "Customer":
        print("\nCUSTOMER TABLE")
        mycursor.execute("SELECT * FROM Customer WHERE deleted = 0;")
    elif tableName == "CustomerOrder":
        print("\nCUSTOMER ORDER TABLE")
        mycursor.execute("SELECT * FROM CustomerOrder WHERE deleted = 0;")
    elif tableName == "OrderDetails":
        print("\nORDER DETAILS TABLE")
        mycursor.execute("SELECT * FROM OrderDetails WHERE deleted = 0;")
    elif tableName == "Store":
        print("\nSTORE TABLE")
        mycursor.execute("SELECT * FROM Store WHERE deleted = 0;")
    field_names = [i[0] for i in mycursor.description]
    tablesData = pd.DataFrame(mycursor.fetchall())
    tablesData.columns = field_names
    pd.set_option('display.max_rows', None)
    print(tablesData.to_string(index=False))
    exportData(tablesData)


# Query in each table using ID

def queryID(tableName, filterBy):
    if tableName == "Cookie":
        mycursor.execute("SELECT * FROM Cookie "
                         "WHERE cookieID = %s "
                         "AND deleted = 0;", (filterBy,))
    elif tableName == "Customer":
        mycursor.execute("SELECT * FROM Customer "
                         "WHERE customerID = %s "
                         "AND deleted = 0;", (filterBy,))
    elif tableName == "CustomerOrder":
        mycursor.execute("SELECT * FROM CustomerOrder "
                         "WHERE orderID = %s "
                         "AND deleted = 0;", (filterBy,))
    elif tableName == "OrderDetails":
        mycursor.execute("SELECT * FROM OrderDetails "
                         "WHERE detailID = %s "
                         "AND deleted = 0;", (filterBy,))
    elif tableName == "Store":
        mycursor.execute("SELECT * FROM Store "
                         "WHERE storeID = %s "
                         "AND deleted = 0;", (filterBy,))
    tablesData = pd.DataFrame(mycursor.fetchall())
    print(tablesData)
    exportData(tablesData)


# Queries using the name of a store or cookie

def queryName(tableName, filterBy):
    if tableName == "Cookie":
        mycursor.execute("SELECT * FROM Cookie "
                         "WHERE flavor = %s "
                         "AND deleted = 0;", (filterBy,))
    elif tableName == "Store":
        mycursor.execute("SELECT * FROM Store "
                         "WHERE name = %s "
                         "AND deleted = 0;", (filterBy,))
    tablesData = pd.DataFrame(mycursor.fetchall())
    print(tablesData)
    exportData(tablesData)


# Queries by customer first name

def queryCustFName(filterBy):
    mycursor.execute("SELECT * FROM Customer "
                     "WHERE fName = %s "
                     "AND deleted = 0;", (filterBy,))
    tablesData = pd.DataFrame(mycursor.fetchall())
    print(tablesData)
    exportData(tablesData)


# Queries by customer first name

def queryCustLName(filterBy):
    mycursor.execute("SELECT * FROM Customer "
                     "WHERE lName = %s "
                     "AND deleted = 0;", (filterBy,))
    tablesData = pd.DataFrame(mycursor.fetchall())
    print(tablesData)
    exportData(tablesData)


# Soft delete based on table and ID

def delete(tableName, ID):
    if tableName == "Cookie":
        mycursor.execute("UPDATE Cookie SET deleted = 1 "
                         "WHERE cookieID = %s;", (ID,))
    elif tableName == "Customer":
        print(1)
        mycursor.execute("UPDATE Customer SET deleted = 1 "
                         "WHERE customerID = %s;", (int(ID),))
        print(1)
    elif tableName == "CustomerOrder":
        mycursor.execute("UPDATE CustomerOrder SET deleted = 1 "
                         "WHERE cookieID = %s;", (ID,))
    elif tableName == "OrderDetails":
        mycursor.execute("UPDATE OrderDetails SET deleted = 1 "
                         "WHERE detailID = %s;", (ID,))
    elif tableName == "Store":
        mycursor.execute("UPDATE Store SET deleted = 1 "
                         "WHERE storeID = %s;", (ID,))
    try:
        db.commit()
        print("Row deleted successfully!")
    except:
        db.rollback()


# Updates a value using an ID

def update(tableName, ID, newVal):
    if tableName == "Cookie":
        mycursor.execute("UPDATE Cookie SET 'cost' = %s "
                         "WHERE cookieID = %s;", (newVal, ID))
    elif tableName == "Customer":
        mycursor.execute("UPDATE Customer SET 'age' = %s "
                         "WHERE customerID = %s;", (newVal, ID))
    elif tableName == "Store":
        mycursor.execute("UPDATE Store SET 'name' = %s "
                         "WHERE storeID = %s;", (newVal, ID))
    try:
        db.commit()
        print(tableName + " updated successfully!")
    except:
        db.rollback()


# Roll back

def rollback():
    db.rollback()
    print("Rollback successful!")


# Adds a new cookie record

def addCookie():
    flavor = input("What is the cookie's flavor? ")
    cost = input("What is the cookie's cost? ")
    while not isFloat(cost) and not cost.isnumeric():
        cost = input("Please enter a numeric cookie cost: ")
    cost = float(cost)
    try:
        mycursor.execute("INSERT INTO Cookie (flavor,cost,deleted) VALUES (%s,%s,%s);", (flavor, cost, 0))
        db.commit()
        id = mycursor.lastrowid
        return id
    except:
        db.rollback()
        return None


# Adds a new customer record

def addCustomer():
    fName = input("What is the customer's first name?")
    lName = input("What is the customer's first name?")
    sex = input("What is the customer's gender? Enter 0 for female, 1 for male")
    while not (sex == '0' or sex == '1'):
        sex = input("Please enter either a 0 for female or 1 for male:")
    sex = chr(sex)
    age = input("What is the customer's age?")
    while not isInt(age):
        age = input("Please enter a numeric age:")
    age = int(age)
    mycursor.execute("INSERT INTO Customer(fName,lName,sex,age,deleted) VALUES (%s,%s,%s,%s,%s);",
                     (fName, lName, sex, age, 0))
    db.commit()
    id = mycursor.lastrowid
    return id


# Adds a new store record

def addStore():
    name = input("What is the store's name? Stores are named after their location.")
    state = input("What is the full name of the state the store is located in?")
    phoneNum = input(
        "What is the store's phone number, and extension if applicable? Enter in (000)-000-0000 format OR with extension (000)-000-0000x111")
    while not valid_phone_num(phoneNum):
        phoneNum = input("Please enter phone number in (000)-000-0000 format OR with extension (000)-000-0000x111:")
    mycursor.execute("INSERT INTO Store (name, state, phoneNum, deleted) VALUES (%s,%s,%s,%s);",
                     (name, state, phoneNum, 0))
    db.commit()
    id = mycursor.lastrowid
    return id


# Checks that a record exists in a table to ensure referential integrity

def integrityCheck(tableName, idNum):
    idNum = int(idNum)
    if tableName == "Customer":
        mycursor.execute("SELECT COUNT(*) FROM Customer WHERE Customer.customerID = %s "
                         "AND deleted = 0;", (idNum,))
    elif tableName == "Cookie":
        mycursor.execute("SELECT COUNT(*) FROM Cookie WHERE Cookie.cookieID = %s "
                         "AND deleted = 0;", (idNum,))
    elif tableName == "Store":
        mycursor.execute("SELECT COUNT(*) FROM Store WHERE Store.storeID = %s "
                         "AND deleted = 0;", (idNum,))
    result = mycursor.fetchall()
    return result[0][0]


# Ensures referential integrity when adding records

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
            id = input("Enter the new ID number: ")
            result = integrityCheck(tableName, id)
    return id


# Adds a new order record (adding to both CustomerOrder and OrderDetails tables)

def addOrder():  # make sure the store exists, make sure the customer exists, make sure the cookie exists
    customerID = input("What is the ID of the customer who placed the order?")
    customerCheck = integrityCheck("Customer", customerID)
    if customerCheck == 0:
        customerID = fixError("Customer")

    storeID = input("What is the ID of the store the order was placed at?")
    storeCheck = integrityCheck("Store", storeID)
    if storeCheck == 0:
        storeID = fixError("Store")

    orderDate = input("What is the date the order was made?")

    mycursor.execute("INSERT INTO CustomerOrder(customerID,storeID,orderDate,deleted) VALUES (%s,%s,%s,%s);",
                     (customerID, storeID, orderDate, 0))
    db.commit()
    orderID = mycursor.lastrowid

    numCookies = input("How many different cookie flavors were in this order?")
    while not numCookies.isdigit():
        numCookies = input("Please enter an integer for number of cookie flavors bought:")
    numCookies = int(numCookies)
    for x in range(numCookies):
        print("COOKIE " + str(x + 1))
        cookieID = input("What is the cookie ID?")
        cookieCheck = integrityCheck("Cookie", cookieID)
        if cookieCheck == 0:
            cookieID = fixError("Cookie")
        numCookies = input("How many of this cookie flavor did they buy?")
        mycursor.execute("INSERT INTO OrderDetails(orderID, cookieID, quantity, deleted) VALUES (%s,%s,%s,%s);",
                         (orderID, cookieID, numCookies, 0))
        db.commit()


# Prints aggregate sales data based on filter

def get_total_sales(filterBy):
    if filterBy == 'all':
        mycursor.execute("SELECT sum(sub.net_sales) as net_sales "
                         "from (SELECT DISTINCT OD.cookieID, "
                         "sum(OD.quantity * 5) - sum(OD.quantity * C.cost) as net_sales "
                         "from OrderDetails OD "
                         "left join Cookie C on OD.cookieID = C.cookieID "
                         "where OD.deleted = 0 "
                         "and C.deleted = 0 "
                         "GROUP BY 1) as sub "
                         "WHERE deleted = 0;")
    elif filterBy == 'store':
        mycursor.execute("SELECT DISTINCT sub.store_name, sum(sub.net_sales) as net_sales "
                         "from (SELECT DISTINCT OD.cookieID, S.name as store_name, "
                         "sum(OD.quantity * 5) - sum(OD.quantity * C.cost) as net_sales "
                         "from OrderDetails OD "
                         "left join Cookie C on OD.cookieID = C.cookieID "
                         "left join CustomerOrder CO on OD.orderID = CO.orderID "
                         "left join Store S on CO.storeID = S.storeID "
                         "where OD.deleted = 0 "
                         "and C.deleted = 0 and S.deleted = 0 and CO.deleted = 0 "
                         "GROUP BY 1, 2) as sub GROUP BY 1 ORDER BY 1;")
    elif filterBy == 'state':
        mycursor.execute("SELECT DISTINCT sub.state, sum(sub.net_sales) as net_sales "
                         "from (SELECT DISTINCT OD.cookieID, S.state as state, "
                         "sum(OD.quantity * 5) - sum(OD.quantity * C.cost) as net_sales "
                         "from OrderDetails OD "
                         "left join Cookie C on OD.cookieID = C.cookieID "
                         "left join CustomerOrder CO on OD.orderID = CO.orderID "
                         "left join Store S on CO.storeID = S.storeID "
                         "where OD.deleted = 0 "
                         "and C.deleted = 0 and S.deleted = 0 and CO.deleted = 0 "
                         "GROUP BY 1, 2) as sub GROUP BY 1 ORDER BY 1;")
    elif filterBy == 'date':
        mycursor.execute(
            "SELECT DISTINCT DATE_FORMAT(co.orderDate, '%y-%m-%d') AS day, SUM(quantity * 5) - SUM(quantity * cost) as net_sales "
            "from CustomerOrder co "
            "left join OrderDetails OD on co.orderID = OD.orderID "
            "left join Cookie C on OD.cookieID = C.cookieID "
            "where co.deleted = 0 and OD.deleted = 0 and C.deleted = 0 "
            "GROUP BY 1;")
    elif filterBy == 'weekday':
        mycursor.execute(
            "SELECT DISTINCT (DAYNAME(co.orderDate)) AS day, SUM(quantity * 5) - SUM(quantity * cost) as net_sales "
            "from CustomerOrder co "
            "left join OrderDetails OD on co.orderID = OD.orderID "
            "left join Cookie C on OD.cookieID = C.cookieID "
            "where co.deleted = 0 and OD.deleted = 0 and C.deleted = 0 "
            "GROUP BY 1;")

    else:
        print("Invalid Filter")
        exit(0)

    # Pretty print
    field_names = [i[0] for i in mycursor.description]
    salesData = pd.DataFrame(mycursor.fetchall())
    salesData.columns = field_names
    pd.set_option('display.max_rows', None)
    print(salesData.to_string(index=False))

    export = input("Would you like to export this data? (Y/N): ")
    if export == "y" or export == "Y":
        exportData(salesData)


# Exports data to a CSV file

def exportData(dataframe):
    choice = input("Would you like to export the data? (Y/N): ")
    if choice == "Y" or choice == "y":
        dataframe = pd.DataFrame(dataframe)
        filename = input("What file would you like this data exported to (make sure to include .csv or .xlsx): ")
        while not ".csv" in filename and not ".xlsx" in filename:
            filename = input("Please enter a file name with a .csv or .xlsx extension: ")
        if ".csv" in filename:
            dataframe.to_csv(filename)
        else:
            dataframe.to_excel(filename)
        print("Exported successfully.")


# Prompts the user and runs the commands

def runSelection(choice):
    if choice == 1:
        table = input("What table would you like to display?"
                      "\n1. Cookie"
                      "\n2. Customer"
                      "\n3. Customer Order"
                      "\n4. Order Details"
                      "\n5. Store"
                      "\nPlease enter your selection:")
        while not validInput(table, 5):
            table = input("Please enter a number 1-5:")
        if table == "1":
            printTable("Cookie")
        elif table == "2":
            printTable("Customer")
        elif table == "3":
            printTable("CustomerOrder")
        elif table == "4":
            printTable("OrderDetails")
        elif table == "5":
            printTable("Store")

    # Insert a record
    elif choice == 2:
        tableToAdd = input("What record would you like to add?"
                           "\n1. Cookie"
                           "\n2. Customer"
                           "\n3. Store"
                           "\n4. Order"
                           "\nPlease enter your selection: ")
        while not validInput(tableToAdd, 4):
            tableToAdd = input("Please enter a number 1-4: ")
        if tableToAdd == "1":
            addCookie()
        elif tableToAdd == "2":
            addCustomer()
        elif tableToAdd == "3":
            addStore()
        elif tableToAdd == "4":
            addOrder()

    # Delete a record
    elif choice == 3:
        table = input("What table would you like to delete from?"
                      "\n1. Cookie"
                      "\n2. Customer"
                      "\n3. Customer Order"
                      "\n4. Order Details"
                      "\n5. Store"
                      "\nPlease enter your selection: ")
        while not validInput(table, 5):
            table = input("Please enter a number 1-5: ")
        ID = input("What is the ID # of the record you'd like to delete? ")
        if table == "1":
            delete("Cookie", ID)
        elif table == "2":
            delete("Customer", ID)
        elif table == "3":
            delete("CustomerOrder", ID)
        elif table == "4":
            delete("OrderDetails", ID)
        elif table == "5":
            delete("Store", ID)

    # Update a record
    elif choice == 4:
        table = input("What would you like to update?"
                      "\n1. Cookie cost"
                      "\n2. Customer age"
                      "\n3. Store name"
                      "\nPlease enter your selection: ")
        while not validInput(table, 3):
            table = input("Please enter a number 1-3: ")
        id = input("What is the ID # of the record you'd like to update? ")
        while not isInt(id):
            id = input("Please enter a numeric ID number: ")

        newVal = input("What is the new value? ")

        if table == "1":
            if isInt(newVal):
                newValInt = int(newVal)
                update("Cookie", id, newValInt)
        elif table == "2":
            if isInt(newVal):
                newValInt = int(newVal)
                update("Customer", id, newValInt)
        elif table == "3":
            update("Store", id, newVal)

    # Generate report
    elif choice == 5:
        query = input("What would you like to query by?"
                      "\n1. ID"
                      "\n2. Name"
                      "\nPlease enter your selection: ")
        while not validInput(query, 2):
            query = input("Please enter a number 1-2: ")
        # Query by ID
        if query == "1":
            table = input("What table would you like to query?"
                          "\n1. Cookie"
                          "\n2. Customer"
                          "\n3. Customer Order"
                          "\n4. Order Details"
                          "\n5. Store"
                          "\nPlease enter your selection: ")
            while not validInput(table, 5):
                table = input("Please enter a number 1-5: ")
            ID = input("What is the ID you'd like to query? ")
            while not isInt(ID):
                ID = input("Please enter an integer ID: ")
            if table == "1":
                queryID("Cookie", ID)
            elif table == "2":
                queryID("Customer", ID)
            elif table == "3":
                queryID("CustomerOrder", ID)
            elif table == "4":
                queryID("OrderDetails", ID)
            elif table == "5":
                queryID("Store", ID)
        # Query by name
        elif query == "2":
            table = input("What table would you like to query?"
                          "\n1. Cookie"
                          "\n2. Customer"
                          "\n3. Store"
                          "\nPlease enter your selection: ")
            while not table == "1" and not table == "2" and not table == "3":
                table = input("Please enter a number 1-3: ")
            if table == "2":
                nameType = input("Would you like to query by 1. first name or 2. last name? ")
                while not validInput(nameType, 2):
                    nameType = input("Please enter 1 or 2: ")
                name = input("What is the name you'd like to query? ")
                if nameType == "1":
                    queryCustFName(name)
                elif nameType == "2":
                    queryCustFName(name)
            else:
                name = input("What is the name you'd like to query? ")
                if table == "1":
                    queryName("Cookie", name)
                elif table == "3":
                    queryName("Store", name)

    # Display sales data with filters
    elif choice == 6:

        filterBy = input("What would you like to filter sales data by?"
                         "\n1. No filter- display all"
                         "\n2. Store"
                         "\n3. State"
                         "\n4. Date"
                         "\nPlease enter your selection: ")
        while not validInput(filterBy, 4):
            filterBy = input("Please enter a number 1-4:")
        if filterBy == "1":
            get_total_sales("all")
        elif filterBy == "2":
            get_total_sales("store")
        elif filterBy == "3":
            get_total_sales("state")
        elif filterBy == "4":
            get_total_sales("date")


# Runs the database program

def runProgram():
    print("Welcome to the Cookies Database.\n")
    userChoice = 1
    while userChoice > 0:
        userChoice = menuSelection()
        runSelection(userChoice)
    exit(0)


runProgram()
