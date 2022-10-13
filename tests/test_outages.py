from models.db import DB
from models.repository import Repository
from models.models import Landlord
import asyncio, pytest, json


@pytest.mark.asyncio
async def test_Landlord_Service_returns_error_during_database_outage():
    db = DB("test", "homeowner", "localhost", "roomr")
    repository = Repository(db)
    with open(r"./tests/sample_landlord.json", mode="r") as test_landlord:
        landlordData = json.load(test_landlord)
        landlord = Landlord(**landlordData)
    
    monad = await repository.insert(landlord)
    assert monad.error_status == {"status": 502, "reason": "Failed to connect to database"}

