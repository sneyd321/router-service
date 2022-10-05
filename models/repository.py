from models.request import Request
from models.monad import MaybeMonad
from models.cloud_run import CloudRun
import aiohttp

class HouseRepsository:

    def __init__(self):
        self.cloudRun = CloudRun()
        self.cloudRun.initialize()

    async def insert_house(self, landlordId): 
        hostname = self.cloudRun.get_house_hostname()
        if not hostname:
            return MaybeMonad(errors={"status_code": 503, "Error": "Failed to connect to house service"})

        request = Request(hostname, f"/House")
        monad = MaybeMonad({
            "homeownerId": landlordId
        })
        monad = await monad.bind(request.post)
        return monad

    
    async def get_house(self, landlordId):
        hostname = self.cloudRun.get_house_hostname()
        if not hostname:
            return MaybeMonad(errors={"status_code": 503, "Error": "Failed to connect to house service"})

        try:
            request = Request(hostname, f"/Landlord/{landlordId}/House")
            houseData = await request.get()
            return MaybeMonad(data=houseData)
        except aiohttp.client_exceptions.ClientConnectorError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Failed to connect downstream service"})
        except aiohttp.ClientResponseError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Recieved invalid downstream response"})
        except ConnectionError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Failed to connect downstream service"})

    async def get_house_by_house_key(self, houseKey):
        hostname = self.cloudRun.get_house_hostname()
        if not hostname:
            return MaybeMonad(errors={"status_code": 503, "Error": "Failed to connect to house service"})

        try:
            request = Request(hostname, f"/House/{houseKey}")
            houseData = await request.get()
            return MaybeMonad(data=houseData)
        except aiohttp.client_exceptions.ClientConnectorError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Failed to connect downstream service"})
        except aiohttp.ClientResponseError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Recieved invalid downstream response"})
        except ConnectionError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Failed to connect downstream service"})


class LeaseRepository:

    def __init__(self):
        self.cloudRun = CloudRun()
        self.cloudRun.initialize()

    async def insert_lease(self, houseId, leaseInput):
        #Get lease service
        hostname = self.cloudRun.get_lease_hostname()
        if not hostname:
            return MaybeMonad(errors={"status_code": 503, "Error": "Failed to connect to lease service"})
        
        request = Request(hostname, f"/House/{houseId}/Lease")
        monad = MaybeMonad(leaseInput)
        monad = await monad.bind(request.post)
        return monad

    async def get_lease_by_houseIds(self, houseIds):
        hostname = self.cloudRun.get_lease_hostname()
        if not hostname:
            return MaybeMonad(errors={"status_code": 503, "Error": "Failed to connect to lease service"})
        houseIdQuery = ",".join(houseIds)
        request = Request(hostname, f"/Lease?houses={houseIdQuery}")
        try:
            leaseData = await request.get()
            return MaybeMonad(data=leaseData)
        except aiohttp.client_exceptions.ClientConnectorError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Failed to connect downstream service"})
        except aiohttp.ClientResponseError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Recieved invalid downstream response"})
        except ConnectionError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Failed to connect downstream service"})

    async def update(self, leaseId, inputType, resourceName):
        #Get lease service
        hostname = self.cloudRun.get_lease_hostname()
        if not hostname:
            return MaybeMonad(errors={"status_code": 503, "Error": "Failed to connect to lease service"})
        
        request = Request(hostname, f"/Lease/{leaseId}/{resourceName}")
        monad = MaybeMonad(inputType)
        monad = await monad.bind(request.put)
        return monad

    
class SchedulerRepository:

    def __init__(self):
        self.cloudRun = CloudRun()
        self.cloudRun.initialize()

    async def schedule_lease(self, leaseData):
        #Get lease service
        hostname = self.cloudRun.get_scheduler_hostname()
        if not hostname:
            return MaybeMonad(errors={"status_code": 503, "Error": "Failed to connect to scheduler"})
        
        request = Request(hostname, f"/Lease")
        monad = MaybeMonad(leaseData)
        monad = await monad.bind(request.post)
        return monad

    async def schedule_maintenance_ticket_upload(self, houseKey, firebaseId, maintenanceTicket, image):
        #Get lease service
        hostname = self.cloudRun.get_scheduler_hostname()
        if not hostname:
            return MaybeMonad(errors={"status_code": 503, "Error": "Failed to connect to scheduler"})
        
        request = Request(hostname, f"/MaintenanceTicket")
        monad = MaybeMonad({
                'firebaseId': firebaseId,
                'imageURL': maintenanceTicket.imageURL,
                'houseKey': houseKey,
                'maintenanceTicketId': maintenanceTicket.id,
                'description': maintenanceTicket.description.descriptionText,
                'firstName': maintenanceTicket.sender.firstName,
                'lastName': maintenanceTicket.sender.lastName,
                'image': image
            })
        monad = await monad.bind(request.post)
        return monad

    async def schedule_add_tenant_email(self, firstName, lastName, email, house, deviceId):
        #Get lease service
        hostname = self.cloudRun.get_scheduler_hostname()
        if not hostname:
            return MaybeMonad(errors={"status_code": 503, "Error": "Failed to connect to scheduler"})
        
        request = Request(hostname, f"/AddTenantEmail")
        monad = MaybeMonad({
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "houseKey": house.houseKey,
            "documentURL": house.lease.documentURL,
            "firebaseId": house.firebaseId,
            "deviceId": deviceId
        })
        monad = await monad.bind(request.post)
        return monad

    async def schedule_sign_lease(self, tenant, firebaseId, documentURL, signiture, deviceId):
        #Get lease service
        hostname = self.cloudRun.get_scheduler_hostname()
        if not hostname:
            return MaybeMonad(errors={"status_code": 503, "Error": "Failed to connect to scheduler"})
        
        request = Request(hostname, f"/SignLease")
        monad = MaybeMonad({
            "firstName": tenant.firstName,
            "lastName": tenant.lastName,
            "email": tenant.email,
            "documentURL": documentURL,
            "tenantPosition": tenant.tenantPosition,
            "tenantState": tenant.tenantState,
            "signiture": signiture,
            "firebaseId": firebaseId,
            "deviceId": deviceId
        })
        monad = await monad.bind(request.post)
        return monad


