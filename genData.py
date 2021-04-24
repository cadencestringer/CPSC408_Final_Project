from faker import Faker
import csv
import random
import datetime
from random import choice

# Print statements to get input and generate the csv files:
print("Make sure to include the .csv extension after the file name.")
cookie_file_name = input("Enter the filename for the Cookie data: ")
while not 'csv' in cookie_file_name:
    cookie_file_name = input("Enter the filename for the Cookie data, with a .csv extension: ")
cookie_nrows = int(input("Enter the number of rows: "))

customer_file_name = input("Enter the filename for the Customer data: ")
while not 'csv' in customer_file_name:
    customer_file_name = input("Enter the filename for the Customer data, with a .csv extension: ")
customer_nrows = int(input("Enter the number of rows: "))

store_file_name = input("Enter the filename for the Store data: ")
while not 'csv' in store_file_name:
    store_file_name = input("Enter the filename for the Store data, with a .csv extension: ")
store_nrows = int(input("Enter the number of rows: "))

customer_order_file_name = input("Enter the filename for the Customer Order data: ")
while not 'csv' in customer_order_file_name:
    customer_order_file_name = input("Enter the filename for the Customer Order data, with a .csv extension: ")
customer_order_nrows = int(input("Enter the number of rows: "))

order_details_file_name = input("Enter the filename for the Order Details data: ")
while not 'csv' in order_details_file_name:
    order_details_file_name = input("Enter the filename for the Order Details data, with a .csv extension: ")
order_details_nrows = int(input("Enter the number of rows: "))

# Generates customer data using user input
def genCustomer():
    fake = Faker()
    customer_csv = open(customer_file_name, "w")
    writer = csv.writer(customer_csv)
    writer.writerow(["fName", "lName", "sex", "age", "deleted"])

    for i in range(customer_nrows):
        writer.writerow([fake.first_name(),
                    fake.last_name(),
                    random.randrange(0, 2),
                    random.randrange(18, 100),
                    0])

# Generates a random flavor combination to fill the cookies table
def genFlavor():
    base_flavor = ["Peanut Butter", "Lime", "Lemon", "Raspberry", "Cherry",
                   "Double Dark Chocolate", "Vanilla", "Caramel", "Sugar",
                   "Chocolate", "Walnut", "Almond", "Blueberry", "Gingerbread",
                   "Pineapple", "Apple", "Pumpkin", "Pecan", "Maple", "Coconut",
                   "Snicker Doodle", "Mint", "Banana Bread"]
    flavor = ["Swirl", "Volcano", "Lava", "with Sugar", "with Sprinkles",
              "Crumble", "Blondie", "Cupcake", "Candy",
              "Cake", "Pie", "Sundae", "Fudge", "Funfetti"]
    new_dessert = choice(base_flavor) + " " + choice(flavor)
    return new_dessert


# Generates cookie data
def genCookies():
    cookie_csv = open(cookie_file_name, "w")
    writer = csv.writer(cookie_csv)
    writer.writerow(["flavor", "cost", "deleted"])

    cost = [1.99, 1.50, 2.00, 1.75, 2.99, 1.00, 0.75]

    for i in range(cookie_nrows):
        writer.writerow([genFlavor(), choice(cost), 0])


# Generates store data
def genStores():
    fake = Faker()
    stores_csv = open(store_file_name, 'w')
    writer = csv.writer(stores_csv)
    writer.writerow(["name", "state", "phoneNum", "deleted"])

    for i in range(0, store_nrows):  # used to be one row
        writer.writerow([fake.city(),
                    fake.state(),
                    fake.phone_number(),
                    0])

# Generates order details data
def genOrderDetails():
    order_details_data = open(order_details_file_name, 'w')
    writer = csv.writer(order_details_data)
    writer.writerow(['orderID', 'cookieID', 'quantity', 'price', 'deleted'])

    for i in range(0, order_details_nrows):
        orderID = random.randrange(1, (customer_order_nrows+1))
        cookieID = random.randrange(1, 8)
        quantity = random.randrange(1, 11)  # they can only buy up to 10 cookies
        price = quantity * 5
        writer.writerow([orderID, cookieID, quantity, price, 0])

# Generates a random date between January 1st 2020 and February 1st 2020 for the purchase date
def randDate():
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2020, 2, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    return random_date


# Generates customer order data
def genCustomerOrders():
    customer_order_data = open(customer_order_file_name, 'w')
    writer = csv.writer(customer_order_data)
    writer.writerow(['customerID', 'storeID', 'orderDate', 'deleted'])

    for i in range(customer_order_nrows):
        customerID = random.randrange(1, (customer_nrows+1))
        storeID = random.randrange(1, (store_nrows+1))
        date = randDate()
        writer.writerow([customerID, storeID, date, 0])


# Generates all the data for all tables
def genAllData():
    genCookies()
    genStores()
    genCustomer()
    genCustomerOrders()
    genOrderDetails()

genAllData()
