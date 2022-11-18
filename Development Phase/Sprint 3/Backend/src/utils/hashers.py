import bcrypt

def HashPassword(password : str) -> str:
    enc = password.encode('utf-8')

    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(password=enc, salt=salt)
    return hashed.decode('utf-8')

def CheckPassword(hashed : str, passw : str) -> bool:
    enc = passw.encode('utf-8')
    enc_hashed = hashed.encode('utf-8')
    return bcrypt.checkpw(password=enc, hashed_password=enc_hashed)