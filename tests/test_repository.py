from models.db import DB
from models.repository import Repository
from models.models import Landlord

import pytest, json

@pytest.mark.asyncio
async def test_Landlord_Service_returns_error_when_duplicate_entry_is_entered():
    db = DB("test", "homeowner", "localhost", "roomr")
    repository = Repository(db)
    with open(r"./tests/sample_landlord.json", mode="r") as test_landlord:
        landlordData = json.load(test_landlord)
        landlord = Landlord(**landlordData)
    
    monad = await repository.insert(landlord)
    monad = await repository.insert(landlord)
    assert monad.error_status == {"status": 409, "reason": "Failed to insert data into database"}

@pytest.mark.asyncio
async def test_Landlord_Service_returns_error_when_login_with_an_email_that_does_not_exist():
    db = DB("test", "homeowner", "localhost", "roomr")
    repository = Repository(db)
    with open(r"./tests/sample_landlord.json", mode="r") as test_landlord:
        landlordData = json.load(test_landlord)
        landlord = Landlord(**landlordData)
        landlord.email = "FDASFDASFDASF@SDAFsdaf.com"
    monad = await repository.login(landlord, "aaaaaa", "abc123")
    assert monad.error_status == {"status": 401, "reason": "Invalid email or password"}
@pytest.mark.asyncio
async def test_Landlord_Service_returns_error_when__empty_data_is_returned():
    db = DB("test", "homeowner", "localhost", "roomr")
    repository = Repository(db)
    with open(r"./tests/sample_landlord.json", mode="r") as test_landlord:
        landlordData = json.load(test_landlord)
        landlord = Landlord(**landlordData)
       
    monad = await repository.login(landlord, "bbbbbb", "abc123")
    assert monad.error_status == {"status": 401, "reason": "Invalid email or password"}


@pytest.mark.asyncio
async def test_Landlord_Service_returns_error_when_no_data_is_returned():
    db = DB("test", "homeowner", "localhost", "roomr")
    repository = Repository(db)
    landlord = Landlord(id=-1, password="aaaaaa")
    monad = await repository.get_landlord(landlord)
    assert monad.error_status == {"status": 404, "reason": "No data in repository monad"}
