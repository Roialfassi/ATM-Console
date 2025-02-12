from __future__ import annotations
import json
import os
from typing import Dict, Optional
from customer_model import Customer


class ATM:
    def __init__(self, data_path="customers.json") -> None:
        self.customers: Dict[str, Customer] = {}
        self.data_path = data_path
        self.load_customers()

    def load_customers(self) -> None:
        """Load customers from file or generate sample accounts if file not found."""
        if not os.path.exists(self.data_path):
            self.generate_sample_accounts()

        try:
            with open(self.data_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.customers = {
                    acc: Customer(
                        account_number=acc,
                        password_hash=info["password_hash"],
                        salt=info["salt"],
                        balance=float(info["balance"])
                    )
                    for acc, info in data.items()
                }
        except (json.JSONDecodeError, KeyError) as e:
            raise RuntimeError(f"Error loading customer data: {e}")

    def save_customers(self) -> None:
        """Save customer data to file."""
        data = {
            acc: {
                "password_hash": cust.password_hash,
                "salt": cust.salt,
                "balance": float(cust.balance)
            }
            for acc, cust in self.customers.items()
        }
        try:
            with open(self.data_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except IOError as e:
            raise RuntimeError(f"Error saving customer data: {e}")

    def authenticate_user(self) -> Optional[Customer]:
        """Handle user authentication."""
        while True:
            account_number = input("Enter your account number (or -1 to exit): ").strip()
            if account_number == "-1":
                print("Exiting ATM...")
                self.save_customers()
                return None

            customer = self.customers.get(account_number)
            if not customer:
                print("Account not found. Try again.")
                continue

            password = input("Enter your password: ").strip()
            if customer.verify_password(password):
                print("Login successful!\n")
                return customer
            print("Incorrect password. Try again.")

    def get_valid_amount(self, prompt: str) -> float:
        """Get valid monetary amount from user input."""
        while True:
            try:
                amount = float(input(prompt).strip())
                if amount <= 0:
                    print("Please enter a positive amount.")
                    continue
                return amount
            except ValueError:
                print("Invalid input. Please enter a numerical value.")

    def menu(self, customer: Customer) -> None:
        """Display menu and handle operations."""
        options = {
            "1": ("Check Balance", lambda: print(customer.check_balance())),
            "2": ("Withdraw Cash", lambda: print(customer.withdraw(
                self.get_valid_amount("Enter amount to withdraw: ")))),
            "3": ("Deposit Cash", lambda: print(customer.deposit(
                self.get_valid_amount("Enter amount to deposit: ")))),
            "4": ("Change Password", lambda: self._handle_password_change(customer))
        }

        print("\nATM Menu:")
        for key, (option_name, _) in options.items():
            print(f"{key}. {option_name}")

        choice = input("Choose an option: ").strip()
        if action := options.get(choice):
            action[1]()
        else:
            print("Invalid choice. Please select a valid option.")

    def _handle_password_change(self, customer: Customer) -> None:
        """Handle password change operation."""
        old_password = input("Enter your current password: ").strip()
        new_password = input("Enter your new password: ").strip()
        print(customer.change_password(old_password, new_password))

    def run(self) -> None:
        """Run the ATM application."""
        while True:
            customer = self.authenticate_user()
            if not customer:
                break
            self.menu(customer)

    def generate_sample_accounts(self) -> None:
        """Generate sample customer accounts."""
        sample_accounts = [
            ("1001", "DekelVaknin1", 5000.00),
            ("1002", "AviBitter456", 2500.50),
            ("1003", "password111", -200.00),
            ("1004", "hello123", 15000.75),
            ("1005", "bank321", 100.00)
        ]

        self.customers = {
            acc_num: Customer.create(acc_num, password, balance)
            for acc_num, password, balance in sample_accounts
        }
        self.save_customers()
        print("Sample accounts created.")
