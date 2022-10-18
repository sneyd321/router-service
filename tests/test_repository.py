from models.repository import Repository
from models.request import Request
from models.cloud_run import CloudRun


async def test_Router_returns_error_when_house_service_insert_returns_non_json_data():
    request = Request("https://0b008cd5-f83f-40f0-90e8-3c676e55b481.mock.pstmn.io", "/Landlord/1/House")
    repository = Repository(request)
    monad = await repository.get()
    assert monad.error_status == {"status": 502, "reason": "Recieved invalid downstream response"}

async def test_Router_returns_error_when_a_500_response_is_returned_on_insert():
    request = Request("https://0b008cd5-f83f-40f0-90e8-3c676e55b481.mock.pstmn.io", "/House")
    repository = Repository(request)
    monad = await repository.insert(landlordId=1)
    assert monad.error_status == {"status": 500, "reason": "An unexpected error occured"}

async def test_Router_returns_error_when_a_422_response_is_returned_on_insert():
    cloudRun = CloudRun()
    cloudRun.discover_dev()
    request = Request(cloudRun.get_house_hostname(), "/House")
    repository = Repository(request)
    monad = await repository.insert(landlordId=None)
    assert monad.error_status == {"status": 422, "reason": "[{'loc': ['body', 'landlordId'], 'msg': 'none is not an allowed value', 'type': 'type_error.none.not_allowed'}]"}

