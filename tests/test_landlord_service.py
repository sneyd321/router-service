from models.repository import LandlordRepository
from models.request import Request
from models.cloud_run import CloudRun
from models.graphql_inputs import LandlordInput, LoginLandlordInput

import aiohttp, uuid, pytest, json

cloudRun = CloudRun()
cloudRun.discover_dev()

#cloudRun.discover()
repository = LandlordRepository(cloudRun.get_landlord_hostname())

async def test_Router_create_landlord_returns_successfully():
    async with aiohttp.ClientSession() as session:
        with open("./tests/samples/create_landlord.json", mode="r") as create_landlord:
            landlordData = json.load(create_landlord)
            landlordData["email"] = str(uuid.uuid4())
        monad = await repository.create_landlord(session, landlordData)
        print(monad.error_status)
        assert not monad.has_errors()



async def test_Router_landlord_login_returns_successfully():
    email = str(uuid.uuid4())
    async with aiohttp.ClientSession() as session:
        with open("./tests/samples/create_landlord.json", mode="r") as create_landlord:
            landlordData = json.load(create_landlord)
            landlordData["email"] = email
        await repository.create_landlord(session, landlordData) 
        with open("./tests/samples/landlord_login.json", mode="r") as landlord_login:
            loginData = json.load(landlord_login)
            loginData["email"] = email
        monad = await repository.login(session, loginData)
        print(monad.error_status)
        assert not monad.has_errors()


async def test_Router_get_landlord_by_id_returns_successfully():
    email = str(uuid.uuid4())
    async with aiohttp.ClientSession() as session:
        with open("./tests/samples/create_landlord.json", mode="r") as create_landlord:
            landlordData = json.load(create_landlord)
            landlordData["email"] = email
        monad = await repository.create_landlord(session, landlordData) 
        with open("./tests/samples/landlord_login.json", mode="r") as landlord_login:
            loginData = json.load(landlord_login)
            loginData["email"] = email
        landlordId = monad.get_param_at(0)["id"]
        monad = await repository.get_landlord_by_id(session, f"/Landlord/{landlordId}", landlordId)
        print(monad.error_status)
        assert not monad.has_errors()


async def test_Router_get_landlord_by_id_returns_successfully():
    email = str(uuid.uuid4())
    async with aiohttp.ClientSession() as session:
        with open("./tests/samples/create_landlord.json", mode="r") as create_landlord:
            landlordData = json.load(create_landlord)
            landlordData["email"] = email
        monad = await repository.create_landlord(session, landlordData) 
        with open("./tests/samples/landlord_login.json", mode="r") as landlord_login:
            loginData = json.load(landlord_login)
            loginData["email"] = email
        landlordId = monad.get_param_at(0)["id"]
        monad = await repository.get_landlord_by_id(session, f"/Landlord/{landlordId}", landlordId)
        print(monad.error_status)
        assert not monad.has_errors()

async def test_Router_delete_landlord_returns_successfully():
    email = str(uuid.uuid4())
    async with aiohttp.ClientSession() as session:
        with open("./tests/samples/create_landlord.json", mode="r") as create_landlord:
            landlordData = json.load(create_landlord)
            landlordData["email"] = email
        monad = await repository.create_landlord(session, landlordData) 

        with open("./tests/samples/landlord.json", mode="r") as landlord:
            landlordData = json.load(landlord)
            landlordData["email"] = email
        landlordId = monad.get_param_at(0)["id"]
        monad = await repository.delete_landlord(session, f"/Landlord", landlordData)
        print(monad.error_status)
        assert not monad.has_errors()

async def test_Router_update_landlord_returns_successfully():
    email = str(uuid.uuid4())
    async with aiohttp.ClientSession() as session:
        with open("./tests/samples/create_landlord.json", mode="r") as create_landlord:
            landlordData = json.load(create_landlord)
            landlordData["email"] = email
        monad = await repository.create_landlord(session, landlordData) 

        with open("./tests/samples/landlord.json", mode="r") as landlord:
            landlordData = json.load(landlord)
            landlordData["email"] = email
        landlordId = monad.get_param_at(0)["id"]
        monad = await repository.update_landlord(session, f"/Landlord", landlordData)
        print(monad.error_status)
        assert not monad.has_errors()
    
    
