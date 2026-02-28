import sqlite3
import datetime

# ----------------------------
# Connect Database
# ----------------------------
conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

# Create Accounts Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts(
    acc_no INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    pin TEXT,
    balance REAL DEFAULT 0
)
""")

# Create Transactions Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    acc_no INTEGER,
    type TEXT,
    amount REAL,
    date TEXT
)
""")

conn.commit()

# ----------------------------
# Create Account
# ----------------------------
def create_account():
    name = input("Enter Name: ")
    pin = input("Create 4-digit PIN: ")

    cursor.execute(
        "INSERT INTO accounts(name,pin,balance) VALUES(?,?,?)",
        (name, pin, 0)
    )
    conn.commit()

    print("Account Created Successfully!")
    print("Your Account Number:", cursor.lastrowid)


# ----------------------------
# Login
# ----------------------------
def login():
    acc_no = input("Enter Account Number: ")
    pin = input("Enter PIN: ")

    cursor.execute(
        "SELECT * FROM accounts WHERE acc_no=? AND pin=?",
        (acc_no, pin)
    )

    user = cursor.fetchone()

    if user:
        print("Login Successful!")
        user_menu(acc_no)
    else:
        print("Invalid Account Number or PIN")


# ----------------------------
# Deposit
# ----------------------------
def deposit(acc_no):
    amount = float(input("Enter Amount to Deposit: "))

    cursor.execute(
        "UPDATE accounts SET balance = balance + ? WHERE acc_no=?",
        (amount, acc_no)
    )

    cursor.execute(
        "INSERT INTO transactions(acc_no,type,amount,date) VALUES(?,?,?,?)",
        (acc_no, "Deposit", amount, str(datetime.datetime.now()))
    )

    conn.commit()
    print("Deposit Successful!")


# ----------------------------
# Withdraw
# ----------------------------
def withdraw(acc_no):
    amount = float(input("Enter Amount to Withdraw: "))

    cursor.execute(
        "SELECT balance FROM accounts WHERE acc_no=?",
        (acc_no,)
    )
    balance = cursor.fetchone()[0]

    if balance >= amount:
        cursor.execute(
            "UPDATE accounts SET balance = balance - ? WHERE acc_no=?",
            (amount, acc_no)
        )

        cursor.execute(
            "INSERT INTO transactions(acc_no,type,amount,date) VALUES(?,?,?,?)",
            (acc_no, "Withdraw", amount, str(datetime.datetime.now()))
        )

        conn.commit()
        print("Withdraw Successful!")
    else:
        print("Insufficient Balance!")


# ----------------------------
# Check Balance
# ----------------------------
def check_balance(acc_no):
    cursor.execute(
        "SELECT balance FROM accounts WHERE acc_no=?",
        (acc_no,)
    )
    balance = cursor.fetchone()[0]
    print("Current Balance:", balance)


# ----------------------------
# Transaction History
# ----------------------------
def transaction_history(acc_no):
    cursor.execute(
        "SELECT type, amount, date FROM transactions WHERE acc_no=?",
        (acc_no,)
    )

    records = cursor.fetchall()

    print("\n--- Transaction History ---")
    for record in records:
        print(record)


# ----------------------------
# User Menu
# ----------------------------
def user_menu(acc_no):
    while True:
        print("\n1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. Logout")

        choice = input("Choose option: ")

        if choice == "1":
            deposit(acc_no)
        elif choice == "2":
            withdraw(acc_no)
        elif choice == "3":
            check_balance(acc_no)
        elif choice == "4":
            transaction_history(acc_no)
        elif choice == "5":
            break
        else:
            print("Invalid Choice")


# ----------------------------
# Main Menu
# ----------------------------
while True:
    print("\n=== BANK SYSTEM ===")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")

    option = input("Choose option: ")

    if option == "1":
        create_account()
    elif option == "2":
        login()
    elif option == "3":
        break
    else:
        print("Invalid Option")

conn.close()
