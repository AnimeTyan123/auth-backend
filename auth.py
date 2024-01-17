from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from argon2 import PasswordHasher
from typing import Optional

app = FastAPI()
ph = PasswordHasher()

# Dummy database
users_db = {}

# Models
class User(BaseModel):
    username: str
    password: str

class UserInDB(BaseModel):
    username: str
    hashed_password: str

# Utility function
def hash_password(password: str):
    return ph.hash(password)

# Registration endpoint
@app.post("/register")
def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = hash_password(user.password)
    users_db[user.username] = UserInDB(username=user.username, hashed_password=hashed_password)
    return {"message": "User registered successfully"}

# Login endpoint
@app.post("/login")
def login(user: User):
    db_user = users_db.get(user.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    try:
        ph.verify(db_user.hashed_password, user.password)
    except:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"message": "Login successful"}

# Run the app
if __name__ == "__main__":
   import uvicorn
   uvicorn.run(app, host="0.0.0.0", port=8000)

