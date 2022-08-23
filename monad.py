import aiohttp
import asyncio

class MaybeMonad:

    def __init__(self, data = None, result=None, errors = None):
        self.data = data
        self.result = result
        self.errors = errors
        
    async def bind(self, function):
        try:
            self.result = await function(self.data)
            return MaybeMonad(data=self.data, result=self.result)
        except aiohttp.client_exceptions.ClientConnectorError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Failed to connect downstream service"})
        except aiohttp.ClientResponseError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Recieved invalid downstream response"})
        except ConnectionError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Failed to connect downstream service"})
 
