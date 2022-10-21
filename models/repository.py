from models.request import Request
from models.monad import RequestMaybeMonad
import aiohttp

class Repository:

    def __init__(self, request):
        self.request = request

    async def insert(self, **kwargs): 
        async with self.request.get_session() as session:
            return await RequestMaybeMonad(kwargs) \
                .bind_data(self.request.post)
            return monad
            
    async def get(self):
        async with self.request.get_session() as session:
            return await RequestMaybeMonad() \
                .bind_data(self.request.get)
        