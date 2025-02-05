class Account:
    def __init__(self, account_holder, account_number, balance):
        self.account_holder = account_holder
        self.account_number = account_number
        self.__balance = balance


    def deposit(self, amount):
        if amount > 0:
            self.__balance = self.__balance + amount
            print(f"Deposited {amount} to account {self.account_number}. New balance is {self.__balance}")

        else:
            print("Invalid amount")    

    def withdraw(self, amount):
        if amount > 0 and amount <= self.__balance:
            self.__balance = self.__balance - amount
            print(f"Withdrew {amount} from account {self.account_number}. New balance is {self.__balance}")

        else:
            print("Insufficient balance or invalid amount")  

    def show_balance(self):
        print(f"Account {self.account_number} has balance {self.__balance}")


    def get_balance(self): 
        return self.__balance
    
    def set_balance(self, amount):  
        self.__balance = amount
    