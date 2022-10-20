#holds utilities functions
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#when user creating account
def hash(password: str):
    return pwd_context.hash(password)

#when login
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)