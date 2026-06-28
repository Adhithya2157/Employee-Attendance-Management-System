# Employee Attendance Management System

A robust, menu-driven desktop application developed in Python that bridges object-oriented program logic with a relational MySQL database backend to manage and track employee attendance efficiently.

## 🚀 Key Features
- **Secure Admin Authentication:** Features a built-in administrator module supporting login, password recovery, and admin management, with passwords securely protected using SHA-256 cryptographic hashing (`hashlib`).
- **Dynamic Attendance Logging:** Captures and logs employee check-ins dynamically with real-time date and time stamps using Python's `datetime` module.
- **Structured Data Presentation:** Displays attendance and administrative records cleanly on the console terminal utilizing the `tabulate` library.
- **Administrative Flexibility:** Authorized admins can register new administrative accounts or safely remove existing ones.

## 🛠️ System Architecture & Database Design
The application connects to an RDBMS backend consisting of two primary tables:
1. **`admin_users`**: Stores admin credentials (Columns: `id`, `username`, `password_hash`)[cite: 1].
2. **`attendance`**: Tracks employee presence (Columns: `ID`, `Employee_id`, `Name`, `Date`, `Time`, `Status`)[cite: 1].

## 💻 Tech Stack
- **Language:** Python 3.x[cite: 1]
- **Database Backend:** MySQL Server[cite: 1]
- **Core Libraries:** `mysql-connector-python`, `hashlib`, `datetime`, `tabulate`[cite: 1]

## ⚙️ Setup and Installation

### 1. Prerequisites
Ensure you have MySQL Server and Python installed on your local machine[cite: 1]. 

### 2. Configure Database Credentials
Open the `main.py` file and update the following configuration variables to match your local MySQL server credentials[cite: 1]:
```python
DB_USER = "root"          # Replace with your MySQL username
DB_PASSWORD = "12345"     # Replace with your MySQL password
3. Install Dependencies
Install the required Python modules using pip[cite: 1]:

Bash
pip install mysql-connector-python tabulate
4. Run the Application
Execute the primary script to initialize the database tables and launch the menu interface[cite: 1]:

Bash
python main.py
🔒 Default Credentials
For the initial setup and first-time login, use the following default admin credentials[cite: 1]:

Username: admin

[cite: 1]

Password: admin123

[cite: 1]


(Note: Remember to register a custom admin profile and remove the default account for deployment security[cite: 1].)
