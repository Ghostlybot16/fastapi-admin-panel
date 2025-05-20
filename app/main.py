from fastapi import FastAPI
from app.routes import user

# FastAPI app instance 
app = FastAPI()

app.include_router(user.router)

# Root route 
@app.get("/")
def root():
    return {"message": "Welcome to the Admin API!"}