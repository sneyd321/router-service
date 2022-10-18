from models.repository import Repository
from models.request import Request
from models.cloud_run import CloudRun

cloudRun = CloudRun()
cloudRun.discover_dev()

async def test_Router_insert_landlord_returns_successfully():
    request = Request(cloudRun.get_landlord_hostname(), "/Landlord")
    repository = Repository(request)
    monad = await repository.insert(**{
        "firstName": "Ryan",
        "lastName": "Sneyd",
        "email": "aaa@s.com",
        "password": "aaaaaa"
    })
    assert list(monad.get_param_at(0).keys()) == ['id', 'firstName', 'lastName', 'email', 'deviceId']

async def test_Router_insert_landlord_returns_conflict_error_on_duplicate_email():

    request = Request(cloudRun.get_landlord_hostname(), "/Landlord")
    repository = Repository(request)
    monad = await repository.insert(**{
        "firstName": "Ryan",
        "lastName": "Sneyd",
        "email": "aaa@s.com",
        "password": "aaaaaa"
    })
    request = Request(cloudRun.get_landlord_hostname(), "/Landlord")
    repository = Repository(request)
    monad = await repository.insert(**{
        "firstName": "Ryan",
        "lastName": "Sneyd",
        "email": "aaa@s.com",
        "password": "aaaaaa"
    })
    assert monad.error_status == {"status": 409, "reason": "Failed to insert data into database" }

async def test_Router_landlord_login_returns_successfully():
    request = Request(cloudRun.get_landlord_hostname(), "/Landlord")
    repository = Repository(request)
    await repository.insert(**{
        "firstName": "Ryan",
        "lastName": "Sneyd",
        "email": "aaaa@s.com",
        "password": "aaaaaa"
    })
    request = Request(cloudRun.get_landlord_hostname(), "/Login")
    repository = Repository(request)
    monad = await repository.insert(**{
        "email": "aaaa@s.com",
        "password": "aaaaaa",
        "deviceId": "abc"
    })
    assert list(monad.get_param_at(0).keys()) == ['id', 'firstName', 'lastName', 'email', 'deviceId'] 


async def test_Router_landlord_login_returns_401_error():
    request = Request(cloudRun.get_landlord_hostname(), "/Landlord")
    repository = Repository(request)
    await repository.insert(**{
        "firstName": "Ryan",
        "lastName": "Sneyd",
        "email": "aaaaa@s.com",
        "password": "aaaaaa"
    })
    request = Request(cloudRun.get_landlord_hostname(), "/Login")
    repository = Repository(request)
    monad = await repository.insert(**{
        "email": "aaaa@s.com",
        "password": "bbbbbb",
        "deviceId": "abc"
    })
    assert monad.error_status == {"status": 401, "reason": "Invalid email or password" }



async def test_Router_landlord_login_returns_404_error():
    request = Request(cloudRun.get_landlord_hostname(), "/Login")
    repository = Repository(request)
    monad = await repository.insert(**{
        "email": "bbbb@s.com",
        "password": "aaaaaa",
        "deviceId": "abc"
    })
    assert monad.error_status == {"status": 404, "reason": "Invalid email or password" }


async def test_Router_get_landlord_by_id_returns_successfully():
    request = Request(cloudRun.get_landlord_hostname(), "/Landlord/1")
    repository = Repository(request)
    monad = await repository.get()
    assert monad.get_param_at(0) != None
