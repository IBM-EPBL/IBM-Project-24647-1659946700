from flask import Flask, request, session
from utils.loadenv import LoadEnv
from utils.db import ConnectDB
import utils.db
from loader import SchemaLoader
from schemas.UserSchema import User
from schemas.ExpenseSchema import Expense
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = "deadman"

LoadEnv()

# def authenticateUser():
#     def _authenticateUser(f):
#         @wraps(f)
#         def __authenticateUser(*args, **kwargs):
#             # just do here everything what you need
#             print('before home')
#             result = f(*args, **kwargs)
#             print('home result: %s' % result)
#             print('after home')
#             return result
#         return __authenticateUser
#     return _authenticateUser

def main():
    try:
        dsn_hostname = os.getenv('DB_HOST')
        dsn_uid = os.getenv('DB_USER')
        dsn_password = os.getenv('DB_PASS')
        dsn_db = os.getenv('DB_NAME')
        dsn_driver = os.getenv('DB_DRIVER')
        dsn_port = os.getenv('DB_PORT')
        dsn_protocol = os.getenv('DB_PROTOCOL')
        dsn_cert = os.getenv('DB_CERT')

        ConnectDB(dsn_db=dsn_db, dsn_hostname=dsn_hostname, dsn_password=dsn_password, dsn_port=dsn_port, dsn_protocol=dsn_protocol, dsn_uid=dsn_uid, dsn_driver=dsn_driver)
        SchemaLoader.CreateAll()

        @app.route("/user", methods=['POST'])
        def AddUser():
            username = request.json['username']
            password = request.json['password']
            user = User(username=username, password=password)
            err = user.AddUser()
            print(err)
            if not err:
                return "Unable to Create User", 400
            else:
                return "Successfully Created User", 200

        @app.route("/login", methods=['POST'])
        def LoginUser():
            username = request.json['username']
            password = request.json['password']
            user = User(username=username, password=password)
            check, uid = user.LoginUser()
            if check:
                session['isLoggedIn'] = True
                session['uid'] = uid
                return "Logged IN", 200
            else:
                return "Invalid Credentials", 401

        @app.route("/checkLogin", methods=['GET'])
        def CheckLogin():
            if 'isLoggedIn' in session and session['isLoggedIn']:
                return f"Logged IN, uid: {session['uid']}", 200
            return f"Not Logged IN", 401

        @app.route("/expense", methods=['POST'])
        def AddExpense():
            if 'isLoggedIn' not in session or not session['isLoggedIn']:
                return "LOGIN BRO", 401
            else:
                user = session['uid']
                amount = request.json['amount']
                category = request.json['category']
                description = request.json['description']
                date = request.json['date']
                expense = Expense(amount=amount, category=category, description=description,date=date, user=user)
                err = expense.AddExpense()
                if not err:
                    return "Unable To Add Expense", 400
                else:
                    return "Expense Added", 200

        @app.route('/queryexpense', methods=['GET'])
        def QueryExpense():
            if 'isLoggedIn' not in session or not session['isLoggedIn']:
                return "LOGIN BRO", 401
            else:
                st = request.json['start_time']
                end = request.json['end_time']
                categories = request.json['category']
                uid = session['uid']
                Expense.QueryExpenses(start_time=st, end_time=end, category=categories, id=uid)
                return "THANKS"

        app.run(port=5000)

    except KeyboardInterrupt as e:
        print("LUL")
        utils.db.Connection.close()

if __name__ == "__main__":
    main()

