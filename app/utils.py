from passlib.context import CryptContext

# This is to HASH all passwords used in our code
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# This is the fucntion to actually hash the passwords
def hash(password: str):
    return pwd_context.hash(password)

# This is to verify that the login attempt was successful.
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
