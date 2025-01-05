import os
import random
import hashlib

ACCOUNTS_FILE = "account.txt"


def hash_password(password):
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def generate_account_number():
    """Generates a random 10-digit account number."""
    return str(random.randint(1000000000, 9999999999))


def create_account():
    """Creates a new account with a random account number, username, password, and initial deposit."""
    name = input("Enter your name: ")
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    initial_deposit = input("Enter initial deposit amount: ")
    password_hash = hash_password(password)

    # Generate a unique account number
    while True:
        account_number = generate_account_number()
        if os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, "r") as file:
                accounts = file.readlines()
                if any(account_number in account for account in accounts):
                    continue
        break

    with open(ACCOUNTS_FILE, "a") as file:
        file.write(f"{account_number},{name},{username},{password_hash},{initial_deposit},0\n")
    print(f"Account created successfully! Your account number is {account_number}")


def login():
    """Logs in the user using username and password."""
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    password_hash = hash_password(password)

    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as file:
            accounts = file.readlines()
            for account in accounts:
                # Skip empty or malformed lines
                account_data = account.strip().split(",")
                if len(account_data) != 6:
                    continue
                
                acc_num, name, user, stored_password, balance, loan_balance = account_data
                if username == user and password_hash == stored_password:
                    print(f"Login successful! Welcome, {name}.")
                    return {"account_number": acc_num, "name": name, "balance": balance, "loan_balance": loan_balance}
    print("Invalid username or password.")
    return None


def logout():
    """Logs out the current user."""
    print("You have been logged out.")


def deposit(account_number):
    """Deposits money into the user's account."""
    amount = input("Enter amount to deposit: ")

    if not amount.isdigit() or float(amount) <= 0:
        print("Invalid deposit amount. Please enter a positive number.")
        return

    updated = False
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as file:
            accounts = file.readlines()

        with open(ACCOUNTS_FILE, "w") as file:
            for account in accounts:
                account_data = account.strip().split(",")
                
                # Skip malformed or empty lines
                if len(account_data) != 6:
                    file.write(account)
                    continue

                acc_num, name, user, password, balance, loan_balance = account_data
                if acc_num == account_number:
                    balance = str(float(balance) + float(amount))
                    print(f"Deposited {amount}. New balance is {balance}.")
                    updated = True
                file.write(f"{acc_num},{name},{user},{password},{balance},{loan_balance}\n")

    if not updated:
        print("Account not found.")



def withdraw(account_number):
    """Withdraws money from the user's account."""
    amount = input("Enter amount to withdraw: ")

    updated = False
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as file:
            accounts = file.readlines()

        with open(ACCOUNTS_FILE, "w") as file:
            for account in accounts:
                acc_num, name, user, password, balance, loan_balance = account.strip().split(",")
                if acc_num == account_number:
                    if float(balance) >= float(amount):
                        balance = str(float(balance) - float(amount))
                        print(f"Withdrawn {amount}. New balance is {balance}.")
                        updated = True
                    else:
                        print("Insufficient balance.")
                file.write(f"{acc_num},{name},{user},{password},{balance},{loan_balance}\n")

    if not updated:
        print("Account not found.")


def check_balance(account_number):
    """Checks the balance of the user's account."""
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as file:
            accounts = file.readlines()
            for account in accounts:
                acc_num, name, user, password, balance, loan_balance = account.strip().split(",")
                if acc_num == account_number:
                    print(f"Account Holder: {name}")
                    print(f"Balance: {balance}")
                    return

    print("Account not found.")


def take_loan(account_number):
    """Allows the user to take a loan."""
    loan_amount = input("Enter the loan amount: ")
    if not loan_amount.isdigit() or float(loan_amount) <= 0:
        print("Invalid loan amount. Please enter a positive number.")
        return

    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as file:
            accounts = file.readlines()

        with open(ACCOUNTS_FILE, "w") as file:
            for account in accounts:
                acc_num, name, user, password, balance, loan_balance = account.strip().split(",")
                if acc_num == account_number:
                    loan_balance = str(float(loan_balance) + float(loan_amount))
                    print(f"Loan of {loan_amount} approved. Your new loan balance is {loan_balance}.")
                file.write(f"{acc_num},{name},{user},{password},{balance},{loan_balance}\n")
    else:
        print("Account not found.")


def repay_loan(account_number):
    """Allows the user to repay a loan."""
    repayment_amount = input("Enter the amount to repay: ")
    if not repayment_amount.isdigit() or float(repayment_amount) <= 0:
        print("Invalid repayment amount. Please enter a positive number.")
        return

    updated = False
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as file:
            accounts = file.readlines()

        with open(ACCOUNTS_FILE, "w") as file:
            for account in accounts:
                acc_num, name, user, password, balance, loan_balance = account.strip().split(",")
                if acc_num == account_number:
                    if float(repayment_amount) > float(loan_balance):
                        print("Repayment amount exceeds loan balance. Repaying full loan.")
                        repayment_amount = loan_balance
                    loan_balance = str(float(loan_balance) - float(repayment_amount))
                    print(f"Repayment successful. Remaining loan balance is {loan_balance}.")
                    updated = True
                file.write(f"{acc_num},{name},{user},{password},{balance},{loan_balance}\n")

    if not updated:
        print("Account not found.")


def check_loan_balance(account_number):
    """Checks the user's loan balance."""
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as file:
            accounts = file.readlines()
            for account in accounts:
                acc_num, name, user, password, balance, loan_balance = account.strip().split(",")
                if acc_num == account_number:
                    print(f"Loan balance for {name}: {loan_balance}")
                    return

    print("Account not found.")
