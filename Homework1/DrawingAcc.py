#vadesiz hesap
from Homework1 import Account


class DrawingAcc(Account):

    def __init__ (self, account_holder, account_number, balance):
        super().__init__(account_holder, account_number, balance)
