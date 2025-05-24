# Internal Admin Panel API

A secure, modular backend API for internal admin tools - built using **FastAPI**, **PostgreSQL**, **Docker**, and **Alembic**. This API provides clean, scalable foundations for internal dashboards, analytics and authenticated admin operations. 

---

## Project Goal

> To build a containerized, production-grade **Admin Panel API** that supports user management, JWT-based security (WIP), and seamless database integration that is ready to plug into internal company tools or frontends. 

---

## Tech Stack 

- FastAPI
- PostgreSQL 16 + pgAdmin 4
- SQLAlchemy 2.0 + Alembic
    - asyncpg, SQLAlchemy asyncio
- Docker + Docker Compose
- python-dotenv (config management)
- Postman (API Testing)

---

## Features Implemented So Far

- [x] **POST /users** - Create new user with hashed password
- [x] **GET /users** - Fetch all users, wrapped with total count of entries
- [x] **GET /users/{user_id}** - Fetch user by UUID
- [x] Integrated SQLAlchemy ORM and Alembic migrations
- [x] pgAdmin 4 UI for database inspection
- [x] Dockerized multi-service startup
- [x] Verified API behavior with Postman

---

## API Testing with Postman

All routes have been tested using Postman and exported for reproducibility 

Stored at: `/postman_collection/GraphQL-Docker-PostgreSQL-Python-AdminPanel.postman_collection.json`  
  


#### Sample Responses   

**POST /users**  
Creates a new user with hashed password.  

![POST User](/postman_collection/postman_screenshots/post-create-newUser.png "POST Method: Create New User")  
-

**GET /users**  
Returns total count and lists all users.  

![GET All Users](/postman_collection/postman_screenshots/get-all-users.png "GET Method: Fetch All Users")
-

**GET /users/{user_id}**  
Returns a single user based on their Universally Unique Identifier (`UUID`) value.  

![GET One User](/postman_collection/postman_screenshots/get-user-by-id.png "GET Method: Fetch One User")
-

## Next Steps 

- Implement **PUT /users/{user_id}** to update user information.
- Implement **DELETE /users/{user_id}** to delete user.
- Add **JWT login route** and token generation.
- Protect sensitive routes with JWT-based dependency.
- Add automated tests with `pytest`
- Add rate limiting, logging, front-end dashboard

---

## Getting Started 

```bash
# Clone this repo
git clone http://github.com/Ghostlybot16/graphql-docker-admin.git
cd graphql-docker-admin

# Start Docker services 
docker compose up --build 

# Run Alembic migrations 
docker exec -it fastapi-app alembic -c /project/alembic.ini upgrade head
