import aiohttp
import asyncio
from collections.abc import Callable

class RequestMaybeMonad:
    def __init__(self, *data, error_status=None):
        self.data = data
        self.error_status = error_status

    def has_errors(self):
        return self.error_status is not None

    def get_param_at(self, position):
        return self.data[position]

    async def bind(self, function: Callable):
        """
        Calls a function with self.data as the parameter and returns a new instance of RepositoryMaybeMonad where self.data stays the same value. 
        Meant to be used with void functions
        """
        print(function.__name__, f"Data: {self.data}, Error Status: {self.error_status}")
        # If Tuple contains None
        if not all(self.data):
            if self.error_status is None:
                return RequestMaybeMonad(None, error_status={"status": 404, "reason": "No data in repository monad"})
            return RequestMaybeMonad(None, error_status=self.error_status)
        try:
            await function(*self.data)
            return RequestMaybeMonad(*self.data, error_status=self.error_status)
        except aiohttp.client_exceptions.ClientConnectorError:
            return RequestMaybeMonad(None, error_status={"status": 408, "reason": "Failed to connect downstream service"})
        except aiohttp.ClientResponseError:
            return RequestMaybeMonad(None, error_status={"status": 502, "reason": "Recieved invalid downstream response"})
        
        

    async def bind_data(self, function: Callable):
        """
        Calls a function with self.data as the parameter and returns a new instance of RepositoryMaybeMonad with self.data as the result of the function 
        Meant to be used with function that has a return value
        """
        print(function.__name__, f"Data: {self.data}, Error Status: {self.error_status}")
        # If Tuple contains None
        if not all(self.data):
            if self.error_status is None:
                return RequestMaybeMonad(None, error_status={"status": 404, "reason": "No data in repository monad"})
            return RequestMaybeMonad(None, error_status=self.error_status)
        try:
            result = await function(*self.data)
            if "status_code" in result and "detail" in result:
                return RequestMaybeMonad(None, error_status={"status": result["status_code"], "reason": result["detail"]})
            return RequestMaybeMonad(result, error_status=self.error_status)
        except aiohttp.client_exceptions.ClientConnectorError:
            return RequestMaybeMonad(None, error_status={"status": 408, "reason": "Failed to connect downstream service"})
        except aiohttp.ClientResponseError:
            return RequestMaybeMonad(None, error_status={"status": 502, "reason": "Recieved invalid downstream response"})
        