from schemas.UserSchema import User
from schemas.ExpenseSchema import Expense
from schemas.SalarySchema import Salary

def CreateAll():
    User.CreateSchema()
    Expense.CreateSchema()
    Salary.CreateSalary()