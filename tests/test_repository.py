from models.db import DB
from models.repository import Repository
from models.models import Landlord

import pytest, json, os

host = os.environ.get("DB_HOST", "localhost")

async def test_Landlord_Service_returns_error_when_same_email_is_inserted():
    db = DB("root", "root", host, "roomr")
    repository = Repository(db)
    with open(r"./tests/sample_landlord.json", mode="r") as test_landlord:
        landlordData = json.load(test_landlord)
        landlord = Landlord(**landlordData)
   
    monad = await repository.insert(landlord)
    monad = await repository.insert(landlord)
    assert monad.error_status == {"status": 409, "reason": "Failed to insert data into database"}


async def test_Landlord_Service_returns_error_on_login_when_account_not_found():
    db = DB("root", "root", host, "roomr")
    repository = Repository(db)
    with open(r"./tests/sample_landlord.json", mode="r") as test_landlord:
        landlordData = json.load(test_landlord)
        landlord = Landlord(**landlordData)
        landlord.email = "FDASFDASFDASF@SDAFsdaf.com"
    monad = await repository.login(landlord.email, "aaaaaa", "abc123")
    assert monad.error_status == {"status": 404, "reason": "Invalid email or password"}

async def test_Landlord_Service_returns_error_when_password_is_invalid():
    db = DB("root", "root", host, "roomr")
    repository = Repository(db)
    with open(r"./tests/sample_landlord.json", mode="r") as test_landlord:
        landlordData = json.load(test_landlord)
        landlord = Landlord(**landlordData)

    monad = await repository.insert(landlord)
    monad = await repository.login(landlord.email, "bbbbbb", "abc123")
    assert monad.error_status == {"status": 401, "reason": "Invalid email or password"}

async def test_Landlord_Service_returns_not_found_error_on_get_landlord():
    db = DB("root", "root", host, "roomr")
    repository = Repository(db)
    with open(r"./tests/sample_landlord.json", mode="r") as test_landlord:
        landlordData = json.load(test_landlord)
        landlord = Landlord(**landlordData)
        landlord.id = -1
    monad = await repository.get_landlord(landlord)
    assert monad.error_status == {"status": 404, "reason": f"Landlord not found with id: {landlord.id}"}


async def test_Landlord_Service_returns_not_found_error_on_update():
    db = DB("root", "root", host, "roomr")
    repository = Repository(db)
    with open(r"./tests/sample_landlord.json", mode="r") as test_landlord:
        landlordData = json.load(test_landlord)
        landlord = Landlord(**landlordData)
        landlord.email = "FDASFDASFDASF@SDAFsdaf.com"

    monad = await repository.update(landlord)
    assert monad.error_status == {"status": 404, "reason": f"Landlord not found with id: {landlord.id}"}

async def test_Landlord_Service_returns_not_found_error_on_delete():
    db = DB("root", "root", host, "roomr")
    repository = Repository(db)
    with open(r"./tests/sample_landlord.json", mode="r") as test_landlord:
        landlordData = json.load(test_landlord)
        landlord = Landlord(**landlordData)
        landlord.email = "FDASFDASFDASF@SDAFsdaf.com"

    monad = await repository.delete(landlord)
    assert monad.error_status == {"status": 404, "reason": f"Landlord not found with id: {landlord.id}"}
