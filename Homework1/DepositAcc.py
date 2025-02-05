#vadeli hesap
from Homework1.Account import Account


class DepositAcc(Account):
    
    def __init__(self, account_holder, account_number, balance, interest_rate):
        super().__init__(account_holder, account_number, balance)
        self.interest_rate = interest_rate



    def calculate_interest(self):
       balance = self.get_balance()  
       interest = balance * (self.interest_rate / 100)  
       print(f"Calculated interest: {interest}")  
       return interest

    def withdraw(self, amount):
       interest = self.calculate_interest()  
       updated_balance = self.get_balance() + interest  
       self.set_balance(updated_balance)  
       print(f"New balance after adding interest: {self.get_balance()}")  
       super().withdraw(amount)  



