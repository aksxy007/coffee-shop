import bcrypt
import base64

def hash_password(plain_password: str) -> str:
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    
    # Convert bytes to a Base64-encoded string for easy storage
    return base64.b64encode(hashed_password).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Decode the hashed password from Base64 to bytes
    hashed_password_bytes = base64.b64decode(hashed_password)
    
    # Verify the password against the stored hashed password
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password_bytes)