import aiohttp
import asyncio

class Request:

    def __init__(self, hostname, resourcePath, payload=None):
        self.hostname = hostname
        self.resourcePath = resourcePath
        self.payload = payload


    async def get(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.hostname + self.resourcePath) as response:
                payload = await response.json()
                if "status_code" in payload:
                    print(payload)
                    raise ConnectionError
                return payload


    async def post(self, payload):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.hostname + self.resourcePath, json=payload) as response:
                payload = await response.json()
                if "status_code" in payload:
                    print(payload)
                    raise ConnectionError
                return payload

    async def put(self, payload):
        async with aiohttp.ClientSession() as session:
            async with session.put(self.hostname + self.resourcePath, json=payload) as response:
                payload = await response.json()

                if "status_code" in payload:
                    print(payload)
                    raise ConnectionError
                return payload


