from models.request import Request
from models.monad import RequestMaybeMonad
import aiohttp

class Repository:

    def __init__(self, cloudRun):
        self.cloudRun = cloudRun

    async def post(self, request, **kwargs): 
        return await RequestMaybeMonad(kwargs) \
            .bind_data(request.post)
   
    async def put(self, request, **kwargs): 
        return await RequestMaybeMonad(kwargs) \
            .bind_data(request.put)

    async def put_list(self, request, *args): 
        return await RequestMaybeMonad(args) \
            .bind_data(request.put)
  
    async def get(self, request):
        return await RequestMaybeMonad() \
            .bind_data(request.get)
        
class TenantRepository(Repository):

    def __init__(self, cloudRun):
        Repository.__init__(self, cloudRun)
    
    async def create_tenant(self, session, houseId, tenant):
        request = Request(self.cloudRun.get_tenant_hostname(), f"/Tenant")
        request.set_session(session)
        return await self.post(request, houseId=houseId, **tenant.__dict__)
        
    async def login(self, session, houseId, login):
        request = Request(self.cloudRun.get_tenant_hostname(), f"/Login")
        request.set_session(session)
        return await self.post(request, houseId=houseId, **login.__dict__)

    async def get_tenants_by_house_id(self, session, houseId):
        request = Request(self.cloudRun.get_tenant_hostname(), f"/House/{houseId}/Tenant")
        request.set_session(session)
        return await self.get(request)
       

class LandlordRepository(Repository):

    def __init__(self, cloudRun):
        Repository.__init__(self, cloudRun)

    async def create_landlord(self, session, landlord):
        request = Request(self.cloudRun.get_landlord_hostname(), "/Landlord")
        request.set_session(session)
        return await self.post(request, **landlord.__dict__)

    async def login(self, session, login):
        request = Request(self.cloudRun.get_landlord_hostname(), "/Login")
        request.set_session(session)
        return await self.post(request, **login.__dict__)

    async def get_landlord_by_id(self, session, landlordId):
        request = Request(self.cloudRun.get_landlord_hostname(), f"/Landlord/{landlordId}")
        request.set_session(session)
        return await self.get(request)


class HouseRepository(Repository):

    def __init__(self, cloudRun):
        Repository.__init__(self, cloudRun)

    async def create_house(self, session, landlordId):
        request = Request(self.cloudRun.get_house_hostname(), f"/House")
        request.set_session(session)
        return await self.post(request, **{"landlordId": landlordId})


    async def get_houses(self, session, landlordId):
        request = Request(self.cloudRun.get_house_hostname(), f"/Landlord/{landlordId}/House")
        request.set_session(session)
        return await self.get(request)
      

    async def get_house_by_house_key(self, session, houseKey) :
        request = Request(self.cloudRun.get_house_hostname(), f"/House/{houseKey}")
        request.set_session(session)
        return await self.get(request)
    
class MaintenanceTicketRepository(Repository):

    def __init__(self, cloudRun):
        Repository.__init__(self, cloudRun)

    async def get_maintenance_tickets(self, session, houseId):
        request = Request(self.cloudRun.get_maintenance_ticket_hostname(), f"/House/{houseId}/MaintenanceTicket")
        request.set_session(session)
        return await self.get(request)

    async def get_maintenance_tickets_by_house_key(self, session, houseId, maintenanceTicketId):
        request = Request(self.cloudRun.get_maintenance_ticket_hostname(), f"/House/{houseId}/MaintenanceTicket?query={maintenanceTicketId}")
        request.set_session(session)
        return await self.get(request)

    async def create_maintenance_ticket(self, session, houseId, maintenanceTicket):
        request = Request(self.cloudRun.get_maintenance_ticket_hostname(), f"/MaintenanceTicket")
        request.set_session(session)
        maintenanceTicket.houseId = houseId
        return await self.post(request, **maintenanceTicket.__dict__)
        

