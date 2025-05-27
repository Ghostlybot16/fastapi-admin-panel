import uuid
from sqlalchemy import Column, String, DateTime, func
# from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base

class User(Base):
    """
    SQLAlchemy ORM model for the `users` table.
    
    
    Columns:
        id (UUID): Unique identifier for each user, generated using uuid4 (primary key).
        email (str): User's email address, must be unique
        hashed_password (str): Securely stored password (hashed).
        full_name (str): Optional full name of the user. 
        created_at (datetime): Timestamp of when the user was created. 

    """
    
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4())) # String based UUID for SQLite
    email = Column(String(255), unique=True, nullable=False, index=True) # User's email address, must be unique
    full_name = Column(String(255), nullable=True) # Optional full name for display
    hashed_password = Column(String(255), nullable=False) # Hashed password for secure storage
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # Auto set timestamp at creation