class MaintenanceTicketRepository:


    def __init__(self):
        self.cloudRun = CloudRun()
        self.cloudRun.initialize()

    async def create_maintenance_ticket(self, houseId, maintenanceTicketData):
        hostname = self.cloudRun.get_maintenance_ticket_hostname()
        if not hostname:
            return MaybeMonad(errors={"status_code": 503, "Error": "Failed to connect to maintenance ticket service"})
        maintenanceTicketData["houseId"] = houseId
        request = Request(hostname, f"/MaintenanceTicket")
        monad = MaybeMonad(maintenanceTicketData)
        monad = await monad.bind(request.post)
        return monad

    async def get_maintenance_ticket_by_id(self, maintenanceTicketId):
        hostname = self.cloudRun.get_maintenance_ticket_hostname()
        if not hostname:
            return MaybeMonad(errors={"status_code": 503, "Error": "Failed to connect to maintenance ticket service"})
        
        try:
            request = Request(hostname, f"/MaintenanceTicket/{maintenanceTicketId}")
            maintenanceTicketData = await request.get()
            return MaybeMonad(data=maintenanceTicketData)
        except aiohttp.client_exceptions.ClientConnectorError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Failed to connect downstream service"})
        except aiohttp.ClientResponseError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Recieved invalid downstream response"})
        except ConnectionError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Failed to connect downstream service"})



class TenantRepository:

    def __init__(self):
        self.cloudRun = CloudRun()
        self.cloudRun.initialize() 

    async def create_tenant(self, tenantData, houseId):
        hostname = self.cloudRun.get_tenant_hostname()
        if not hostname:
            return MaybeMonad(errors={"status_code": 503, "Error": "Failed to connect to tenant service"})
        
        request = Request(hostname, f"/Tenant/{houseId}")
        monad = MaybeMonad(tenantData)
        monad = await monad.bind(request.post)
        return monad

    async def login(self, houseId, email, password, deviceId):
        hostname = self.cloudRun.get_tenant_hostname()
        if not hostname:
            return MaybeMonad(errors={"status_code": 503, "Error": "Failed to connect to tenant service"})
        
        request = Request(hostname, f"/Login")
        monad = MaybeMonad({
            "email": email,
            "password": password,
            "houseId": houseId,
            "deviceId": deviceId
        })
        monad = await monad.bind(request.post)
        return monad

    async def get_tenants_by_house_id(self, houseId):
        hostname = self.cloudRun.get_tenant_hostname()
        if not hostname:
            return MaybeMonad(errors={"status_code": 503, "Error": "Failed to connect to tenant service"})
        try:
            request = Request(hostname, f"/House/{houseId}/Tenant")
            return MaybeMonad(data=await request.get())
        except aiohttp.client_exceptions.ClientConnectorError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Failed to connect downstream service"})
        except aiohttp.ClientResponseError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Recieved invalid downstream response"})
        except ConnectionError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Failed to connect downstream service"})



class LandlordRepository:
    def __init__(self):
            self.cloudRun = CloudRun()
            self.cloudRun.initialize() 

    async def create_landlord(self, landlordData):
        hostname = self.cloudRun.get_landlord_hostname()
        if not hostname:
            return MaybeMonad(errors={"status_code": 503, "Error": "Failed to connect to landlord service"})
        
        request = Request(hostname, f"/Landlord")
        monad = MaybeMonad(landlordData)
        monad = await monad.bind(request.post)
        return monad

    async def login(self, email, password, deviceId):
        hostname = self.cloudRun.get_landlord_hostname()
        if not hostname:
            return MaybeMonad(errors={"status_code": 503, "Error": "Failed to connect to landlord service"})
        
        request = Request(hostname, f"/Login")
        monad = MaybeMonad({
            "email": email,
            "password": password,
            "deviceId": deviceId
        })
        monad = await monad.bind(request.post)
        return monad

    async def get_landlord_by_landlord_id(self, landlordId):
        hostname = self.cloudRun.get_landlord_hostname()
        if not hostname:
            return MaybeMonad(errors={"status_code": 503, "Error": "Failed to connect to tenant service"})
        try:
            request = Request(hostname, f"/Landlord/{landlordId}")
            return MaybeMonad(data=await request.get())
        except aiohttp.client_exceptions.ClientConnectorError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Failed to connect downstream service"})
        except aiohttp.ClientResponseError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Recieved invalid downstream response"})
        except ConnectionError:
            return MaybeMonad(result=None, errors={"status_code": 502, "Error": "Failed to connect downstream service"})
