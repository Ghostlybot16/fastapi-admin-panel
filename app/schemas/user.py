from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID



class UserBase(BaseModel):
    """
    Shared base schema for user-related operations.
    
    Includes fields shared that are common to both input (creation) and output (reponses) user schemas.
    """
    email: EmailStr
    full_name: Optional[str] = None
    

class UserCreate(UserBase):
    """
    Schema for creating a new user.
    
    Accepts:
        - Email
        - Optional full name 
        - Password
    """
    password: str # Password to be hashed on creation

class UserOut(UserBase):
    """
    Schema for returning user data to clients.
    
    Includes UUID and account creation timestamp.
    """
    id: UUID
    created_at: datetime
    
    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }