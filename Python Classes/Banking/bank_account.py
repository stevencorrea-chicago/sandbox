class BankAccount:
    def __init__(self, **kwargs):
        """
        Initialize a new instance of BankAccount.

        """

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"BankAccount({self.__dict__}"
    
    def get_attributes(self, attribute):
        if attribute not in self.__dict__:
            return "Attribute not found"
        return self.__dict__[attribute]

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Deposited: ${amount:,.2f}. New balance: ${self.balance:,.2f}"
        else:
            return "Deposit amount must be positive."
    
    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            return f"Withdrew: ${amount:,.2f}. New balance: ${self.balance:,.2f}"
        else:
            return f"Insufficient funds! Current balance: ${self.balance:,.2f}, requested amount: ${amount:,.2f}."

def main():
    new_customer = BankAccount(acct_number="123456789", fname="Abraham", lname="Lincoln", state = 'Illinois', balance=1000.00)

    print(new_customer)
    print(new_customer.get_attributes('lname'))  # Output: Abraham

    print(new_customer.deposit(500))  # Output: Deposited: 500. New balance: 1500.0
    print(new_customer.withdraw(200))  # Output: Withdrew: 200. New balance: 1300.0
    print(new_customer.withdraw(2000))  # Output: Insufficient funds! Current balance is 1300.0.
    
if __name__ == "__main__":
    main()