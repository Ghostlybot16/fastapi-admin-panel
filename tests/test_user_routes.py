import asyncio
import pytest
import uuid
import pytest_asyncio
from httpx import AsyncClient
from fastapi import status
from app.db.session import engine, Base




@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_and_teardown():
    """
    Setup and teardown fixture for each test:
    - Creates all tables before a test. 
    - Drops all tables after the test to allow for isolation.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
        
        

@pytest.mark.asyncio
async def test_create_user(async_client: AsyncClient):
    """
    Test the POST /users endpoint by sending a new user's data.

    Verified that:
    - The response status code is 201 (Created)
    - The returned JSON contains the correct user information
    - Fields like `id` and `created_at` are present in the response
    """
    
    test_payload = { # Define the data to send to the /users endpoint
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "password123"
    }
    
    # Send a POST request to /users with the test payload information
    response = await async_client.post("/users/", json=test_payload) 
    
    # Check that the response status code is HTTP 201 (Created)
    assert response.status_code == status.HTTP_201_CREATED
    
    returned_data = response.json() # Parse the response JSON body 
    
    # Assert that the returned data matches the sent payload information
    assert returned_data["email"] == test_payload["email"]
    assert returned_data["full_name"] == test_payload["full_name"]
    assert "id" in returned_data 
    assert "created_at" in returned_data




# Duplicate user creation
@pytest.mark.asyncio
async def test_create_user_duplicate_email(async_client: AsyncClient):
    """
    Test POST /users with a duplicate email.
    
    Verified that:
    - Initial users is created 
    - The response status code is 400 (Bad Request) for the second account creation  
    - Second user with the same email gets rejected and sees a "Email is already registered" message
    """
    
    test_payload = {
        "email": "duplicateUser@example.com",
        "full_name": "Dup User",
        "password": "password123"
    }
    
    response1 = await async_client.post("/users/", json=test_payload) # Send a POST request to /users/ to initially create the first user
    assert response1.status_code == status.HTTP_201_CREATED
    
    response2 = await async_client.post("/users/", json=test_payload) # Send a POST request to /users/ to create another user using the same account credentials
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email is already registered." in response2.text




@pytest.mark.asyncio
async def test_get_one_user(async_client: AsyncClient):
    """
    Test the GET /users/{user_id} endpoint to retrieve a specific user.
    """
    
    test_payload = {
        "email": "fetchOneUser@example.com",
        "full_name": "Fetch One User",
        "password": "password123"
    }
    
    create_response = await async_client.post("/users/", json=test_payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    
    user_id = create_response.json()["id"]
    
    await asyncio.sleep(0.1)
    
    # Fetch the user by ID
    response = await async_client.get(f"/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    
    returned_data = response.json() # Parse the response JSON body
    
    assert returned_data["email"] == test_payload["email"]
    assert returned_data["full_name"] == test_payload["full_name"]
    assert "id" in returned_data




@pytest.mark.asyncio
async def test_get_one_user_not_found(async_client: AsyncClient):
    """ 
    Test GET /users/{user_id} with non-existent user.
    
    Verified that:
    - The response status code is 404 for missing user
    - A random UUID is used
    """
    random_uuid = str(uuid.uuid4()) # Generate a random UUID
    response = await async_client.get(f"/users/{random_uuid}") # Send a GET request using the randomly generated UUID value
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "User not found." in response.text




@pytest.mark.asyncio
async def test_get_all_users(async_client: AsyncClient):
    """
    Test the GET /users endpoint to retrieve all users.
    """
    # Create a user if DB is empty 
    test_payload = {
        "email": "allusers@example.com",
        "full_name": "All Users Test",
        "password": "password123"
    }
    await async_client.post("/users/", json=test_payload)
    
    # Fetch all users 
    response = await async_client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    
    returned_data = response.json() # Parse the response JSON body
    
    assert "total" in returned_data
    assert "users" in returned_data
    assert isinstance(returned_data["users"], list) # Check that a list type has been returned 
    
    emails = [user["email"] for user in returned_data["users"]] # Check that the created user is in the returned list
    assert test_payload["email"] in emails