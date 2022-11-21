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
    monad = await repository.login(Landlord(email=loginData["email"], password=""), 
        password=loginData["password"], 
        deviceId=loginData["deviceId"])
    if monad.error_status:
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return monad.get_param_at(0).to_json()


@app.get("/Landlord/{landlordId}")
async def get_landlord(landlordId: int):
    landlord = Landlord(password="")
    landlord.id = landlordId
    monad = await repository.get_landlord(landlord)
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return monad.get_param_at(0).to_json()

@app.delete("/Landlord/{landlordId}")
async def delete_landlord(landlordId: int):
    landlord = Landlord(password="")
    landlord.id = landlordId
    monad = await repository.delete(landlord)
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return monad.get_param_at(0).to_json()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8086)