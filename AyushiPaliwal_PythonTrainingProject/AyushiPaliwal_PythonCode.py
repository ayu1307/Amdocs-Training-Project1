import mysql.connector
import getpass  # for hidden password input
from datetime import datetime

# Database connection
dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="emp",
    auth_plugin='mysql_native_password'
)

# Creating a cursor object
cursorObject = dataBase.cursor()


# Register a new user
def register_user():
    username = input("Enter a username for registration: ")
    userpassword = input("Enter a password: ")
    repassword = input("Re-enter the password: ")

    if userpassword != repassword:
        print("Error: Passwords do not match. Please try again.")
        return  # Early return to ask for inputs again

    phone = int(input("Enter your phone number: "))
    email = input("Enter your email address: ")
    location = input("Enter your location: ")
    department = input("Enter your department: ")

    sql = "INSERT INTO User1 (username, userpassword, phone, email, location, department) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (username, userpassword, phone, email, location, department)

    try:
        cursorObject.execute(sql, val)
        dataBase.commit()
        print("Registration successful! Please log in.\n")
    except mysql.connector.Error as err:
        print("Error:", err)
        print("Registration failed. Please try with a different username.\n")


# User login
def login_user():
    while True:
        username = input("Enter your username: ")
        userpassword = input("Enter your password: ")

        sql = "SELECT * FROM User1 WHERE username = %s AND userpassword = %s"
        val = (username, userpassword)

        cursorObject.execute(sql, val)
        result = cursorObject.fetchone()

        if result:
            print("Login successful!\n")
            return True
        else:            print("Invalid credentials. Please try again.\n")


