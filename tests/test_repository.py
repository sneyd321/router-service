from models.repository import Repository
from models.request import Request
import aiohttp

repository = Repository()

async def test_Router_returns_error_when_house_service_insert_returns_non_json_data():
    async with aiohttp.ClientSession() as session:
        request = Request("https://0b008cd5-f83f-40f0-90e8-3c676e55b481.mock.pstmn.io", "/Landlord/1/House")
        request.set_session(session)
        monad = await repository.get(request)
        assert monad.error_status == {"status": 502, "reason": "Recieved invalid downstream response"}

async def test_Router_returns_error_when_a_500_response_is_returned_on_insert():
    async with aiohttp.ClientSession() as session:
        request = Request("https://0b008cd5-f83f-40f0-90e8-3c676e55b481.mock.pstmn.io", "/House")
        request.set_session(session)
        monad = await repository.post(request, landlordId=1)
        assert monad.error_status == {"status": 500, "reason": "An unexpected error occured"}

async def test_Router_returns_error_when_a_422_response_is_returned_on_insert():
    async with aiohttp.ClientSession() as session:
        request = Request("https://0b008cd5-f83f-40f0-90e8-3c676e55b481.mock.pstmn.io", "/House-422")
        request.set_session(session)
        monad = await repository.post(request, **{
            "lanvcxvcxdlordId": "1"
        })
        assert monad.error_status == {"status": 422, "reason": "[{'loc': ['body', 'landlordId'], 'msg': 'field required', 'type': 'value_error.missing'}]"}

