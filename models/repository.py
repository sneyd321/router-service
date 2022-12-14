from models.request import Request
from models.monad import RequestMaybeMonad
import aiohttp
from models.authorization import Authorization

import google.auth.transport.requests
import google.oauth2.id_token
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"./models/static/ServiceAccount.json"
auth = Authorization()

class Repository:

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

    async def delete(self, request, **kwargs): 
        return await RequestMaybeMonad(kwargs) \
            .bind_data(request.delete)

    async def deleteNoBody(self, request): 
        return await RequestMaybeMonad() \
            .bind_data(request.deleteNoBody)
        
class TenantRepository(Repository):

    def __init__(self, hostname):
        self.hostname = hostname
    
    async def create_temp_tenant(self, session, scopes, houseId, tenant, isTest=False):
        request = Request(self.hostname, f"/Tenant?isTest={isTest}")
        if "/Tenant" in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
          
            return await self.post(request, houseId=houseId, **tenant)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})

        
    async def login(self, session, houseId, login):
        request = Request(self.hostname, f"/Login")
        auth_req = google.auth.transport.requests.Request()
        id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
        session.headers["Authorization"] = f"Bearer {id_token}"
        request.set_session(session)
        return await self.post(request, houseId=houseId, **login)

    async def get_tenants_by_house_id(self, session, scopes, houseId):
        request = Request(self.hostname, f"/House/{houseId}/Tenant")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.get(request)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})

    async def update_tenant_state(self, session, scopes, tenantState, tenant):
        request = Request(self.hostname, f"/Tenant/{tenantState}")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
   
            return await self.put(request, **tenant)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})
    
    async def update_tenant(self, session, scopes, tenant):
        request = Request(self.hostname, f"/Tenant")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
         
            return await self.put(request, **tenant)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})
    

    async def delete_tenant(self, session, scopes, tenant):
        request = Request(self.hostname, f"/Tenant")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            tenant["state"] = ""
            tenant["deviceId"] = ""
            tenant["phoneNumber"] = ""
            tenant["profileURL"] = ""
            tenant["houseId"] = 0
            return await self.delete(request, **tenant)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})


class LandlordRepository(Repository):

    def __init__(self, hostname):
        self.hostname = hostname

    async def create_landlord(self, session, landlord):
        request = Request(self.hostname, "/Landlord")
        auth_req = google.auth.transport.requests.Request()
        id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
        session.headers["Authorization"] = f"Bearer {id_token}"
        request.set_session(session)
        return await self.post(request, **landlord)

    async def login(self, session, login):
        request = Request(self.hostname, "/Login")
        auth_req = google.auth.transport.requests.Request()
        id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
        session.headers["Authorization"] = f"Bearer {id_token}"
        request.set_session(session)
        return await self.post(request, **login)

    async def get_landlord_by_id(self, session, scopes, landlordId):
        request = Request(self.hostname, f"/Landlord/{landlordId}")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.get(request)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})
    
    async def delete_landlord(self, session, scopes, landlord):
        request = Request(self.hostname, f"/Landlord")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.delete(request, **landlord)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})

    async def update_landlord(self, session, scopes, landlord):
        request = Request(self.hostname, f"/Landlord")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.put(request, **landlord)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})




class HouseRepository(Repository):

    def __init__(self, hostname):
        self.hostname = hostname

    async def create_house(self, session, scopes, landlordId):
        request = Request(self.hostname, f"/House")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.post(request, **{"landlordId": landlordId})
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})

    async def createTenantNotification(self, session, scopes, firebaseId, houseKey, tenant):
        request = Request(self.hostname, f"/Notification/{firebaseId}/TenantAccountCreated")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            tenant["houseKey"] = houseKey
            return await self.post(request, **tenant)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})


    async def delete_house(self, session, scopes, houseId):
        request = Request(self.hostname, f"/House/{houseId}")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.deleteNoBody(request, **{})
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})


    async def get_houses(self, session, scopes, landlordId):
        request = Request(self.hostname, f"/Landlord/{landlordId}/House")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.get(request)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})
        

    async def get_house_by_house_key(self, session, scopes, houseKey) :
        request = Request(self.hostname, f"/House/{houseKey}")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.get(request)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})
    
class MaintenanceTicketRepository(Repository):

    def __init__(self, hostname):
        self.hostname = hostname

    async def get_maintenance_tickets(self, session, scopes, houseId):
        request = Request(self.hostname, f"/House/{houseId}/MaintenanceTicket")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.get(request)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})

    async def get_maintenance_ticket_by_id(self, session, scopes, houseId, maintenanceTicketId):
        request = Request(self.hostname, f"/House/{houseId}/MaintenanceTicket?query={maintenanceTicketId}")
        if f"/House/{houseId}/MaintenanceTicket" in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            
            return await self.get(request)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})

    async def create_maintenance_ticket(self, session, scopes, houseId, maintenanceTicket):
        request = Request(self.hostname, f"/MaintenanceTicket")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            maintenanceTicket["houseId"] = houseId
            return await self.post(request, **maintenanceTicket)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})
        

