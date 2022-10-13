from fastapi import FastAPI, HTTPException
from typing import List
from models.schemas import *
from models.db import DB
from models.models import Landlord
from models.repository import Repository

import uvicorn, os

user = os.environ.get('DB_USER', "root")
password = os.environ.get('DB_PASS', "root")
host = os.environ.get('DB_HOST', "localhost")
database = os.environ.get('DB_DATABASE', "roomr")

db = DB(user, password, host, database)
repository = Repository(db)

app = FastAPI()

@app.get("/Health")
async def health_check():
    return {"status": 200}

@app.post("/Landlord")
async def create_landlord(request: CreateLandlordSchema):
    landlord = Landlord(**request.dict())
    monad = await repository.insert(landlord)
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return landlord.to_json()

@app.post("/Login")
async def login(request: LoginSchema):
    loginData = request.dict()
    landlord = await repository.get_landlord_by_email(Landlord(**loginData))
    if not landlord:
        return HTTPException(status_code="404", detail="Landlord not found")
    if not landlord.verify_password(loginData["password"], landlord.password):
        return HTTPException(status_code="401", detail="Invalid email or password")
   
    landlord.deviceId = loginData["deviceId"]
    monad = await repository.update(landlord)
    if monad.error_status:
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return landlord.to_json()

    
    



  
@app.get("/Landlord/{landlordId}")
async def get_landlord(landlordId: int):
    landlord = Landlord(password="")
    landlord.id = landlordId
    result = await repository.get_landlord(landlord)
    print(result)
    return result.to_json()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8086)