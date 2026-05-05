import sqlite3
from tabulate import tabulate

conn = sqlite3.connect("Kannur_University.db")
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS Details(
               student_id INTEGER PRIMARY KEY AUTOINCREMENT,
               name VARCHAR(25) UNIQUE,
               course VARCHAR(20),
               email TEXT)
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS User(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(20) UNIQUE ,
            passwordS TEXT ,
            st_id INTEGER,
            role INTEGER,
            FOREIGN KEY(st_id) REFERENCES Details(student_id)             
               )
''')
                    
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Grade(
               st_id INTGER,
               course VARCHAR(20),
               mark INTEGER,
               percentage TEXT,
               elgiblity TEXT,
               FOREIGN KEY(st_id) REFERENCES Details(student_id)
               )

    ''')

# cursor.execute('''
#     INSERT INTO User(username,passwordS,role)
#                VALUES('hod','hod1029',0)

#     ''')

conn.commit()
conn.close()

print("                                                   🏫                                                     ")
print("                                           _______________________                                           ")
print("\n-------------------------------------------|WELCOME TO UNIVERSITY|-------------------------------------------")
print("                                           _______________________                                           ")

def login():
    while True:
        conn = sqlite3.connect("Kannur_University.db")
        cursor = conn.cursor()
        print("\n-------------------------------------------LOGIN PAGE-------------------------------------------")
        username = input("enter your user name:--")
        password = input("enter your password:--")
        cursor.execute('''
        SELECT * FROM User WHERE username = ? AND passwordS = ?
                                                                                        
        ''',(username,password))                                                    # LOGIN FOR HOD/TEACHER/STUDENT
        user = cursor.fetchone()
        if user:
            print("\n-------|LOGIN SUCCESFULL|--------")
            return user
        else:
            print("Invalid user❗❗ \n TRY AGAIN")

def add_hod():
    conn = sqlite3.connect("Kannur_University.db")
    cursor = conn.cursor()
    print("\n-------------------------------------------ADD HOD-------------------------------------------")   
    username = input("enter hod name:--")
    password = input("enter a password for hod:--")
    try:
        cursor.execute('''
        INSERT INTO Users(username,passwordS,role)
                    VALUES(?,?,0)
        '''(username,password))
        conn.commit()
        print("-----------HOD ADDED SUCCSFULL------------")
    except sqlite3.IntegrityError:
        print("user name already exist\n TRY AGAIN")
    finally:
        conn.close()

def add_teacher():
    conn = sqlite3.connect("Kannur_University.db")
    cursor = conn.cursor()
    print("\n-------------------------------------------ADD TEACHER-------------------------------------------")
    username = input("enter teacher name:--")
    password = input("enter the password:--")
    try:                                     # ADD TEACHER
        cursor.execute('''
        INSERT INTO User(username,passwordS,role)
                    VALUES(?,?,1)
        ''',(username,password))
        print("\n----------|ADDED TEACHER SUCCESFULLY|-----------")
        conn.commit()
    except sqlite3.IntegrityError:
        print("user name is already exists\n TRY AGIN")
    finally:
        conn.close()

def add_student():
    conn = sqlite3.connect("Kannur_University.db")
    cursor = conn.cursor()
    print("\n-------------------------------------------ADD STUDENT-------------------------------------------")
    username = input("enter the student name:--")
    print("Select the course ")
    ch = int(input("1.MBA\n2.BCom\n3.BBA\n4.MA\n5.BSc\n6.BA\n:--"))
    course = ""
    if ch == 1:
        course = "MBA"
    elif ch == 2:
        course = "BCom"
    elif ch == 3:
        course = "BBA"
    elif ch == 4:
        course = "MA"                                                              # ADD STUDENTS
    elif ch == 5:
        course = "BSc"
    elif ch == 6:
        course = "BA"
    else:
        print("invalid option❗❗\n TRY AGAIN ")
        return add_student()
    email = input('enter student email id:--')
    password = input("enter a new password:--")
    cursor.execute('''
    INSERT INTO Details(name,course,email)
                   VALUES(?,?,?)
    ''',(username,course,email))
    studentid = cursor.lastrowid
    cursor.execute('''
    INSERT INTO User(username,passwordS,st_id,role)
                   VALUES(?,?,?,2)
    ''',(username,password,studentid))
    print("\n--------|ADDED STUDENT SUCCESFULLY|---------")
    conn.commit()
    conn.close()

def view_student():
    conn = sqlite3.connect("Kannur_University.db")
    cursor = conn.cursor()
    print("\n-------------------------------------------VIEW STUDENT-------------------------------------------")
    while True:
        ch = int(input("1.view all student detail\n2.view single student detail\n3.exit\n:---"))
        if ch == 1:
            cursor.execute('''
            SELECT * FROM DETAILS 
        ''')                                                                                                # VIEW STUDENTS DETAIL FOR HOD
            all_detail = cursor.fetchall()
            headers = ["student_id","name","course","email"]
            print(tabulate(all_detail, headers=headers, tablefmt="grid"))
            # for i in all_detail:
            #     print(i)
        elif ch == 2:
            id = int(input("enter the student id to veiw the details:--"))
            cursor.execute('''
            SELECT * FROM Details WHERE student_id = ?
            ''',(id,)) 
            single_detail = cursor.fetchall()
            print(tabulate(single_detail,headers=headers,tablefmt="grid"))
            # for i in single_detail:
            #     print(i) 
        elif ch == 3:
            break
        else:
            print("ivalid option❗❗\ntry again")