class SchedulerRepository(Repository):

    def __init__(self, cloudRun):
        Repository.__init__(self, cloudRun)

    async def schedule_maintenance_ticket_upload(self, house, maintenanceTicket, image):
        request = Request(self.cloudRun.get_scheduler_hostname(), "/MaintenanceTicket")
        return await self.post(request, **{
            "firebaseId": maintenanceTicket.firebaseId,
            "imageURL": maintenanceTicket.imageURL,
            "houseKey": house.houseKey,
            "maintenanceTicketId": maintenanceTicket.id,
            "description": maintenanceTicket.description.descriptionText,
            "firstName": maintenanceTicket.sender.firstName,
            "lastName": maintenanceTicket.sender.lastName,
            "image": image
        })

        
    async def schedule_lease(self, house, lease):
        request = Request(self.cloudRun.get_scheduler_hostname(), "/Lease/Ontario")
        return await self.post(request **{
            "firebaseId": house.firebaseId,
            "lease": lease.to_json()
        })
        
    async def schedule_add_tenant_email(self, house, lease, tenant):
        request = Request(self.cloudRun.get_scheduler_hostname(), f"/AddTenantEmail")
        return await self.post(request, **{
            "firstName": tenant.firstName,
            "lastName": tenant.lastName,
            "email": tenant.email,
            "houseKey": house.houseKey,
            "documentURL": lease.documentURL,
            "firebaseId": house.firebaseId,
        })
    
    async def schedule_sign_lease(self, tenant, house, documentURL, signature):
        request = Request(self.cloudRun.get_scheduler_hostname(), "/SignLease")
        return await self.post(request, **{
            "firstName": tenant.firstName,
            "lastName": tenant.lastName,
            "email": tenant.email,
            "documentURL": documentURL,
            "tenantPosition": tenant.tenantPosition,
            "tenantState": tenant.tenantState,
            "signiture": signature,
            "firebaseId": house.firebaseId,
        })
       

class LeaseRepository(Repository):

    def __init__(self, cloudRun):
        Repository.__init__(self, cloudRun)

    async def create_lease(self, session, houseId, lease):
        request = Request(self.cloudRun.get_lease_hostname(), f"/House/{houseId}/Lease")
        request.set_session(session)
        return await self.post(request, **lease.__dict__)

    async def get_lease_by_houseIds(self, session, houseIds):
        houseIdsAsString = [str(item) for item in houseIds]
        request = Request(self.cloudRun.get_lease_hostname(), f"/Lease?houses={','.join(houseIdsAsString)}")
        request.set_session(session)
        return await self.get(request)

    
    async def update_landlord_info(self, session, leaseId, landlordInfo):
        request = Request(self.cloudRun.get_lease_hostname(), f"/Lease/{leaseId}/LandlordInfo")
        request.set_session(session)
        return await self.put(request, **landlordInfo.__dict__)


    async def update_landlord_address(self, session, leaseId, landlordAddress):
        request = Request(self.cloudRun.get_lease_hostname(), f"/Lease/{leaseId}/LandlordAddress")
        request.set_session(session)
        return await self.put(request, **landlordAddress.__dict__)

    async def update_rental_address(self, session, leaseId, rentalAddress):
        request = Request(self.cloudRun.get_lease_hostname(), f"/Lease/{leaseId}/RentalAddress")
        request.set_session(session)
        return await self.put(request, **rentalAddress.__dict__)
    
    async def update_rent(self, session, leaseId, rent):
        request = Request(self.cloudRun.get_lease_hostname(), f"/Lease/{leaseId}/Rent")
        request.set_session(session)
        return await self.put(request, **rent.__dict__)
    
    async def update_tenancy_terms(self, session, leaseId, tenancyTerms):
        request = Request(self.cloudRun.get_lease_hostname(), f"/Lease/{leaseId}/TenancyTerms")
        request.set_session(session)
        return await self.put(request, **tenancyTerms.__dict__)

    async def update_services(self, session, leaseId, services):
        request = Request(self.cloudRun.get_lease_hostname(), f"/Lease/{leaseId}/Services")
        request.set_session(session)
        return await self.put_list(request, *[service.__dict__ for service in services])

    async def update_utilities(self, session, leaseId, utililties):
        request = Request(self.cloudRun.get_lease_hostname(), f"/Lease/{leaseId}/Utilities")
        request.set_session(session)
        return await self.put_list(request, *[utility.__dict__ for utility in utililties])

    async def udpate_rent_discounts(self, session, leaseId, rentDiscounts):
        request = Request(self.cloudRun.get_lease_hostname(), f"/Lease/{leaseId}/RentDiscounts")
        request.set_session(session)
        return await self.put_list(request, *[rentDiscount.__dict__ for rentDiscount in rentDiscounts])

    async def udpate_rent_deposits(self, session, leaseId, rentDeposits):
        request = Request(self.cloudRun.get_lease_hostname(), f"/Lease/{leaseId}/RentDeposits")
        request.set_session(session)
        return await self.put_list(request, *[rentDeposit.__dict__ for rentDeposit in rentDeposits])

    async def udpate_additional_terms(self, session, leaseId, additionalTerms):
        request = Request(self.cloudRun.get_lease_hostname(), f"/Lease/{leaseId}/AdditionalTerms")
        request.set_session(session)
        return await self.put_list(request, *[additionalTerm.__dict__ for additionalTerm in additionalTerms])

