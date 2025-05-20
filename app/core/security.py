from passlib.context import CryptContext

# ---------------------------------------------------------
# Create a password hashing context using bcrypt
# ---------------------------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt (password hashing function, modified version of blowfish cipher).

    Args:
        password (str): The password to hash.

    Returns:
        str: Hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify that a plain-text password matches the hashed password.

    Args:
        plain_password (str): User entered password.
        hashed_password (str): Hashed password to store in the database. 

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    
    return pwd_context.verify(plain_password, hashed_password)