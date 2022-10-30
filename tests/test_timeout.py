from models.repository import HouseRepository
from models.request import Request
from models.cloud_run import CloudRun

import aiohttp

cloudRun = CloudRun()
cloudRun.discover_dev()

async def test_Router_returns_error_when_fails_to_connect_to_house_service():
    async with aiohttp.ClientSession() as session:
        repository = HouseRepository(cloudRun.get_house_hostname())
        monad = await repository.create_house(session, landlordId=1)
        assert monad.error_status == {"status": 408, "reason": "Failed to connect downstream service"}

