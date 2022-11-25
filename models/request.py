import aiohttp
import asyncio



class Request:

    def __init__(self, hostname, resourcePath, **kwargs):
        self.hostname = hostname
        self.resourcePath = resourcePath

    def create_new_session(self):
        self.session = aiohttp.ClientSession()

    def set_session(self, session):
        self.session = session

    async def determine_response(self, response):
        print(response.status)
        
        if response.status == 500:
            return { "status_code": 500, "detail": "An unexpected error occured" }

        data = await response.json()
        print(data)
        if response.status == 422:
            return { "status_code": 422, "detail": str(data["detail"]) }
        if response.status == 409:
            return { "status_code": 409, "detail": str(data["detail"]) }
        if response.status == 404:
            return { "status_code": 404, "detail": str(data["detail"]) }
        if response.status == 401:
            return { "status_code": 401, "detail": str(data["detail"]) }
        if response.status == 405:
            return { "status_code": 405, "detail": str(data["detail"]) }
        return await response.json()


    async def get(self):
        response = await self.session.get(self.hostname + self.resourcePath)
        return await self.determine_response(response)

    async def post(self, payload):
        response = await self.session.post(self.hostname + self.resourcePath, json=payload)
        return await self.determine_response(response)
                
    async def put(self, payload):
        response = await self.session.put(self.hostname + self.resourcePath, json=payload)
        return await self.determine_response(response)

    async def delete(self, payload):
        response = await self.session.delete(self.hostname + self.resourcePath,json=payload)
        return await self.determine_response(response)

    async def deleteNoBody(self):
        response = await self.session.delete(self.hostname + self.resourcePath)
        return await self.determine_response(response)

   


