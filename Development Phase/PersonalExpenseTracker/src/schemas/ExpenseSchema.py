from utils.db import ExecuteDB

class Expense:
    def __init__(self, amount="", category="", date=None, description="", user="") -> None:
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description
        self.user = user

    @staticmethod
    def CreateSchema():
        query = "CREATE TABLE IF NOT EXISTS EXPENSES (expense_id INT PRIMARY KEY NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),user INT NOT NULL, amount FLOAT NOT NULL, category varchar(40) NOT NULL, description varchar(100), spent_date DATE NOT NULL, FOREIGN KEY user_id (user) REFERENCES USERS ON DELETE NO ACTION)"
        ExecuteDB(query)

    def ValidateExpense(self) -> bool:
        return self.amount > 0 and self.user != "" and self.category != "" and self.date != ""

    def AddExpense(self):
        if self.ValidateExpense():
            query = f"INSERT INTO EXPENSES (user, amount, category, description, spent_date) VALUES ({self.user}, {self.amount}, '{self.category}', '{self.description}', TO_DATE('{self.date}', 'DD-MM-YYYY'))"
            print(query)
            _, err = ExecuteDB(command=query)
            return err
        return False

    @staticmethod
    def QueryExpenses(start_time, end_time, id, category="all"):
        if category == "all":
            query = f"SELECT * FROM EXPENSES WHERE user = {id} and spent_date between '{start_time}' and '{end_time}'"
        else:
            catStr = "("
            for i in range(len(category)-1):
                catStr += f"'{category[i]}', "
            catStr += f"'{category[len(category)-1]}')"
            query = f"SELECT * FROM EXPENSES WHERE user = {id} and category IN {catStr} and spent_date between '{start_time}' and '{end_time}'"
            print(query)
        l, err = ExecuteDB(command=query)
        print(l)
        return l, err

