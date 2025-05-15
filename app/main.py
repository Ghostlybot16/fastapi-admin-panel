from fastapi import FastAPI

# FastAPI app instance 
app = FastAPI()

# Root route 
@app.get("/")
def root():
    return {"message": "Welcome to the Admin API!"}