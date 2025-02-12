from __future__ import annotations
from dataclasses import dataclass
import hashlib
import secrets


@dataclass
class Customer:
    account_number: str
    password_hash: str
    salt: str
    balance: float

    @classmethod
    def create(cls, account_number: str, password: str, balance: float) -> Customer:
        salt = secrets.token_hex(16)
        password_hash = cls._hash_password(password, salt)
        return cls(account_number, password_hash, salt, float(balance))

    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        return self._hash_password(password, self.salt) == self.password_hash

    def check_balance(self) -> str:
        return f"Your current balance is: ${self.balance:.2f}"

    def withdraw(self, amount: float) -> str:
        if amount <= 0:
            return "Invalid amount. Please enter a positive number."
        if amount > self.balance:
            return "Insufficient funds."
        self.balance -= amount
        return f"Withdrawal successful. New balance: ${self.balance:.2f}"

    def deposit(self, amount: float) -> str:
        if amount <= 0:
            return "Invalid amount. Please enter a positive number."
        self.balance += amount
        return f"Deposit successful. New balance: ${self.balance:.2f}"

    def change_password(self, old_password: str, new_password: str) -> str:
        if not self.verify_password(old_password):
            return "Incorrect password."
        self.salt = secrets.token_hex(16)
        self.password_hash = self._hash_password(new_password, self.salt)
        return "Password changed successfully."
