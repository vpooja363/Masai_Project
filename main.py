from transaction import (
    create_account,
    login,
    logout,
    deposit,
    withdraw,
    check_balance,
    take_loan,
    repay_loan,
    check_loan_balance,
)

current_user = None  # Tracks the logged-in user


def main():
    global current_user
    while True:
        if current_user:
            print(f"\n=== Welcome, {current_user['name']} ===")
            print("1. Deposit Money")
            print("2. Withdraw Money")
            print("3. Check Balance")
            print("4. Take Loan")
            print("5. Repay Loan")
            print("6. Check Loan Balance")
            print("7. Logout")
        else:
            print("\n=== Banking System ===")
            print("1. Login")
            print("2. Create Account")
            print("3. Exit")

        choice = input("Enter your choice: ")

        if not current_user:
            if choice == "1":
                current_user = login()
            elif choice == "2":
                create_account()
            elif choice == "3":
                print("Thank you for using our banking system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            if choice == "1":
                deposit(current_user['account_number'])
            elif choice == "2":
                withdraw(current_user['account_number'])
            elif choice == "3":
                check_balance(current_user['account_number'])
            elif choice == "4":
                take_loan(current_user['account_number'])
            elif choice == "5":
                repay_loan(current_user['account_number'])
            elif choice == "6":
                check_loan_balance(current_user['account_number'])
            elif choice == "7":
                logout()
                current_user = None
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
