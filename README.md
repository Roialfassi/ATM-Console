# ATM Console Program 🏦

## Overview
This Python console application simulates an **ATM machine**, allowing customers to perform banking transactions such as:
- Checking balance
- Withdrawing cash
- Depositing cash
- Changing their password

The application securely loads customer data from a file (`customers.json`) and updates it upon exit to maintain changes.


## Installation & Setup
### Prerequisites
- Python 3.8+

### Steps to Run the Program
1. **Clone or Download the Repository**
   ```sh
   git clone https://github.com/yourusername/ATM-Console.git
   cd ATM-Console
   ```
   
2. **Run the Program**
   ```sh
    python ATM-Console.py
   ```

If no customer data file (customers.json) exists, the program automatically generates sample accounts.

# How to Use
## Login
- Enter your account number.
- Enter your password.
- If incorrect, retry.

## Select an option 
ATM Menu:
1. Check Balance
2. Withdraw Cash
3. Deposit Cash
4. Change Password

Enter -1 at the login screen to exit the ATM.

# Error Handling & Validations

- Ensures user enters valid numbers for withdrawals/deposits.
- Prevents invalid withdrawals (e.g., negative or exceeding balance).
- Password change requires correct old password.
- Handles missing or corrupted customers.json gracefully.

