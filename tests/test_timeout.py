from models.repository import HouseRepsository
from models.request import Request
from models.cloud_run import CloudRun


async def test_Router_returns_error_when_fails_to_connect_to_house_service():
    cloudRun = CloudRun()
    cloudRun.discover_dev()
    request = Request(cloudRun.get_house_hostname(), "/House")
    repository = HouseRepsository(request)
    monad = await repository.insert_house(landlordId=1)
    assert monad.error_status == {"status": 408, "reason": "Failed to connect downstream service"}

