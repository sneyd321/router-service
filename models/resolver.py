import strawberry
from typing import Optional, Union, List, AsyncGenerator
from strawberry.file_uploads import Upload
from strawberry.types import Info
from models.cloud_run import CloudRun
from models.monad import RequestMaybeMonad
from models.repository import MaintenanceTicketRepository, HouseRepository, LeaseRepository, SchedulerRepository, TenantRepository, LandlordRepository
from models.request import Request
from models.graphql_inputs import *
from models.graphql_types import *
from models.authorization import Authorization

import json, itertools, asyncio, base64, aiohttp

cloudRun = CloudRun()
#cloudRun.discover_dev()


cloudRun.discover()
maintenanceTicketRepository = MaintenanceTicketRepository(cloudRun.get_maintenance_ticket_hostname())
leaseRepository = LeaseRepository(cloudRun.get_lease_hostname())
schedulerRepository = SchedulerRepository(cloudRun.get_scheduler_hostname())
landlordRepository = LandlordRepository(cloudRun.get_landlord_hostname())
tenantRepository = TenantRepository(cloudRun.get_tenant_hostname())
houseRepository = HouseRepository(cloudRun.get_house_hostname())
auth = Authorization()


def get_auth_token_payload(info: Info):
    jwtToken = info.context["request"].headers.get("Authorization", None)
    info.context["response"].headers["Access-Control-Expose-Headers"] = "Authorization"
    if jwtToken is None:
        raise Exception("Missing Authorization header")
    info.context["response"].headers["Authorization"] = jwtToken[7:]

    tokenPayload = auth.get_token_payload(jwtToken[7:])
    if tokenPayload == {}:
        raise Exception("Session has expired")
    return tokenPayload


async def get_maintenance_tickets(houseId: int, info: Info) -> List[MaintenanceTicket]:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await maintenanceTicketRepository.get_maintenance_tickets(session, scope, houseId)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return [MaintenanceTicket(**data) for data in monad.get_param_at(0)]

async def get_maintenance_ticket_by_id(houseKey: str, maintenanceTicketId: int, info: Info) -> MaintenanceTicket:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await houseRepository.get_house_by_house_key(session, scope, houseKey)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        house = NewHouse(**monad.get_param_at(0))
        
        monad = await maintenanceTicketRepository.get_maintenance_ticket_by_id(session, scope, house.id, maintenanceTicketId)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return MaintenanceTicket(**monad.get_param_at(0))

async def add_maintenance_ticket(houseKey: str, maintenanceTicket: MaintenanceTicketInput, image: str, info: Info) -> MaintenanceTicket:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await houseRepository.get_house_by_house_key(session, scope, houseKey)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        
        house = NewHouse(**monad.get_param_at(0))
        monad = await maintenanceTicketRepository.create_maintenance_ticket(session, scope, house.id, maintenanceTicket.to_json())
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        
        returnedMaintenanceTicket = MaintenanceTicket(**monad.get_param_at(0))
   
        monad = await schedulerRepository.schedule_maintenance_ticket_upload(session, scope, houseKey, house.firebaseId, returnedMaintenanceTicket, image)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        
        return returnedMaintenanceTicket



async def add_house(landlordId: int, lease: LeaseInput, info: Info) -> House:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await houseRepository.create_house(session, scope, landlordId)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        

        house = House(**monad.get_param_at(0), lease=None)
        monad = await leaseRepository.create_lease(session, scope, house.id, lease.to_json())
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])

        house.lease = Lease(**monad.get_param_at(0))
        monad = await schedulerRepository.schedule_lease(session, scope, house.firebaseId, house.houseKey, monad.get_param_at(0), "")
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return house

    






async def get_houses(landlordId: int, info: Info) -> List[House]:
    async with aiohttp.ClientSession() as session:
        
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        
        monad = await houseRepository.get_houses(session, scope, landlordId)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])

        houses = []
        for house in monad.get_param_at(0):
            monad = await leaseRepository.get_lease_by_houseId(session, scope, house["id"])
            if monad.has_errors():
                if monad.error_status["status"] == 404:
                    continue
                else:
                    raise Exception(monad.error_status["reason"])
            houses.append(House(**house, lease=Lease(**monad.get_param_at(0))))
        return houses
        
        
