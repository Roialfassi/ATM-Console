import json
import os


class Customer:
    def __init__(self, account_number, password, balance):
        self.account_number = account_number
        self.password = password
        self.balance = float(balance)

    def check_balance(self):
        return f"Your current balance is: ${self.balance:.2f}"

    def withdraw(self, amount):
        if amount <= 0:
            return "Invalid amount. Please enter a positive number."
        if amount > self.balance:
            return "Insufficient funds."
        self.balance -= amount
        return f"Withdrawal successful. New balance: ${self.balance:.2f}"

    def deposit(self, amount):
        if amount <= 0:
            return "Invalid amount. Please enter a positive number."
        self.balance += amount
        return f"Deposit successful. New balance: ${self.balance:.2f}"

    def change_password(self, old_password, new_password):
        if self.password != old_password:
            return "Incorrect password."
        self.password = new_password
        return "Password changed successfully."


class ATM:
    DATA_FILE = "customers.json"

    def __init__(self):
        self.customers = {}
        self.load_customers()

    def load_customers(self):
        """Loads customers from a file, or generates a new file if not found."""
        if not os.path.exists(self.DATA_FILE):
            self.generate_sample_accounts()
        with open(self.DATA_FILE, "r") as file:
            data = json.load(file)
            self.customers = {acc: Customer(acc, info["password"], info["balance"]) for acc, info in data.items()}

    def save_customers(self):
        """Saves updated customer data to the file."""
        with open(self.DATA_FILE, "w") as file:
            data = {acc: {"password": cust.password, "balance": cust.balance} for acc, cust in self.customers.items()}
            json.dump(data, file, indent=4)

    def authenticate_user(self):
        """Handles user authentication."""
        while True:
            account_number = input("Enter your account number (or -1 to exit): ").strip()
            if account_number == "-1":
                print("Exiting ATM...")
                self.save_customers()
                exit()
            if account_number in self.customers:
                password = input("Enter your password: ").strip()
                if self.customers[account_number].password == password:
                    print("Login successful!\n")
                    return self.customers[account_number]
                else:
                    print("Incorrect password. Try again.")
            else:
                print("Account not found. Try again.")

    def menu(self, customer):
        """Displays the menu and handles operations."""
        while True:
            print("ATM Menu:")
            print("1. Check Balance")
            print("2. Withdraw Cash")
            print("3. Deposit Cash")
            print("4. Change Password")

            choice = input("Choose an option: ").strip()
            if choice == "1":
                print(customer.check_balance())
            elif choice == "2":
                amount = self.get_valid_amount("Enter amount to withdraw: ")
                print(customer.withdraw(amount))
            elif choice == "3":
                amount = self.get_valid_amount("Enter amount to deposit: ")
                print(customer.deposit(amount))
            elif choice == "4":
                old_password = input("Enter your current password: ").strip()
                new_password = input("Enter your new password: ").strip()
                print(customer.change_password(old_password, new_password))
            else:
                print("Invalid choice. Please select a valid option.")
            break

    def get_valid_amount(self, prompt):
        """Ensures valid numeric input for monetary transactions."""
        while True:
            try:
                amount = float(input(prompt).strip())
                if amount <= 0:
                    print("Please enter a positive amount.")
                    continue
                return amount
            except ValueError:
                print("Invalid input. Please enter a numerical value.")

    def run(self):
        """Runs the ATM application."""
        while True:
            customer = self.authenticate_user()
            self.menu(customer)

    def generate_sample_accounts(self):
        """Generates a file with 10 sample customer accounts."""
        sample_data = {
            "1001": {"password": "DekelVaknin1", "balance": 5000.00},
            "1002": {"password": "AviBitter456", "balance": 2500.50},
            "1003": {"password": "password111", "balance": -200.00},
            "1004": {"password": "hello123", "balance": 15000.75},
            "1005": {"password": "bank321", "balance": 100.00},
            "1006": {"password": "rabbi770", "balance": 750.25},
            "1007": {"password": "secure999", "balance": -500.00},
            "1008": {"password": "easymoney23", "balance": 2200.00},
            "1009": {"password": "lukaLebron123", "balance": 0.00},
            "1010": {"password": "MessiRonaldo710", "balance": 9800.00},
        }
        with open(self.DATA_FILE, "w") as file:
            json.dump(sample_data, file, indent=4)
        print("Sample accounts created.")


if __name__ == "__main__":
    atm = ATM()
    atm.run()
