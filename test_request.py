from request import MaybeMonad, Request
import pytest, asyncio


def test_Validate_Request():
    request = Request()
    async def do_test():
        monad = await MaybeMonad(("http://localhost:8080/House/1/MaintenanceTicket")).bind(request.get)
        print(monad.errors)
        assert monad.errors == {"status_code": 502, "Error": "Failed to connect downstream service"}
    asyncio.run(do_test())