from models.repository import Repository
from models.request import Request
from models.cloud_run import CloudRun


async def test_Router_insert_house_returns_successfully():
    cloudRun = CloudRun()
    cloudRun.discover_dev()
    request = Request(cloudRun.get_house_hostname(), "/House")
    repository = Repository(request)
    monad = await repository.insert(landlordId=1)
    assert list(monad.get_param_at(0).keys()) == ['id', 'landlordId', 'houseKey', 'firebaseId']

async def test_Router_get_house_by_landlord_id_returns_successfully():
    cloudRun = CloudRun()
    cloudRun.discover_dev()
    request = Request(cloudRun.get_house_hostname(), "/House")
    repository = Repository(request)
    monad = await repository.insert(landlordId=2)

    request = Request(cloudRun.get_house_hostname(), "/Landlord/1/House")
    repository = Repository(request)
    monad = await repository.get()
    assert len(monad.get_param_at(0)) > 0

async def test_Router_get_house_by_house_key_returns_successfully():
    cloudRun = CloudRun()
    cloudRun.discover_dev()
    request = Request(cloudRun.get_house_hostname(), "/House")
    repository = Repository(request)
    monad = await repository.insert(landlordId=3)
    house = monad.get_param_at(0)
    print(house['houseKey'])

    request = Request(cloudRun.get_house_hostname(), f"/House/{house['houseKey']}")
    repository = Repository(request)
    monad = await repository.get()
    assert list(monad.get_param_at(0).keys()) == ['id', 'landlordId', 'houseKey', 'firebaseId']