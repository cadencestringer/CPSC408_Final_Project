import sqlite3, datetime
import pandas as pd
import re

conn = sqlite3.connect('./StudentDB.sqlite')#establish connection to the database
mycursor = conn.cursor()

#function that reads in the students csv
def readStudents():
    with open("./students.csv") as inputFile:
        columns = inputFile.readline() #get column names
        data = inputFile.readlines()

    for i in range(len(data)):
        data[i] = data[i].strip().split(',')
        data[i].append("")
        data[i].append("0")

        mycursor.execute("INSERT INTO Student ('FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State',"
                             "'ZipCode', 'MobilePhoneNumber', 'isDeleted') VALUES(?,?,?,?,?,?,?,?,?,?,?);",
                             (data[i][0], data[i][1], data[i][8], data[i][7], data[i][9], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6], data[i][10]))
        conn.commit()
    print("Data from students.csv imported successfully")

#function that adds a new student
def addNewStudent():
    #each input checks to make sure the field is the type it should be
    #stays in a while loop while input is incorrect
    print("Adding new student to the database")
    fName = str(input("Please enter the first name: "))
    while not fName.isalpha():
        print("Only letters allowed!")
        fName = str(input("Please enter the first name: "))
    lName = str(input("Please enter the last name: "))
    while not lName.isalpha():
        print("Only letters allowed!")
        lName = str(input("Please enter the last name: "))
    gpa = str(input("Please enter the GPA: "))
    while True:
        while gpa.isalpha():
            print("GPA must be numeric")
            gpa = str(input("Please enter the GPA: "))
        while (float(gpa) < 0 or float(gpa) > 4):
            print("GPA invalid!")
            print("Please enter a gpa between 0 and 4")
            gpa = str(input("Please enter the GPA of the new student: "))
            while gpa.isalpha():
                print("GPA must be numeric")
                gpa = str(input("Please enter the GPA: "))
        break
    gpa = float(gpa)

    major = str(input("Please enter the major: "))
    while not major.isalpha():
        print("Only letters allowed!")
        major = str(input("Please enter the major: "))
    fAdvisor = str(input("Please enter the faculty advisor: "))
    while not fAdvisor.isalpha():
        print("Only letters allowed!")
        fAdvisor = str(input("Please enter the faculty advisor: "))
    address = str(input("Enter the student's address: "))
    city = str(input("Enter the city: "))
    while not city.isalpha():
        print("Only letters allowed!")
        city = str(input("Enter the city: "))
    state = str(input("Enter the state: "))
    while not state.isalpha():
        print("Only letters allowed!")
        state = str(input("Enter the state: "))
    zipCode = str(input("Enter the zip code: "))
    while not zipCode.isdigit():
        print("Only numbers allowed!")
        zipCode = str(input("Enter the zip code: "))
    #Checks to make sure the phone number is in a correct pattern
    phoneNum = str(input("Enter the student's phone number: "))
    phonePat = "\(\d{3}\)-\d{3}-\d{4}"
    phonePat2 = "\(\d{3}\)-\d{3}-\d{4}x\d"
    while not re.match(phonePat, phoneNum) or re.match(phonePat2, phoneNum) \
            or phoneNum.isalpha() or len(phoneNum) < 14 or len(phoneNum) > 25:
        print("Enter a phone number in the format (XXX)-XXX-XXXX")
        phoneNum = str(input("Enter the student's phone number: "))
    #Executes the insert
    mycursor.execute(
        "INSERT INTO Student ('FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State',"
        "'ZipCode', 'MobilePhoneNumber', 'isDeleted') VALUES(?,?,?,?,?,?,?,?,?,?,?);",
        (fName, lName, gpa, major, fAdvisor, address, city, state, zipCode, phoneNum, 0))
    conn.commit()
    print("Student successfully entered!")

#function to update a student record
def updateStudent():
    mycursor.execute("SELECT COUNT(*) FROM Student;")
    count = mycursor.fetchall()
    #checks to make sure student Id exists
    studId = str(input("Enter the id of the student you wish to update: "))
    while True:
        while studId.isalpha():
            print("Student id must be numeric!")
            studId = str(input("Enter the id of the student you wish to update: "))
        while int(studId) < 1 or int(studId) > count[0][0]:
            print("Student id doesn't exist!")
            studId = str(input("Enter the id of the student you wish to update: "))
            while studId.isalpha():
                print("Student id must be numeric!")
                studId = str(input("Enter the id of the student you wish to update: "))
        break
    studId = int(studId)

    print("Press 1 to update their major")
    print("Press 2 to update their advisor")
    print("Press 3 to update their phone number")
    selection = int(input("Please make a selection: "))


    while selection < 1 or selection > 3:
        print("Invalid selection!")
        selection = int(input("Please make a selection: "))

    if selection == 1:
        major = str(input("Please enter the new major: "))
        while not major.isalpha():
            print("Only letters allowed!")
            major = str(input("Please enter new the major: "))
        mycursor.execute("UPDATE Student SET MAJOR = ? WHERE StudentId = ?;",
                         (major, studId))
        conn.commit()
    elif selection == 2:
        fAdvisor = str(input("Please enter the new faculty advisor: "))
        while not fAdvisor.isalpha():
            print("Only letters allowed!")
            fAdvisor = str(input("Please enter the new faculty advisor: "))
        mycursor.execute("UPDATE Student SET FacultyAdvisor = ? WHERE StudentId = ?;",
                         (fAdvisor, studId))
        conn.commit()
    elif selection == 3:
        phoneNum = str(input("Enter the student's new phone number: "))
        phonePat = "\(\d{3}\)-\d{3}-\d{4}"
        phonePat2 = "\(\d{3}\)-\d{3}-\d{4}x\d"
        while not re.match(phonePat, phoneNum) or re.match(phonePat2, phoneNum) \
                or phoneNum.isalpha() or len(phoneNum) < 14 or len(phoneNum) > 25:
            print("Enter a phone number in the format (XXX)-XXX-XXXX")
            phoneNum = str(input("Enter the student's new phone number: "))
        mycursor.execute("UPDATE Student SET MobilePhoneNumber = ? WHERE StudentId = ?;",
                         (phoneNum, studId))
        conn.commit()
    print("Success!")

