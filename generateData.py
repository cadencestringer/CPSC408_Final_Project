import mysql.connector
import random
import datetime
from random import randrange
from datetime import timedelta
from datetime import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Jameskis13!Kaleo432!",
    database = "Cookies"
)

mycursor = mydb.cursor()

def generateCookieData():
    mycursor.execute("INSERT INTO Cookie (flavor, cost, deleted) VALUES ('Chocolate Chip', 0.99, 0),"
                    "('Sugar Cookie', 0.5, 0), ('Snickerdoodle', 0.75, 0),"
                    "('Dark Chocolate', 1, 0);")
    mydb.commit()

def deleteCookieData():
    mycursor.execute("DELETE FROM Cookie;")
    mydb.commit()

def generateCustomerData():
    fNames = ['John', 'James', 'Kaleo', 'Rene', 'Cadence']
    lNames = ['Smith', 'Christensen', 'Kistner', 'German', 'Stringer']
    sexes = ['M', 'F']

    for i in range(len(fNames)):
        if i % 2 == 0:
            sex = sexes[0]
        else:
            sex = sexes[1]
        age = random.randrange(18, 40)
        mycursor.execute("INSERT INTO Customer (fName, lName, sex, age, deleted)"
                        "VALUES (%s, %s, %s, %s, %s);", (fNames[i], lNames[i], sex, age, 0))
        mydb.commit()

def deleteCustomerData():
    mycursor.execute("DELETE FROM Customer;")
    mydb.commit()

def random_date():
    start = datetime.strptime('1/1/2021 5:00 AM', '%m/%d/%Y %I:%M %p')
    end = datetime.strptime('1/31/2021 9:00 PM', '%m/%d/%Y %I:%M %p')
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

def generateOrderData():
    for i in range(500):
        customer = random.randrange(1, 5)
        cookie = random.randrange(1, 4)
        store = random.randrange(1, 4)
        date = random_date()
        quant = random.randrange(1, 10)
        price = quant * 3.99 + random.randrange(1, 3)
        mycursor.execute("INSERT INTO CustomerOrder (customerID, storeID, cookieID, "
                        "orderDate, quantity, price, deleted) VALUES"
                        "(%s, %s, %s, %s, %s, %s, %s);",
        (customer, store, cookie, date, quant, price, 0))
        mydb.commit()

def deleteOrderData():
    mycursor.execute("DELETE FROM CustomerOrder;")
    mydb.commit()

def generateStoreData():
    names = ['Orange', 'Aspen', 'Dallas', 'Salt Lake City']
    states = ['CA', 'CO', 'TX', 'UT']
    phoneNums = ['(512)-323-3112', '(533)-321-9854', '(970)-342-3095',
                 '(671)-321-9878']
    for i in range(4):
        mycursor.execute("INSERT INTO Store (name, state, phoneNum, deleted) VALUES "
                         "(%s, %s, %s, %s);", (names[i], states[i], phoneNums[i], 0))
        mydb.commit()

def deleteStoreData():
    mycursor.execute("DELETE FROM Store;")
    mydb.commit()

def resetTables():
    mycursor.execute("ALTER TABLE Cookie AUTO_INCREMENT = 1")
    mydb.commit()
    mycursor.execute("ALTER TABLE Customer AUTO_INCREMENT = 1")
    mydb.commit()
    mycursor.execute("ALTER TABLE CustomerOrder AUTO_INCREMENT = 1")
    mydb.commit()
    mycursor.execute("ALTER TABLE Store AUTO_INCREMENT = 1")
    mydb.commit()

    deleteOrderData()
    deleteCustomerData()
    deleteCookieData()
    deleteStoreData()
    resetTables()
    generateStoreData()
    generateCookieData()
    generateCustomerData()
    generateOrderData()


# ASK ABOUT ORGANIZATION OF ORDER TABLE