import mysql.connector
import csv
import genData as gd

# Connect to the database in GCP
db = mysql.connector.connect(
    host="35.235.87.251", # updated
    user="cookies_user",
    password="gloopybloopy",
    database="Cookies"
)
mycursor = db.cursor()

# Imports the cookies data into the table
def importCookies(fileName):
    with open(fileName) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mycursor.execute('INSERT INTO Cookie(flavor,cost,deleted)'
                             'VALUES (%s,%s,%s);', (row['flavor'], row['cost'], row['deleted']))
            db.commit()

# Imports the customers data into the table
def importCustomers(fileName):
    with open(fileName) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mycursor.execute('INSERT INTO Customer(fName,lName,sex,age,deleted)'
                             'VALUES (%s,%s,%s,%s,%s);', (row['fName'], row['lName'],row['sex'],row['age'],row['deleted']))
            db.commit()


# Imports the customer order data into the table
def importCustomerOrders(fileName):
    with open(fileName) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mycursor.execute('INSERT INTO CustomerOrder(customerID,storeID,orderDate,deleted)'
                             'VALUES (%s,%s,%s,%s);', (row['customerID'],row['storeID'],row['orderDate'],row['deleted']))
            db.commit()

# Imports the store data into the table
def importStores(fileName):
    with open(fileName) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mycursor.execute('INSERT INTO Store(name, state, phoneNum, deleted)'
                             'VALUES (%s,%s,%s,%s);', (row['name'], row['state'], row['phoneNum'], row['deleted']))
            db.commit()

# Imports the order details data into the table
def importOrderDetails(fileName):
    with open(fileName) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mycursor.execute('INSERT INTO OrderDetails(orderID, cookieID, quantity, price, deleted)'
                             'VALUES (%s,%s,%s,%s,%s);',
                             (row['orderID'], row['cookieID'], row['quantity'], row['price'], row['deleted']))
            db.commit()

# Imports all data into the database
def importData():
    importCookies(gd.cookie_file_name)
    importCustomers(gd.customer_file_name)
    importStores(gd.store_file_name)
    importCustomerOrders(gd.customer_order_file_name)
    importOrderDetails(gd.order_details_file_name)

importData()