class SchedulerRepository(Repository):

    def __init__(self, hostname):
        self.hostname = hostname

    async def schedule_maintenance_ticket_upload(self, session, scopes, houseKey, firebaseId, maintenanceTicket, image):
        request = Request(self.hostname, "/MaintenanceTicket")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.post(request, **{
                "firebaseId": firebaseId,
                "imageURL": maintenanceTicket.imageURL,
                "houseKey": houseKey,
                "maintenanceTicketId": maintenanceTicket.id,
                "description": maintenanceTicket.description.descriptionText,
                "firstName": maintenanceTicket.sender.firstName,
                "lastName": maintenanceTicket.sender.lastName,
                "image": image
            })
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})


    async def schedule_tenant_profile_upload(self, session, scope, houseKey, imageURL, firebaseId, firstName, lastName, image):
        request = Request(self.hostname, "/Profile/Tenant")
        if request.resourcePath in scope:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.post(request, **{
                "firebaseId": firebaseId,
                "imageURL": imageURL,
                "houseKey": houseKey,
                "firstName": firstName,
                "lastName": lastName,
                "image": image
            })
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})


    async def schedule_landlord_profile_upload(self, session, scope, houseKey, imageURL, firstName, lastName, image):
        request = Request(self.hostname, "/Profile/Landlord")
        if request.resourcePath in scope:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.post(request, **{
                "firebaseId": "",
                "imageURL": imageURL,
                "houseKey": houseKey,
                "firstName": firstName,
                "lastName": lastName,
                "image": image
            })
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})


        
    async def schedule_lease(self, session, scopes, firebaseId, houseKey, lease, landlordAddress, signature):
        request = Request(self.hostname, "/Lease/Ontario")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            lease["landlordAddress"] = landlordAddress
            return await self.post(request, **{
                "firebaseId": firebaseId,
                "houseKey": houseKey,
                "lease": lease,
                "signature": signature
            })
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})
        
    async def schedule_add_tenant_email(self, session, scopes, houseKey, firebaseId, documentURL, tenant):
        request = Request(self.hostname, f"/AddTenantEmail")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.post(request, **{
                "firstName": tenant["firstName"],
                "lastName": tenant["lastName"],
                "email": tenant["email"],
                "houseKey": houseKey,
                "documentURL": documentURL,
                "firebaseId": firebaseId,
            })
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})
    
    async def schedule_sign_lease(self, session, scopes, tenant, tenantPosition, houseKey, firebaseId, documentURL, signature):
        request = Request(self.hostname, "/SignLease")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.post(request, **{
                "firstName": tenant.firstName,
                "lastName": tenant.lastName,
                "email": tenant.email,
                "houseKey": houseKey,
                "documentURL": documentURL,
                "tenantPosition": tenantPosition,
                "tenantState": "Approved",
                "signature": signature,
                "firebaseId": firebaseId,
            })
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})
        

class LeaseRepository(Repository):

    def __init__(self, hostname):
        self.hostname = hostname

    async def create_lease(self, session, scopes, houseId, lease):
        request = Request(self.hostname, f"/Lease")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            lease["houseId"] = houseId
            return await self.post(request, **lease)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})

    async def get_lease_by_houseId(self, session, scopes, houseId):
        request = Request(self.hostname, f"/Lease/{houseId}")
        auth_req = google.auth.transport.requests.Request()
        id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
        session.headers["Authorization"] = f"Bearer {id_token}"
        request.set_session(session)
        return await self.get(request)

    async def delete_lease_by_house_id(self, session, scopes, houseId):
        request = Request(self.hostname, f"/Lease/{houseId}")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.deleteNoBody(request)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})

    
    async def update_landlord_info(self, session, scopes, leaseId, landlordInfo):
        request = Request(self.hostname, f"/Lease/{leaseId}/LandlordInfo")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.put(request, **landlordInfo)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})


    async def update_landlord_address(self, session, scopes, leaseId, landlordAddress):
        request = Request(self.hostname, f"/Lease/{leaseId}/LandlordAddress")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.put(request, **landlordAddress)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})

    async def update_rental_address(self, session, scopes, leaseId, rentalAddress):
        request = Request(self.hostname, f"/Lease/{leaseId}/RentalAddress")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.put(request, **rentalAddress)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})
    
    async def update_rent(self, session, scopes, leaseId, rent):
        request = Request(self.hostname, f"/Lease/{leaseId}/Rent")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.put(request, **rent)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})
    
    async def update_tenancy_terms(self, session, scopes, leaseId, tenancyTerms):
        request = Request(self.hostname, f"/Lease/{leaseId}/TenancyTerms")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.put(request, **tenancyTerms)
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})

    async def update_services(self, session, scopes, leaseId, services):
        request = Request(self.hostname, f"/Lease/{leaseId}/Services")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.put_list(request, *[service.to_json() for service in services])
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})

    async def update_utilities(self, session, scopes, leaseId, utilities):
        request = Request(self.hostname, f"/Lease/{leaseId}/Utilities")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.put_list(request, *[utility.to_json() for utility in utilities])
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})

    async def udpate_rent_discounts(self, session, scopes, leaseId, rentDiscounts):
        request = Request(self.hostname, f"/Lease/{leaseId}/RentDiscounts")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.put_list(request, *[rentDiscount.to_json() for rentDiscount in rentDiscounts])
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})

    async def update_rent_deposits(self, session, scopes, leaseId, rentDeposits):
        request = Request(self.hostname, f"/Lease/{leaseId}/RentDeposits")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.put_list(request, *[rentDeposit.to_json() for rentDeposit in rentDeposits])
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})

    async def update_additional_terms(self, session, scopes, leaseId, additionalTerms):
        request = Request(self.hostname, f"/Lease/{leaseId}/AdditionalTerms")
        if request.resourcePath in scopes:
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(auth_req, self.hostname)
            session.headers["Authorization"] = f"Bearer {id_token}"
            request.set_session(session)
            return await self.put_list(request, *[additionalTerm.to_json() for additionalTerm in additionalTerms])
        return RequestMaybeMonad(None, error_status={"status": 403, "reason": f"Permission denied to access {request.resourcePath}"})
