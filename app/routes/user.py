from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select 

from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.db.deps import get_db
from app.core.security import hash_password


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(new_user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new user in the database with a hashed password.

    Args:
        new_user_data (UserCreate): Incoming user data from the request body.
        db (AsyncSession): Database session injected through dependency
    
    Returns:
        UserOut: The newly created user data (excluding password).
    """
    # Check if the user already exists by email 
    database_query_result = await db.execute(select(User).where(User.email == new_user_data.email))
    existing_user = database_query_result.scalar_one_or_none() # Return a single result if found or returns None if no match found 
    
    
    if existing_user: # Return message if user already exists within the database
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered."
        )
    
    # Hash the password before storing in database 
    new_user = User(
        email=new_user_data.email,
        full_name=new_user_data.full_name,
        hashed_password=hash_password(new_user_data.password)
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    
    return new_user