from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select 
from uuid import UUID

from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserListResponse
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
    
    # Set new user email, full name and password
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

# Fetch ONE USER response using user_id
@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a user from the database using their `user_id` value.

    Args:
        user_id (UUID): The unique ID value of the user to fetch.
        db (AsyncSession): Database session.
    
    Returns:
        UserOut: The user information, if found in database
    """
    
    # Search for user in database using `user_id` value 
    database_query_result = await db.execute(select(User).where(User.id == user_id))
    user_info_from_db = database_query_result.scalar_one_or_none()
    
    if not user_info_from_db: # Error message if user information not found in database
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    return user_info_from_db


# Fetch ALL USERS
@router.get("/", response_model=UserListResponse)
async def get_all_users(db: AsyncSession = Depends(get_db)):
    """
    Fetch all users from the database and return total entries in a wrapped list.

    Args:
        db (AsyncSession): Database session.
    
    Returns:
        List[UserOut]: A list of all users in the system.
    """
    database_query_result = await db.execute(select(User))
    all_users_in_system = database_query_result.scalars().all() # Search the database for all users
    
    return {
        "total": len(all_users_in_system),
        "users": [UserOut.model_validate(user) for user in all_users_in_system] # Converts each SQLAlchemy User ORM object into a UserOut Pydantic schema object
    }