async def get_house_by_house_key(houseKey: str, info: Info) -> House:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await houseRepository.get_house_by_house_key(session, scope, houseKey)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])

        house = NewHouse(**monad.get_param_at(0))
        monad = await leaseRepository.get_lease_by_houseId(session, scope, house.id)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])

        monad = await schedulerRepository.schedule_lease(session, scope, house.firebaseId, houseKey, monad.get_param_at(0), "")
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return House(**house, lease=Lease(**monad.get_param_at(0)))
   



async def schedule_lease(houseKey: str, signature: str, info: Info) -> Lease:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await houseRepository.get_house_by_house_key(session, scope, houseKey)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        house = NewHouse(**monad.get_param_at(0))
        
        monad = await leaseRepository.get_lease_by_houseId(session, scope, house.id)
        if monad.has_errors():
                raise Exception(monad.error_status["reason"])
        lease = monad.get_param_at(0)

        monad = await schedulerRepository.schedule_lease(session, scope, house.firebaseId, houseKey, lease, signature)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return Lease(**lease)
 

        
async def add_tenant(houseKey: str, tenant: AddTenantEmailInput, info: Info) -> Tenant:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await houseRepository.get_house_by_house_key(session, scope, houseKey)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])

        houseRepsonse = monad.get_param_at(0)
        monad = await leaseRepository.get_lease_by_houseId(session, scope, houseRepsonse["id"])
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        house = House(**houseRepsonse, lease=Lease(**monad.get_param_at(0)))

        monad = await tenantRepository.update_tenant_state(session, scope, "InvitePending", tenant.to_json())
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        updatedTenant = Tenant(**monad.get_param_at(0))
        
        monad = await schedulerRepository.schedule_add_tenant_email(session, scope, houseKey, house.firebaseId, house.lease.documentURL, tenant.to_json())
        if monad.has_errors():
            raise Exception(monad.errors["reason"])
      
        return updatedTenant

async def create_temp_tenant_account(houseId: int, tenant: TempTenantInput, info: Info) -> Tenant:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await tenantRepository.create_tenant(session, scope, houseId, tenant.to_json())
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return Tenant(**monad.get_param_at(0))


async def create_tenant_account(houseKey: str, tenant: TenantInput, signature: str, documentURL: str, info: Info) -> Tenant:
    async with aiohttp.ClientSession() as session:
        
        monad = await houseRepository.get_house_by_house_key(session, scope, houseKey)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        
        house = NewHouse(**monad.get_param_at(0))
        monad = await tenantRepository.update_tenant_state(session, scope, "Approved", tenant.to_json())
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])

        tenant = Tenant(**monad.get_param_at(0))
      
        monad = await schedulerRepository.schedule_sign_lease(session, scope, tenant, houseKey, house.firebaseId, documentURL, signature)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])

        return tenant


async def tenant_login(login: LoginTenantInput, info: Info) -> Tenant:
    async with aiohttp.ClientSession() as session:
        
        monad = await houseRepository.get_house_by_house_key(session, scope, login.houseKey)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        house = NewHouse(**monad.get_param_at(0))

        monad = await tenantRepository.login(session, scope, house.id, login.to_json())
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        print(monad.get_param_at(0))
        return Tenant(**monad.get_param_at(0))


async def get_tenants_by_house_id(houseId: int, info: Info) -> List[Tenant]:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await tenantRepository.get_tenants_by_house_id(session, scope, houseId)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return [Tenant(**json) for json in monad.get_param_at(0)]

async def create_landlord_account(landlord: LandlordInput) -> Landlord:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await landlordRepository.create_landlord(session, scope, landlord.to_json())
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return Landlord(**monad.get_param_at(0))
    
async def landlord_login(login: LoginLandlordInput, info: Info) -> Landlord:
    async with aiohttp.ClientSession() as session:
   
        monad = await landlordRepository.login(session, login.to_json())
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        landlord = Landlord(**monad.get_param_at(0))

        monad = await houseRepository.get_houses(session, [f"/Landlord/{landlord.id}/House"], landlord.id)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        houses = [NewHouse(**json) for json in monad.get_param_at(0)]

        scopes = auth.get_landlord_scope(landlord.id, houses)
        print(scopes)
        token = auth.generate_landlord_token(scopes)

        info.context["response"].headers["Access-Control-Expose-Headers"] = "Authorization"
        info.context["response"].headers["Authorization"] = token
        tokenPayload = auth.get_token_payload(token)
        return landlord



