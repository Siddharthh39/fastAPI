from passlib.context import CryptContext
import hashlib

class Hashing:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hashPassword(self, password: str):
        # Truncate password to 72 bytes to prevent bcrypt error
        # Use SHA256 hash for longer passwords to maintain security
        if len(password.encode('utf-8')) > 72:
            password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return self.pwd_context.hash(password)

    def verify(self, hashed_password, plain_password):
        # Apply same truncation logic for verification
        if len(plain_password.encode('utf-8')) > 72:
            plain_password = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
        try:
            return self.pwd_context.verify(plain_password, hashed_password)
        except ValueError as e:
            if "password cannot be longer than 72 bytes" in str(e):
                # Fallback: hash the password and try again
                plain_password = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
                return self.pwd_context.verify(plain_password, hashed_password)
            raise e