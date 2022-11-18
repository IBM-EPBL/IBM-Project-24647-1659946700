from utils.db import ExecuteDB
from schemas.UserSchema import User

class Expense:
    def __init__(self, amount="", category="", date=None, description="", user="") -> None:
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description
        self.user = user
    
    @staticmethod
    def NewDict(amount="", category="", date=None, description="", user="", id=""):
        expense = Expense(amount=amount, category=category, date=date, description=description, user=user)
        expense.AddID(id=id)
        return expense

    def AddID(self,id):
        self.id = id

    @staticmethod
    def CreateSchema():
        query = "CREATE TABLE IF NOT EXISTS EXPENSES (expense_id INT PRIMARY KEY NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),ref_user INT NOT NULL, amount FLOAT NOT NULL, category varchar(40) NOT NULL, description varchar(100), spent_date DATE NOT NULL, FOREIGN KEY user_id (ref_user) REFERENCES USERS ON DELETE NO ACTION)"
        ExecuteDB(query)

    def ValidateExpense(self) -> bool:
        return self.amount > 0 and self.user != "" and self.category != "" and self.date != ""

    def AddExpense(self):
        if self.ValidateExpense():
            query = f"INSERT INTO EXPENSES (ref_user, amount, category, description, spent_date) VALUES ({self.user}, {self.amount}, '{self.category}', '{self.description}', TO_DATE('{self.date}', 'YYYY-MM-DD'))"
            print(query)
            _, err = ExecuteDB(command=query)
            User.DeductWallet(amount=self.amount, id=self.user)
            return err
        return False

    @staticmethod
    def QueryExpenses(start_time, end_time, id, category="all"):
        if category == "all":
            query = f"SELECT * FROM EXPENSES WHERE ref_user = {id} and spent_date between DATE('{start_time}') and DATE('{end_time}')"
        else:
            catStr = "("
            for i in range(len(category)-1):
                catStr += f"'{category[i]}', "
            catStr += f"'{category[len(category)-1]}')"
            query = f"SELECT * FROM EXPENSES WHERE ref_user = {id} and category IN {catStr} and spent_date between DATE('{start_time}') and DATE('{end_time}')"
        print(query)
        return ExecuteDB(command=query)



