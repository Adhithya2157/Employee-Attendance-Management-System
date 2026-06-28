import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import hashlib
from tabulate import tabulate

#Configuration
DB_NAME = "attendance_db"
DB_USER = "root"      # Replace with your MySQL username
DB_PASSWORD = "12345"  # Replace with your MySQL password
DB_HOST = "localhost"

#Connect to MySQL Server
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD
)
#Create Cursor
cursor = conn.cursor()

#Create Database
def create_database():
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f" Database `{DB_NAME}` is ready.")
    except mysql.connector.Error as err:
        print(f" Failed creating database: {err}")
        exit(1)

create_database()
conn.database = DB_NAME

#Create Tables
TABLES = {
    "admin_users": """
        CREATE TABLE IF NOT EXISTS admin_users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL
        )
    """,
    "attendance": """
        CREATE TABLE IF NOT EXISTS attendance (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            Employee_id VARCHAR(10),
            Name VARCHAR(100),
            Date DATE,
            Time TIME,
            Status VARCHAR(10)
        )
    """
}

for table_name, ddl in TABLES.items():
    try:
        cursor.execute(ddl)
        print(f" Table `{table_name}` is ready.")
    except mysql.connector.Error as err:
        print(f" Error creating table {table_name}: {err}")

#Utilities
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#Default Admin
def ensure_default_admin():
    cursor.execute("SELECT COUNT(*) FROM admin_users")
    count = cursor.fetchone()[0]
    if count == 0:
        username = "admin"
        password = "admin123"
        password_hash = hash_password(password)
        cursor.execute("INSERT INTO admin_users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
        conn.commit()
        print(" Default admin created — Username: admin | Password: admin123")

ensure_default_admin()
#To Remove Admin
def remove_admin(current_username):
    print("\n Remove Admin")
    username_to_remove = input("Enter admin username to remove: ")

    if username_to_remove == current_username:
        print(" You cannot remove yourself.")
        return

    cursor.execute("SELECT COUNT(*) FROM admin_users")
    admin_count = cursor.fetchone()[0]

    if admin_count <= 1:
        print(" Cannot remove the last admin user.")
        return

    cursor.execute("SELECT * FROM admin_users WHERE username = %s", (username_to_remove,))
    if cursor.fetchone():
        confirm = input(f"Are you sure you want to remove '{username_to_remove}'? (yes/no): ").lower()
        if confirm == "yes":
            cursor.execute("DELETE FROM admin_users WHERE username = %s", (username_to_remove,))
            conn.commit()
            print(f" Admin '{username_to_remove}' removed.")
        else:
            print(" Removal cancelled.")
    else:
        print("Admin not found.")


#Admin Login
def login_admin():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    password_hash = hash_password(password)
    cursor.execute("SELECT * FROM admin_users WHERE username = %s AND password_hash = %s", (username, password_hash))
    if cursor.fetchone():
        print(f" Welcome, {username}!")
        return username
    else:
        print(" Invalid login.")
        return None

# Forgot Password
def forgot_password():
    print("\n Forgot Password")
    username = input("Enter your admin username: ")

    cursor.execute("SELECT * FROM admin_users WHERE username = %s", (username,))
    if cursor.fetchone():
        new_password = input("Enter new password: ")
        confirm = input("Confirm new password: ")
        if new_password != confirm:
            print(" Passwords do not match.")
            return
        password_hash = hash_password(new_password)
        cursor.execute("UPDATE admin_users SET password_hash = %s WHERE username = %s", (password_hash, username))
        conn.commit()
        print(" Password updated successfully.")
    else:
        print(" Username not found.")

#Register New Admin
def register_new_admin():
    print("\n Register New Admin")
    username = input("Enter new admin username: ")
    password = input("Enter password: ")
    confirm = input("Confirm password: ")
    
    if password != confirm:
        print("Passwords do not match.")
        return

    password_hash = hash_password(password)
    try:
        cursor.execute("INSERT INTO admin_users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
        conn.commit()
        print(f" Admin '{username}' registered successfully.")
    except mysql.connector.IntegrityError:
        print("Username already exists.")

#To Mark Attendance
def mark_attendance(employee_id, name, status):
    now = datetime.now()
    date = now.date()
    time = now.time()
    cursor.execute(
        "INSERT INTO attendance (Employee_ID, Name, Date, Time, Status) VALUES (%s, %s, %s, %s, %s)",
        (employee_id, name, date, time, status)
    )
    conn.commit()
    print(f" Attendance marked for {name} ({status})")

def view_attendance():
    cursor.execute("SELECT * FROM attendance")
    records = cursor.fetchall()
    if records:
        headers = ["ID", "Emp ID", "Name", "Date", "Time", "Status"]
        print("\n All Attendance Records:\n")
        print(tabulate(records, headers=headers, tablefmt="grid"))
    else:
        print(" No attendance records found.")

def search_attendance(emp_id):
    cursor.execute("SELECT * FROM attendance WHERE employee_id = %s", (emp_id,))
    records = cursor.fetchall()
    if records:
        headers = ["ID", "Emp ID", "Name", "Date", "Time", "Status"]
        print(f"\n Records for Employee ID {emp_id}:\n")
        print(tabulate(records, headers=headers, tablefmt="grid"))
    else:
        print(" No records found.")

#Attendance Menu
def attendance_menu(current_username):
    while True:
        print("\n Attendance Menu")
        print("1. Mark Attendance")
        print("2. View All Records")
        print("3. Search by Employee ID")
        print("4. Register New Admin")
        print("5. Logout")
        print("6. Remove Admin")

        choice = input("Choose option (1-6): ")

        if choice == "1":
            emp_id = input("Employee ID: ")
            name = input("Name: ")
            status = input("Status (Present/Absent): ").capitalize()
            mark_attendance(emp_id, name, status)
        elif choice == "2":
            view_attendance()
        elif choice == "3":
            emp_id = input("Employee ID to search: ")
            search_attendance(emp_id)
        elif choice == "4":
            register_new_admin()
        elif choice == "5":
            print(" Logged out.")
            break
        elif choice == "6":
            remove_admin(current_username)
            break
        else:
             print(" Invalid choice.")
            
#Main Menu
def main():
    while True:
        print("\n ----------------------Employee Attendance Management System-----------------------------")
        print("1. Admin Login")
        print("2. Forgot Password")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")
        

        if choice == "1":
            current_username=login_admin()
            if current_username:
                attendance_menu(current_username)
            
        elif choice == "2":
            forgot_password()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

#Run the Program
if __name__ == "__main__":
    main()
    cursor.close()
    conn.close()