# Employee management functions
def add_employee():
    emp_id = input("Enter Employee ID: ")
    name = input("Enter Employee Name: ")
    email = input("Enter Employee Email: ")
    phone = int(input("Enter Employee Phone: "))
    salary = float(input("Enter Employee Salary: "))
    designation = input("Enter Employee Designation: ")
    location = input("Enter Employee Location: ")
    department = input("Enter Employee Department: ")
    hiredate = input("Enter Employee Hire Date (YYYY-MM-DD): ")
    gender = input("Enter Employee Gender: ")

    sql = """INSERT INTO Employee1 (empid, name, email, phone, salary, designation, location, department, hiredate, gender) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    val = (emp_id, name, email, phone, salary, designation, location, department, hiredate, gender)

    cursorObject.execute(sql, val)
    dataBase.commit()
    print("Employee details added successfully.\n")


def update_employee():
    emp_id = input("Enter Employee ID to update: ")
    name = input("Enter new Employee Name: ")
    email = input("Enter new Employee Email: ")
    phone = int(input("Enter new Employee Phone: "))
    salary = float(input("Enter new Employee Salary: "))
    designation = input("Enter new Employee Designation: ")
    location = input("Enter new Employee Location: ")
    department = input("Enter new Employee Department: ")
    hiredate = input("Enter new Employee Hire Date (YYYY-MM-DD): ")
    gender = input("Enter new Employee Gender: ")

    sql = """UPDATE Employee1 
             SET name = %s, email = %s, phone = %s, salary = %s, designation = %s, location = %s, department = %s, hiredate = %s, gender = %s 
             WHERE empid = %s"""
    val = (name, email, phone, salary, designation, location, department, hiredate, gender, emp_id)

    cursorObject.execute(sql, val)
    dataBase.commit()
    print("Employee details updated successfully.\n")


def delete_employee():
    emp_id = input("Enter Employee ID to delete: ")
    sql = "DELETE FROM Employee1 WHERE empid = %s"
    val = (emp_id,)
    cursorObject.execute(sql, val)
    dataBase.commit()
    print("Employee details deleted successfully.\n")


def view_employees():
    query = "SELECT * FROM Employee1"
    cursorObject.execute(query)
    myresult = cursorObject.fetchall()
    print("Employee Records:")
    for record in myresult:
        print(record)
    print()


def search_employee():
    search_term = input("Enter name, email, designation, or department to search: ")
    sql = """SELECT * FROM Employee1 
             WHERE name LIKE %s OR email LIKE %s OR designation LIKE %s OR department LIKE %s"""
    val = ('%' + search_term + '%',) * 4
    cursorObject.execute(sql, val)
    myresult = cursorObject.fetchall()

    if myresult:
        print("Search Results:")
        for record in myresult:
            print(record)
    else:
        print("No results found.")
    print()


def filter_by_salary():
    min_salary = float(input("Enter minimum salary: "))
    max_salary = float(input("Enter maximum salary: "))
    sql = "SELECT * FROM Employee1 WHERE salary BETWEEN %s AND %s"
    val = (min_salary, max_salary)
    cursorObject.execute(sql, val)
    myresult = cursorObject.fetchall()

    if myresult:
        print("Employees within salary range:")
        for record in myresult:
            print(record)
    else:
        print("No employees found in this salary range.")
    print()


def sort_employees():
    sort_field = input("Enter field to sort by (empid, name, salary, hiredate): ")
    sql = f"SELECT * FROM Employee1 ORDER BY {sort_field}"
    cursorObject.execute(sql)
    myresult = cursorObject.fetchall()

    print(f"Employees sorted by {sort_field}:")
    for record in myresult:
        print(record)
    print()


def view_employee_details():
    emp_id = input("Enter Employee ID to view details: ")
    sql = "SELECT * FROM Employee1 WHERE empid = %s"
    val = (emp_id,)
    cursorObject.execute(sql, val)
    result = cursorObject.fetchone()

    if result:
        print("Employee Details:")
        print(result)
    else:
        print("Employee not found.")
    print()


def department_summary():
    sql = """SELECT department, COUNT(*) AS employee_count FROM Employee1 GROUP BY department"""
    cursorObject.execute(sql)
    myresult = cursorObject.fetchall()

    print("Employee Count by Department:")
    for record in myresult:
        print(f"Department: {record[0]}, Count: {record[1]}")
    print()


def calculate_tenure():
    emp_id = input("Enter Employee ID to calculate tenure: ")
    sql = "SELECT hiredate FROM Employee1 WHERE empid = %s"
    val = (emp_id,)
    cursorObject.execute(sql, val)
    result = cursorObject.fetchone()

    if result:
        hiredate = result[0]
        tenure = (datetime.now().date() - hiredate).days // 365
        print(f"Employee Tenure: {tenure} years")
    else:
        print("Employee not found.")
    print()


def salary_distribution():
    emp_id = input("Enter Employee ID to view salary distribution: ")
    sql = "SELECT salary FROM Employee1 WHERE empid = %s"
    val = (emp_id,)
    cursorObject.execute(sql, val)
    result = cursorObject.fetchone()

    if result:
        total_salary = float(result[0])  # Convert to float
        base_salary = total_salary * 0.40
        pf = total_salary * 0.24
        hra = base_salary  # HRA is 100% of basic salary
        income_tax = base_salary * 0.0833  # 8.33% of Base Salary

        print(f"Salary Distribution for Employee ID {emp_id}:")
        print(f"Total Salary: {total_salary:.2f}")
        print(f"Base Salary: {base_salary:.2f}")
        print(f"Provident Fund (PF): {pf:.2f}")
        print(f"HRA: {hra:.2f}")
        print(f"Income Tax: {income_tax:.2f}")
    else:
        print("Employee not found.")
    print()

# Main program loop
def main():
    while True:
        print("Welcome to the Employee Management System")
        print("1. Register")
        print("2. Login")
        choice = input("Enter your choice: ")

        if choice == '1':
            register_user()
        elif choice == '2':
            if login_user():
                break  # Exit loop after successful login
            else:
                print("Login unsuccessful. Please try again.\n")
        else:
            print("Invalid choice. Please select either 1 or 2.\n")

    # Employee management options
    while True:
        print("Employee Management System")
        print("1. Add Employee")
        print("2. Update Employee")
        print("3. Delete Employee")
        print("4. View Employees")
        print("5. Search Employee")
        print("6. Filter by Salary")
        print("7. Sort Employees")
        print("8. View Employee Details by ID")
        print("9. Department Summary")
        print("10. Calculate Tenure")
        print("11. View Salary Distribution")
        print("12. Exit")

        choice = input("Please enter your choice: ")

        if choice == '1':
            add_employee()
        elif choice == '2':
            update_employee()
        elif choice == '3':
            delete_employee()
        elif choice == '4':
            view_employees()
        elif choice == '5':
            search_employee()
        elif choice == '6':
            filter_by_salary()
        elif choice == '7':
            sort_employees()
        elif choice == '8':
            view_employee_details()
        elif choice == '9':
            department_summary()
        elif choice == '10':
            calculate_tenure()
        elif choice == '11':
            salary_distribution()
        elif choice == '12':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

    # Closing database connection
    dataBase.close()


if __name__ == "__main__":
    main()