def view_student1(st_id):
    conn = sqlite3.connect("Kannur_University.db")
    cursor = conn.cursor()  
    print("\n-------------------------------------------DETAILS-------------------------------------------")     
    cursor.execute('''
            SELECT * FROM Details WHERE student_id = ?
        ''',(st_id,))                                                       #VIEW STUDENT FOR STUDENTS
    all_detail = cursor.fetchall()
    headers = ["student_id","name","course","email"]
    print(tabulate(all_detail, headers=headers, tablefmt="grid"))
    # for i in all_detail:
    #     for j in i:
    #         print("  ",j)

def delete_student():
    conn = sqlite3.connect("kannur_University.db")
    cursor = conn.cursor()
    print("\n-------------------------------------------DELETE STUDENT-------------------------------------------")
    id = int(input("enter the student id that want to delete:--"))
    ch = input("if you really want to delete \n type yes / no\n:--")
    if ch == "yes":
        cursor.execute('''
        DELETE  FROM Details WHERE student_id = ?
    ''',(id,))                                                                  # DELETE STUDENT
        cursor.execute('''
        DELETE FROM User WHERE st_id = ?
        ''',(id,))
        cursor.execute('''
        DELETE FROM Grade WHERE st_id = ?
        ''',(id,))
        print("\n-------|DELETED SUCCESFULLY|--------")
    else:
        print("student not deleted")
    conn.commit()
    conn.close()

def add_grade():
    conn = sqlite3.connect("Kannur_University.db")
    cursor = conn.cursor()
    print("\n-------------------------------------------ADD GRADE-------------------------------------------")
    studentid = int(input("enter your student id:--"))
    cursor.execute('''
        SELECT course FROM Details WHERE student_id = ?
    ''',(studentid,))
    student = cursor.fetchone()                                                         #ADD GRADES
    course = student[0]
    mark = float(input("enter student mark out of 100:--"))
    percentage = f"{mark}%"
    if mark >=40:
        eligiblity = "pass"
    else:
        eligiblity = "fail"

    cursor.execute('''
    INSERT INTO Grade(st_id,course,mark,percentage,elgiblity)
                   VALUES(?,?,?,?,?)
    ''',(studentid,course,mark,percentage,eligiblity))
    print("\n--------|GRADE ADDED SUCCESFULL|-------")
    conn.commit()
    conn.close()


def view_grade(st_id):
    conn = sqlite3.connect("kannur_University.db")
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM Grade WHERE st_id = ?
    ''',(st_id,))                                                         #VIEW GRADES
    student = cursor.fetchall()
    headers = ["st_id","course","mark","percentage","eligibility"]
    print(tabulate(student, headers=headers, tablefmt="grid"))
    # for i in student:
    #     for j in i:
    #         print(j)

def view_all_grades():
    conn = sqlite3.connect("kannur_University.db")
    cursor = conn.cursor()
    print("-----------STUDENTS GRADES-------------")
    cursor.execute('''
    SELECT * FROM Grade
    ''')
    details = cursor.fetchall()                                         #VIEW ALL GRADES
    headers = ["st_id","course","mark","percentage","eligibility"]
    print(tabulate(details, headers=headers, tablefmt="grid"))
    # for i in details:
    #     print(i)
    conn.close()

def update_student(st_id):
    conn = sqlite3.connect("kannur_University.db")
    cursor = conn.cursor()
    name = input("Update your name:--")
    email = input("Update your email:--")
    cursor.execute('''
    UPDATE Details SET name = ?, email = ? WHERE student_id = ?
    ''',(name,email,st_id))                                             #UPDATE STUDENTS
    print("------------|UPDATED SUCCESFULL|-----------")
    conn.commit()
    conn.close()

def hod_dashbord():
    while True:
        print("\n----------------welcome HOD-----------------------")
        ch = int(input("1.add hod\n2.add teacher\n3.add student\n4.veiw student\n5.veiw grades\n6.delete student\n7.exit\nenter your choice:--"))
        if ch == 1:
            add_hod()
        elif ch == 2:
            add_teacher()
        elif ch == 3:
            add_student()                                              #HOD DASHBOARD
        elif ch == 4:
            view_student()
        elif ch == 5:
            view_all_grades()
        elif ch == 6:
            delete_student()
        elif ch == 7:
            print("\nTHANK YOU")
            break
        else:
            print("invalid option❗❗\nTRY AGAIN")


def teacher_dashboard():
    while True:
        print("--------WELCOME TEACHER--------")
        ch = int(input("1.add student\n2.view student\n3.add gradess\n4.view grades\n5.delete student\n6.exist\nenter your choice:--"))
        if ch == 1:
            add_student()
        elif ch == 2:
            view_student()
        elif ch == 3:
            add_grade()                                         #TEACHER DASHBOARD
        elif ch == 4:
            view_all_grades()
        elif ch == 5:
            delete_student()
        elif ch == 6:
            print("\nTHANK YOU")
            break
        else:
            print("invalid option❗❗\nTRY AGAIN")


def student_dashboard(st_id):
    while True:
        print("--------WELCOME STUDENT---------")
        ch = int(input("1.view student\n2.view grade\n3.update your details\n4.exit\nEnter your choice:--"))
        if ch == 1:
            view_student1(st_id)
        elif ch == 2:
            view_grade(st_id)                                       #STUDENT DASHBOARD
        elif ch == 3:
            update_student(st_id)
        elif ch == 4:
            print("\nTHANK YOU")
            break
        else:
            print("invalid choice❗❗\nTRY AGAIN")
      

def main():
    while True:
        user = login()
        if user:
            role = user[4]
            st_id = user[3]
        if role == 0:
            hod_dashbord()
        elif role == 1:
            teacher_dashboard()
        elif role == 2:
            student_dashboard(st_id)
        else:
             print("NO USER FOUND❗❗ \n TRY AGAIN")


main()