from schemas.UserSchema import User
from schemas.ExpenseSchema import Expense

def CreateAll():
    User.CreateSchema()
    Expense.CreateSchema()