async def get_device_ids(houseKey: str) -> DeviceId:
    async with aiohttp.ClientSession() as session:
        monad = await houseRepository.get_house_by_house_key(session, scope, houseKey)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        house = NewHouse(**monad.get_param_at(0))
    
        monad = await tenantRepository.get_tenants_by_house_id(session, scope, house.id)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        tenants = map(lambda tenant: Tenant(**tenant), monad.get_param_at(0))
        tenantDeviceIds = map(lambda tenant: tenant.deviceId, tenants)
        tenantDeviceIds = filter(lambda tenant: tenant != None, tenantDeviceIds)
        
        monad = await landlordRepository.get_landlord_by_id(session, scope, house.landlordId)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        landlord = Landlord(**monad.get_param_at(0))
        
        return DeviceId(landlordDeviceId=landlord.deviceId, tenantDeviceIds=list(tenantDeviceIds))




async def get_lease(houseId: int, info: Info) -> Lease:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await leaseRepository.get_lease_by_houseId(session, scope, houseId)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return monad.get_param_at(0).to_json()

    


async def update_landlord_info(houseId: int, landlordInfo: LandlordInfoInput, info: Info) -> LandlordInfo:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await leaseRepository.update_landlord_info(session, scope, houseId, landlordInfo.to_json())
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return LandlordInfo(**monad.get_param_at(0))


async def update_landlord_address(houseId: int, landlordAddress: LandlordAddressInput, info: Info) -> LandlordAddress:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await leaseRepository.update_landlord_address(session, scope, houseId, landlordAddress.to_json())
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return LandlordAddress(**monad.get_param_at(0))

async def update_rental_address(houseId: int, rentalAddress: RentalAddressInput, info: Info) -> RentalAddress:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await leaseRepository.update_rental_address(session, scope, houseId, rentalAddress.to_json())
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return RentalAddress(**monad.get_param_at(0))

async def update_rent(houseId: int, rent: RentInput, info: Info) -> Rent:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await leaseRepository.update_rent(session, scope, houseId, rent.to_json())
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return Rent(**monad.get_param_at(0))

async def update_tenancy_terms(houseId: int, tenancyTerms: TenancyTermsInput, info: Info) -> TenancyTerms:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await leaseRepository.update_tenancy_terms(session, scope, houseId, tenancyTerms.to_json())
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return TenancyTerms(**monad.get_param_at(0))

async def update_services(houseId: int, services: List[ServiceInput], info: Info) -> List[Service]:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await leaseRepository.update_services(session, scope, houseId, services)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return [Service(**service) for service in monad.get_param_at(0)]

async def update_utilities(houseId: int, utilities: List[UtilityInput], info: Info) -> List[Utility]:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await leaseRepository.update_utilities(session, scope, houseId, utilities)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return [Utility(**utility) for utility in monad.get_param_at(0)]

async def update_rent_discounts(houseId: int, rentDiscounts: List[RentDiscountInput], info: Info) -> List[RentDiscount]:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await leaseRepository.udpate_rent_discounts(session, scope, houseId, rentDiscounts)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return [RentDiscount(**rentDiscount) for rentDiscount in monad.get_param_at(0)]

async def update_rent_deposits(houseId: int, rentDeposits: List[RentDepositInput], info: Info) -> List[RentDeposit]:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await leaseRepository.update_rent_deposits(session, scope, houseId, rentDeposits)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return [RentDeposit(**rentDeposit) for rentDeposit in monad.get_param_at(0)]

async def update_additional_terms(houseId: int, additionalTerms: List[AdditionalTermInput], info: Info) -> List[AdditionalTerm]:
    async with aiohttp.ClientSession() as session:
        tokenPayload = get_auth_token_payload(info)
        scope = tokenPayload["scope"]
        monad = await leaseRepository.update_additional_terms(session, scope, houseId, additionalTerms)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return [AdditionalTerm(**additionalTerm) for additionalTerm in monad.get_param_at(0)]













    