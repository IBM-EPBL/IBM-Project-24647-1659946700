from utils.db import ExecuteDB
import re
from utils.hashers import HashPassword, CheckPassword

USERNAME_REGEX = "^(?=[a-zA-Z0-9._]{8,20}$)(?!.*[_.]{2})[^_.].*[^_.]$"
PASSWORD_REGEX = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

class User:
    def __init__(self, username="", password="") -> None:
        self.username = username
        self.password = password

    @staticmethod
    def CreateSchema():
        query = "CREATE TABLE IF NOT EXISTS USERS (user_id INT PRIMARY KEY NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) , username varchar(25) NOT NULL UNIQUE, password varchar(100) NOT NULL)"
        ExecuteDB(query)

    def CheckPassword(self) -> bool:
        pat = re.compile(PASSWORD_REGEX)
        return re.fullmatch(pattern=pat, string=self.password)

    def CheckUsername(self) -> bool:
        pat = re.compile(USERNAME_REGEX)
        return re.fullmatch(pattern=pat, string=self.username)

    def ValidateUser(self) -> bool:
        return self.CheckPassword() and self.CheckUsername()

    def AddUser(self) -> bool:
        if self.ValidateUser():
            hashed_pwd = HashPassword(self.password)
            self.hashed_pwd = hashed_pwd
            query = f"INSERT INTO USERS (username, password) VALUES ('{self.username}', '{hashed_pwd}')"
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
