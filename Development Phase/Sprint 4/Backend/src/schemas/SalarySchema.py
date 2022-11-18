from utils.db import ExecuteDB
from schemas.UserSchema import User


class Salary:
    def __init__(self, user="", amount="", date="") -> None:
        self.user = user
        self.amount = amount
        self.date = date

    @staticmethod
    def CreateSalary():
        query = "CREATE TABLE IF NOT EXISTS SALARIES (salary_id INT PRIMARY KEY NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) , amount FLOAT NOT NULL, update_date DATE NOT NULL, ref_user INT NOT NULL, FOREIGN KEY user_id (ref_user) REFERENCES USERS ON DELETE NO ACTION)"
        ExecuteDB(query)

    def ValidateSalary(self):
        return self.date != "" and self.user != "" and self.amount != ""

    def AddSalary(self):
        if self.ValidateSalary():
            query = f"INSERT INTO SALARIES (ref_user, amount, update_date) VALUES ({self.user}, {self.amount}, TO_DATE('{self.date}', 'YYYY-MM-DD'))"
            print(query)
            _, err = ExecuteDB(command=query)
            User.AddToWallet(amount=self.amount, id=self.user)
            return err
        return False

    @staticmethod
    def GetSalary(uid):
        query = f"SELECT * FROM SALARIES WHERE ref_user = {uid} order by update_date limit 2"

