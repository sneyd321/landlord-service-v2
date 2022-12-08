from fastapi import FastAPI, HTTPException
from typing import List
from models.schemas import LandlordSchema, LoginSchema, CreateLandlordSchema
from models.db import DB
from models.models import Landlord
from models.repository import Repository
from models.firebase import Firebase

import uvicorn, os

user = os.environ.get('DB_USER', "root")
password = os.environ.get('DB_PASS', "root")
host = os.environ.get('DB_HOST', "localhost")
database = os.environ.get('DB_DATABASE', "roomr")

db = DB(user, password, host, database)
repository = Repository(db)

firebase = Firebase()
firebase.setServiceAccountPath(r"./models/static/ServiceAccount.json")
firebase.init_app()

app = FastAPI()

@app.get("/Health")
async def health_check():
    return {"status": 200}


@app.post("/Landlord")
async def create_landlord(request: CreateLandlordSchema, isTest: bool = False):
    landlord = Landlord(**request.dict())
    monad = await repository.insert(landlord, firebase, isTest=isTest)
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return landlord.to_json()


@app.post("/Login")
async def login(request: LoginSchema):
    monad = await repository.login(**request.dict())
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return monad.get_param_at(0).to_json()


@app.get("/Landlord/{landlordId}")
async def get_landlord(landlordId: int):
    
    monad = await repository.get_landlord(landlordId)
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return monad.get_param_at(0).to_json()

@app.delete("/Landlord")
async def delete_landlord(request: LandlordSchema):
    landlord = Landlord(**request.dict())
    monad = await repository.delete(landlord)
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return monad.get_param_at(0).to_json()

@app.put("/Landlord")
async def update_landlord(request: LandlordSchema):
    landlord = Landlord(**request.dict())
    monad = await repository.update(landlord)
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return monad.get_param_at(0).to_json()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8086)