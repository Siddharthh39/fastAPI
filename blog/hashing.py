from passlib.context import CryptContext

class Hashing:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hashPassword(self, password:str):
        return self.pwd_context.hash(password)

    def verify(self, hashed_password, plain_password):
        return self.pwd_context.verify(plain_password, hashed_password)