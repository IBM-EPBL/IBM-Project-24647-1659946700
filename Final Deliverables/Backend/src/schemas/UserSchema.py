from utils.db import ExecuteDB
import re
from utils.hashers import HashPassword, CheckPassword

USERNAME_REGEX = "^(?=[a-zA-Z0-9._]{8,20}$)(?!.*[_.]{2})[^_.].*[^_.]$"
PASSWORD_REGEX = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
EMAIL_REGEX = "^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$"

class User:
    def __init__(self, username="", password="", email="") -> None:
        self.username = username
        self.password = password
        self.email = email

    @staticmethod
    def CreateSchema():
        query = "CREATE TABLE IF NOT EXISTS USERS (user_id INT PRIMARY KEY NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) , username varchar(25) NOT NULL UNIQUE, password varchar(100) NOT NULL, email varchar(35) NOT NULL, balance FLOAT NOT NULL, lim FLOAT NOT NULL)"
        ExecuteDB(query)

    def CheckEmail(self) -> bool:
        pat = re.compile(EMAIL_REGEX)
        return re.fullmatch(pattern=pat, string=self.email)

    def CheckPassword(self) -> bool:
        pat = re.compile(PASSWORD_REGEX)
        return re.fullmatch(pattern=pat, string=self.password)

    def CheckUsername(self) -> bool:
        pat = re.compile(USERNAME_REGEX)
        return re.fullmatch(pattern=pat, string=self.username)

    def ValidateUser(self) -> bool:
        return self.CheckPassword() and self.CheckUsername() and self.CheckEmail()

    def AddUser(self) -> bool:
        if self.ValidateUser():
            hashed_pwd = HashPassword(self.password)
            self.hashed_pwd = hashed_pwd
            query = f"INSERT INTO USERS (username, password, email, balance, lim) VALUES ('{self.username}', '{hashed_pwd}', '{self.email}', 0, 10000000000)"
            print(query)
            _, err = ExecuteDB(command=query)
            return err
        return False

    def LoginUser(self):
        try:
            query = f"SELECT PASSWORD, user_id FROM USERS WHERE username='{self.username}'"
            res = ExecuteDB(command=query)[0][0]
            uid = res[1]
            h = res[0]
            return CheckPassword(hashed=h, passw=self.password), uid
        except Exception as e:
            print(e)
            return False, None

    @staticmethod
    def AddToWallet(amount, id):
        query = f"UPDATE USERS SET balance = balance + {amount} where user_id = {id}"
        print(query)
        _, err = ExecuteDB(command=query)
        return err
    
    @staticmethod
    def DeductWallet(amount, id):
        query = f"UPDATE USERS SET balance = balance - {amount}, lim = lim - {amount} where user_id = {id}"
        print(query)
        _, err = ExecuteDB(command=query)
        return err

    @staticmethod
    def SetLimit(amount):
        query = f"UPDATE USERS SET lim = {amount} where user_id = {id}"
        print(query)
        _, err = ExecuteDB(command=query)
        return err

    @staticmethod
    def GetBalance(id):
        query = f"SELECT balance, lim FROM USERS where user_id = {id}"
        print(query)
        return ExecuteDB(command=query)
