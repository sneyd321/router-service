from models.repository import LandlordRepository
from models.request import Request
from models.cloud_run import CloudRun
from models.graphql_inputs import LandlordInput, LoginLandlordInput

import aiohttp, uuid

cloudRun = CloudRun()
#cloudRun.discover_dev()

cloudRun.discover()
repository = LandlordRepository(cloudRun.get_landlord_test_hostname())

async def test_Router_insert_landlord_returns_successfully():
    async with aiohttp.ClientSession() as session:
        landlord = LandlordInput(**{
            "firstName": "Ryan",
            "lastName": "Sneyd",
            "email": f"{uuid.uuid4()}@s.com",
            "password": "aaaaaa"
        })
        monad = await repository.create_landlord(session, landlord)
        print(monad.error_status)
        assert list(monad.get_param_at(0).keys()) == ['id', 'firstName', 'lastName', 'email', 'deviceId']

async def test_Router_insert_landlord_returns_conflict_error_on_duplicate_email():
    async with aiohttp.ClientSession() as session:
        landlord = LandlordInput(**{
            "firstName": "Ryan",
            "lastName": "Sneyd",
            "email": "aaa@s.com",
            "password": "aaaaaa"
        })
        monad = await repository.create_landlord(session, landlord) 
        monad = await repository.create_landlord(session, landlord) 
        assert monad.error_status == {"status": 409, "reason": "Failed to insert data into database" }

async def test_Router_landlord_login_returns_successfully():
    async with aiohttp.ClientSession() as session:
        landlord = LandlordInput(**{
            "firstName": "Ryan",
            "lastName": "Sneyd",
            "email": "aaaa@s.com",
            "password": "aaaaaa"
        })
        await repository.create_landlord(session, landlord) 
        login = LoginLandlordInput(**{
            "email": "aaaa@s.com",
            "password": "aaaaaa",
            "deviceId": "abc"
        })
        monad = await repository.login(session, login)
        assert list(monad.get_param_at(0).keys()) == ['id', 'firstName', 'lastName', 'email', 'deviceId'] 


async def test_Router_landlord_login_returns_401_error():
    async with aiohttp.ClientSession() as session:
        landlord = LandlordInput(**{
        "firstName": "Ryan",
        "lastName": "Sneyd",
        "email": "aaaaa@s.com",
        "password": "aaaaaa"
        })
        await repository.create_landlord(session, landlord) 
        login = LoginLandlordInput(**{
            "email": "aaaaa@s.com",
            "password": "bbbbbb",
            "deviceId": "abc"
        })
        monad = await repository.login(session, login)
        assert monad.error_status == {"status": 401, "reason": "Invalid email or password" }



async def test_Router_landlord_login_returns_404_error():
     async with aiohttp.ClientSession() as session:
        login = LoginLandlordInput(**{
            "email": "bbbb@s.com",
            "password": "aaaaaa",
            "deviceId": "abc"
        })
        monad = await repository.login(session, login)
        assert monad.error_status == {"status": 404, "reason": "Invalid email or password" }


async def test_Router_get_landlord_by_id_returns_successfully():
    async with aiohttp.ClientSession() as session:
        landlord = LandlordInput(**{
            "firstName": "Ryan",
            "lastName": "Sneyd",
            "email": "aaaaa@s.com",
            "password": "aaaaaa"
        })
        monad = await repository.create_landlord(session, landlord) 
        monad = await repository.get_landlord_by_id(session, 1)
        assert monad.get_param_at(0) != None
    
