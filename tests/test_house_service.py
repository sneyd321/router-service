from models.repository import HouseRepository
from models.request import Request
from models.cloud_run import CloudRun
import aiohttp

cloudRun = CloudRun()
#cloudRun.discover_dev()
cloudRun.discover()
houseRepository = HouseRepository(cloudRun.get_house_test_hostname())

async def test_Router_insert_house_returns_successfully():
    async with aiohttp.ClientSession() as session:
        monad = await houseRepository.create_house(session, 1)
        assert list(monad.get_param_at(0).keys()) == ['id', 'landlordId', 'houseKey', 'firebaseId']

async def test_Router_get_house_by_landlord_id_returns_successfully():
     async with aiohttp.ClientSession() as session:
        monad = await houseRepository.create_house(session, 1)
        monad = await houseRepository.get_houses(session, 1)
        assert len(monad.get_param_at(0)) > 0

async def test_Router_get_house_by_house_key_returns_successfully():
    async with aiohttp.ClientSession() as session:
        monad = await houseRepository.create_house(session, 1)
        house = monad.get_param_at(0)
        monad = await houseRepository.get_house_by_house_key(session, house['houseKey'])
        assert list(monad.get_param_at(0).keys()) == ['id', 'landlordId', 'houseKey', 'firebaseId']