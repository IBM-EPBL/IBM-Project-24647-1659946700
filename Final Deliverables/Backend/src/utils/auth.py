import jwt
import json
from flask import request, g
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'token' in request.headers:
            token = request.headers['token']
        # return 401 if token is not passed
        if not token:
            return json.dumps({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, 'niggatarun', algorithms=['HS256'])
            g.data = data
        except Exception as e:
            print(e)
            return json.dumps({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(*args, **kwargs)
  
    return decorated

def token_encode(data):
    token = jwt.encode(data, 'niggatarun', algorithm='HS256')
    return token