#function to set isDeleted = 1
def deleteStudent():
    mycursor.execute("SELECT COUNT(*) FROM Student;")
    count = mycursor.fetchall()
    #Sees if student exists
    studId = str(input("Enter the id of the student you wish to delete: "))
    while True:
        while studId.isalpha():
            print("Student id must be numeric!")
            studId = str(input("Enter the id of the student you wish to delete: "))
        while int(studId) < 1 or int(studId) > count[0][0]:
            print("Student id doesn't exist!")
            studId = str(input("Enter the id of the student you wish to delete: "))
            while studId.isalpha():
                print("Student id must be numeric!")
                studId = str(input("Enter the id of the student you wish to delete: "))
        break
    studId = int(studId)
    mycursor.execute("UPDATE Student SET isDeleted = ? WHERE StudentId = ?;",
                     (1, studId))
    conn.commit()
    print("Success!")

#Searches for student based on 5 criteria
def searchStudent():
    print("")
    print("Type 1 to search for students by Major")
    print("Type 2 to search for students by GPA")
    print("Type 3 to search for students by City")
    print("Type 4 to search for students by State")
    print("Type 5 to search for students by Advisor")
    selection = int(input("Make a selection: "))
    while selection < 1 or selection > 5:
        print("Invalid selection")
        print("")
        print("Type 1 to search for students by Major")
        print("Type 2 to search for students by GPA")
        print("Type 3 to search for students by City")
        print("Type 4 to search for students by State")
        print("Type 5 to search for students by Advisor")
        selection = int(input("Make a selection: "))

    if selection == 1:
        major = str(input("Please enter the major: "))
        while all(not x.isalpha() and not x.isspace() for x in major):
            print("Only letters allowed!")
            major = str(input("Please enter the major: "))
        mycursor.execute("SELECT * FROM Student "
                         "WHERE Major = ?;", (major,))
        print(mycursor.fetchall())

    elif selection == 2:
        gpa = str(input("Please enter the GPA: "))
        while True:
            while gpa.isalpha():
                print("GPA must be numeric")
                gpa = str(input("Please enter the GPA: "))
            while (float(gpa) < 0 or float(gpa) > 4):
                print("GPA invalid!")
                print("Please enter a gpa between 0 and 4")
                gpa = str(input("Please enter the GPA of the new student: "))
                while gpa.isalpha():
                    print("GPA must be numeric")
                    gpa = str(input("Please enter the GPA: "))
            break
        mycursor.execute("SELECT * FROM Student "
                         "WHERE GPA = ?;", (gpa,))
        print(mycursor.fetchall())
    elif selection == 3:
        city = str(input("Enter the city: "))
        while all(not x.isalpha() and not x.isspace() for x in city):
            print("Only letters allowed!")
            city = str(input("Enter the city: "))
        mycursor.execute("SELECT * FROM Student "
                         "WHERE City = ?;", (city,))
        print(mycursor.fetchall())
    elif selection == 4:
        state = str(input("Enter the state: "))
        while all(not x.isalpha() and not x.isspace() for x in state):
            print("Only letters allowed!")
            state = str(input("Enter the state: "))
        mycursor.execute("SELECT * FROM Student "
                         "WHERE State = ?;", (state,))
        print(mycursor.fetchall())
    elif selection == 5:
        fAdvisor = str(input("Please enter the faculty advisor: "))
        while all(not x.isalpha() and not x.isspace() for x in fAdvisor):
            print("Only letters allowed!")
            fAdvisor = str(input("Please enter the faculty advisor: "))
        mycursor.execute("SELECT * FROM Student "
                         "WHERE FacultyAdvisor = ?;", (fAdvisor,))
        print(mycursor.fetchall())

#Menu that repeats until user exits
while True:
    print("")
    print("Type 1 to import data from students.csv")
    print("Type 2 to display all students and their attributes")
    print("Type 3 to add a student to the database")
    print("Type 4 to update a student record")
    print("Type 5 to delete a student record")
    print("Type 6 to search for a student record")
    print("Type 7 to exit")
    option = int(input("Choose an option: "))
    if (option < 1) or (option > 7):
        print("Not a valid selection")
    if (option == 1):
        readStudents()
    elif (option == 2):
        mycursor.execute("SELECT * FROM Student;")
        data = mycursor.fetchall()
        df = pd.DataFrame(data)
        print(df)
    elif (option == 3):
        addNewStudent()
    elif (option == 4):
        updateStudent()
    elif (option == 5):
        deleteStudent()
    elif (option == 6):
        searchStudent()
    elif (option == 7):
        print("Exiting...")
        break
conn.close()