import os

def LoadEnv():
    f = open(os.getcwd() + "/.env", "r")
    for i in f.readlines():
        p = i.split("=")
        os.environ[p[0].strip()] = p[1].strip()