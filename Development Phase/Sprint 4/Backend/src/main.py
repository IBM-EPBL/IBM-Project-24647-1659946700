from flask import Flask, request, g
from utils.loadenv import LoadEnv
from utils.db import ConnectDB
import utils.db
from loader import SchemaLoader
from schemas.UserSchema import User
from schemas.ExpenseSchema import Expense
from schemas.SalarySchema import Salary
import os
from functools import wraps
import json
from utils.auth import token_encode, token_required
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app=app)
app.secret_key = "deadman"
app.config['SECRET_KEY'] = 'niggatarun'

LoadEnv()

JSON_TYPE = "application/json"
TYPE = 'Content-Type'
TYPE_OBJ = {TYPE: JSON_TYPE}

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
            email = request.json['email']
            user = User(username=username, password=password, email=email)
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
            print(username, password)
            user = User(username=username, password=password)
            check, uid = user.LoginUser()
            if check:
                data = {
                    'uid': uid
                }
                token = token_encode(data=data)
                resp = {
                    "token": token,
                    "error": False
                }
                return json.dumps(resp), 200, TYPE_OBJ
            else:
                resp = {
                    "error": True
                }
                return json.dumps(resp), 401, TYPE_OBJ

        @app.route("/checkLogin", methods=['GET'])
        @token_required
        def CheckLogin():
            return "GOOOD"

        @app.route("/expense", methods=['POST'])
        @token_required
        def AddExpense():
            user = g.data['uid']
            amount = int(request.json['amount'])
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
        @token_required
        def QueryExpense():
            print({TYPE: JSON_TYPE})
            st = request.json['start_time']
            end = request.json['end_time']
            categories = request.json['category']
            uid = g.data['uid']
            if categories == []:
                l, err = Expense.QueryExpenses(start_time=st, end_time=end, id=uid)
            else:
                l, err = Expense.QueryExpenses(start_time=st, end_time=end, category=categories, id=uid)
            if not err:
                obj = {
                    "error": True
                }
                return json.dumps(obj=obj), 404, {TYPE: JSON_TYPE}
            resArr = []
            for i in l:
                dt = i[5].strftime("%d-%m-%Y")
                print(dt)
                exp = Expense.NewDict(id=i[0], user=i[1], amount=i[2], category=i[3], description=i[4], date=dt)
                resArr.append(exp.__dict__)
            obj = {
                "error": False,
                "expenses": resArr
            }
            return json.dumps(obj=obj), 200, {TYPE: JSON_TYPE}

        @app.route('/salary', methods=['POST'])
        @token_required
        def AddSalary():
            sal = request.json['amount']
            date = request.json['date']
            uid = g.data['uid']
            salary = Salary(user=uid, amount=sal, date=date)
            err = salary.AddSalary()

            if not err:
                return "Unable to Add Salary", 400
            else:
                return "Added Salary", 200

        @app.route('/balance', methods=['GET'])
        @token_required
        def GetSalary():
            uid = g.data['uid']
            d, err = User.GetBalance(id=uid)
            if not err:
                return "Unable to fetch salary", 404
            else:
                resp = {
                    "balance": d[0][0],
                    "limit": d[0][1]
                }
                return json.dumps(resp), 200, TYPE_OBJ

        def ObjToStr(date : datetime) -> str:
            return date.strftime('%Y-%m-%d')

        @app.route('/expenses', methods=['POST'])
        @token_required
        def GetExpenses():
            date = request.json['date']
            category = request.json['category']
            print(date, category)
            uid = g.data['uid']
            neededD = datetime.strptime(date, '%Y-%m-%d')
            arr = []
            subArr = []
            for i in range(6):
                if i == 0:
                    prev = neededD - timedelta(days=30)
                    subArr.append(prev)
                    arr.append([ObjToStr(neededD), ObjToStr(prev)])
                else:
                    prev = subArr[-1] - timedelta(days=30)
                    arr.append([ObjToStr(subArr[-1]), ObjToStr(prev)])
                    subArr.append(prev)
            respJson = {
                "months": {
                    "1": [],
                    "2": [],
                    "3": [],
                    "4": [],
                    "5": [],
                    "6": []
                }
            }
            k = 1
            for i in (arr):
                l, err = Expense.QueryExpenses(start_time=i[1], end_time=i[0], category=category, id=uid)
                if not err:
                    respJson['months'][str(k)] = []
                    k += 1
                resArr = []
                for j in l:
                    dt = j[5].strftime("%d-%m-%Y")
                    print(dt)
                    exp = Expense.NewDict(id=j[0], user=j[1], amount=j[2], category=j[3], description=j[4], date=dt)
                    resArr.append(exp.__dict__)
                respJson['months'][str(k)] = resArr
                k += 1
            d, _ = User.GetBalance(id=uid)
            bal = {
                "balance": d[0][0],
                "limit": d[0][1]
            }
            respJson['balanceObj'] = bal
            return json.dumps(respJson), 200, TYPE_OBJ
        
        app.run(host='0.0.0.0',port=5000)

    except KeyboardInterrupt as e:
        print("LUL")
        utils.db.Connection.close()

if __name__ == "__main__":
    main()

