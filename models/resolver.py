import strawberry
from typing import Optional, Union, List, AsyncGenerator
from strawberry.file_uploads import Upload

from models.cloud_run import CloudRun
from models.monad import RequestMaybeMonad
from models.repository import MaintenanceTicketRepository, HouseRepository, LeaseRepository, SchedulerRepository
from models.request import Request
from models.graphql_inputs import *
from models.graphql_types import *

import json, itertools, asyncio, base64, aiohttp

cloudRun = CloudRun()
cloudRun.discover_dev()

maintenanceTicketRepository = MaintenanceTicketRepository(cloudRun.get_maintenance_ticket_hostname())
houseRepository = HouseRepository(cloudRun.get_house_hostname())
leaseRepository = LeaseRepository(cloudRun.get_lease_hostname())
schedulerRepository = SchedulerRepository(cloudRun.get_scheduler_hostname())

async def get_maintenance_tickets(houseId: int) -> List[MaintenanceTicket]:
    async with aiohttp.ClientSession() as session:
        monad = await maintenanceTicketRepository.get_maintenance_tickets(session, houseId)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return [MaintenanceTicket(**data) for data in monad.get_param_at(0)]

async def get_maintenance_ticket_by_id(houseKey: str, maintenanceTicketId: int) -> MaintenanceTicket:
    async with aiohttp.ClientSession() as session:
        monad = await houseRepository.get_house_by_house_key(session, houseKey)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        house = NewHouse(**monad.get_param_at(0))
        
        monad = await maintenanceTicketRepository.get_maintenance_ticket_by_id(session, house.id, maintenanceTicketId)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return MaintenanceTicket(**monad.get_param_at(0))

async def add_maintenance_ticket(houseKey: str, maintenanceTicket: MaintenanceTicketInput, image: str) -> MaintenanceTicket:
    request = Request(cloudRun.get_house_hostname(), f"/House/{houseKey}")
    houseRepository = Repository(request)
    monad = await houseRepository.get()
    if monad.has_errors():
        raise Exception(monad.errors["reason"])
    house = NewHouse(**monad.get_param_at(0))

    request = Request(cloudRun.get_maintenance_ticket_hostname(), f"/MaintenanceTicket")
    maintenanceTicketRepository = Repository(request)
    maintenanceTicket.houseId = house.id
    monad = await maintenanceTicketRepository.insert(**maintenanceTicket.to_json())
    if monad.has_errors():
        raise Exception(monad.error_status["reason"])
    maintenanceTicket = MaintenanceTicket(**monad.get_param_at(0))

    request = Request(cloudRun.get_scheduler_hostname(), "/MaintenanceTicket")
    repository = Repository(request)
    monad = await schedulerRepository.insert(**{
        "firebaseId": maintenanceTicket.firebaseId,
        "imageURL": maintenanceTicket.imageURL,
        "houseKey": houseKey,
        "maintenanceTicketId": maintenanceTicket.id,
        "description": maintenanceTicket.description.descriptionText,
        "firstName": maintenanceTicket.sender.firstName,
        "lastName": maintenanceTicket.sender.lastName,
        "image": image
    })
    if monad.errors:
        raise Exception(monad.errors["reason"])
    return maintenanceTicket



async def add_house(landlordId: int, lease: LeaseInput) -> House:
    async with aiohttp.ClientSession() as session:
        monad = await houseRepository.create_house(session, landlordId)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])

        house = House(**monad.get_param_at(0), lease=None)
        monad = await leaseRepository.create_lease(session, house.id, lease)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        print(monad.get_param_at(0))
        house.lease = Lease(**monad.get_param_at(0))
        """
        monad = await schedulerRepository.schedule_lease(session, house.firebaseId, lease.to_json())
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        """
        return house

    


async def get_houses(landlordId: int) -> List[House]:
    async with aiohttp.ClientSession() as session:
        monad = await houseRepository.get_houses(session, landlordId)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])

        houses = []
        for house in monad.get_param_at(0):
            monad = await leaseRepository.get_lease_by_houseId(session, house["id"])
            if monad.has_errors():
                raise Exception(monad.error_status["reason"])
            houses.append(House(**house, lease=Lease(**monad.get_param_at(0))))
        return houses
        
        
async def get_house_by_house_key(houseKey: str) -> House:
    async with aiohttp.ClientSession() as session:
        monad = await houseRepository.get_house_by_house_key(session, houseKey)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])

        house = monad.get_param_at(0)
        monad = await leaseRepository.get_lease_by_houseId(session, house["id"])
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return House(**house, lease=Lease(**monad.get_param_at(0)))
   



async def schedule_lease(houseId: int, firebaseId: str) -> LeaseSchedule:
    monad = await leaseRepository.get_lease_by_houseIds([str(houseId)])
    if monad.errors:
        raise Exception(monad.errors["Error"])
    if not monad.data:
        raise Exception(f"Lease not found with houseId: {houseId}")

    leaseResponse = monad.data[0]
    print(leaseResponse)
    data = {
        "firebaseId": firebaseId,
        "lease": leaseResponse
    }
    monad = await schedulerRepository.schedule_lease(data)
    if monad.errors:
        raise Exception(monad.errors["Error"])
    test = LeaseSchedule(**data)
    print(test.lease["id"])
    return LeaseSchedule(**data)
 
        
async def add_tenant(houseKey: str, tenant: TenantInput) -> Tenant:
    request = Request(cloudRun.get_house_hostname(), f"/House/{houseKey}")
    houseRepository = Repository(request)
    monad = await houseRepository.get()
    if monad.has_errors():
        raise Exception(monad.errors["reason"])
    house = NewHouse(**monad.get_param_at(0))

    #TODO: Get Lease

    request = Request(cloudRun.get_scheduler_hostname(), f"/AddTenantEmail")
    schedulerRepository = Repository(request)
    monad = await schedulerRepository.insert(**{
        "firstName": tenant.firstName,
        "lastName": tenant.lastName,
        "email": tenant.email,
        "houseKey": houseKey,
        "documentURL": "str",
        "firebaseId": house.firebaseId,
    })
    if monad.errors:
        raise Exception(monad.errors["Error"])
    return Tenant(**tenant.to_json(), houseId=0, tenantPosition=0)


async def create_tenant_account(houseKey: str, tenant: TenantInput, signature: str, registrationToken: str, documentURL: str) -> Tenant:
    request = Request(cloudRun.get_house_hostname(), f"/House/{houseKey}")
    houseRepository = Repository(request)
    monad = await houseRepository.get()
    if monad.has_errors():
        raise Exception(monad.errors["reason"])
    house = NewHouse(**monad.get_param_at(0))

    request = Request(cloudRun.get_tenant_hostname(), f"/Tenant")
    tenantRepository = Repository(request)
    tenantRepository.insert(houseId=house.id, **tenant.to_json())
    if monad.has_errors():
        raise Exception(monad.errors["reason"])
    tenant = Tenant(**monad.get_param_at(0))
   
    request = Request(cloudRun.get_scheduler_hostname(), "/SignLease")
    repository = Repository(request)
    monad = await repository.insert(**{
        "firstName": tenant.firstName,
        "lastName": tenant.lastName,
        "email": tenant.email,
        "documentURL": documentURL,
        "tenantPosition": tenant.tenantPosition,
        "tenantState": tenant.tenantState,
        "signiture": signature,
        "firebaseId": house.firebaseId,
    })
    if monad.errors:
        raise Exception(monad.errors["reason"])
    return tenant


async def tenant_login(login: LoginTenantInput) -> Tenant:
    request = Request(cloudRun.get_house_hostname(), f"/House/{login.houseKey}")
    houseRepository = Repository(request)
    monad = await houseRepository.get()
    if monad.has_errors():
        raise Exception(monad.errors["reason"])
    house = NewHouse(**monad.get_param_at(0))

    request = Request(cloudRun.get_tenant_hostname(), f"/Login")
    tenantRepository = Repository(request)
    tenantRepository.insert(houseId=house.id, **login.to_json())
    if monad.has_errors():
        raise Exception(monad.errors["reason"])
    return Tenant(**monad.get_param_at(0))


async def create_landlord_account(landlord: LandlordInput) -> Landlord:
    request = Request(cloudRun.get_landlord_hostname(), "/Landlord")
    landlordRepository = Repository(request)
    monad = await landlordRepository.insert(**landlord.to_json())
    if monad.has_errors():
        raise Exception(monad.errors["reason"])
    return Landlord(**monad.get_param_at(0))
    
async def landlord_login(login: LoginLandlordInput) -> Landlord:
    request = Request(cloudRun.get_landlord_hostname(), "/Login")
    landlordRepository = Repository(request)
    monad = await landlordRepository.insert(**login.to_json())
    if monad.has_errors():
        raise Exception(monad.errors["reason"])
    return Landlord(**monad.get_param_at(0))



async def get_device_ids(houseKey: str) -> DeviceId:
    monad = await houseRepository.get_house_by_house_key(houseKey)
    if monad.errors:
        raise Exception(monad.errors["reason"])
    house = NewHouse(**monad.data)
    print(house)
    monad = await tenantRepository.get_tenants_by_house_id(house.id)
    if monad.errors:
        raise Exception(monad.errors["reason"])
    tenants = map(lambda tenant: Tenant(**tenant), monad.data)
    tenantDeviceIds = map(lambda tenant: tenant.deviceId, tenants)
    tenantDeviceIds = filter(lambda tenant: tenant != None, tenantDeviceIds)
    
    monad = await landlordRepository.get_landlord_by_landlord_id(1)#house.landlordId)
    if monad.errors:
        raise Exception(monad.errors["reason"])
    landlord = Landlord(**monad.data)
    
    deviceIds = list(tenantDeviceIds)
    deviceIds.append(landlord.deviceId)

    return DeviceId(deviceIds)




async def get_lease(houseId: int) -> Lease:
    async with aiohttp.ClientSession() as session:
        monad = await leaseRepository.get_lease_by_houseId(session, houseId)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return monad.get_param_at(0).to_json()

    


async def update_landlord_info(leaseId: int, landlordInfo: LandlordInfoInput) -> LandlordInfo:
    async with aiohttp.ClientSession() as session:
        monad = await leaseRepository.update_landlord_info(session, leaseId, landlordInfo.to_json())
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return LandlordInfo(**monad.get_param_at(0))


async def update_landlord_address(leaseId: int, landlordAddress: LandlordAddressInput) -> LandlordAddress:
    async with aiohttp.ClientSession() as session:
        monad = await leaseRepository.update_landlord_address(session, leaseId, landlordAddress.to_json())
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return LandlordAddress(**monad.get_param_at(0))

async def update_rental_address(leaseId: int, rentalAddress: RentalAddressInput) -> RentalAddress:
    async with aiohttp.ClientSession() as session:
        monad = await leaseRepository.update_rental_address(session, leaseId, rentalAddress.to_json())
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return RentalAddress(**monad.get_param_at(0))

async def update_rent(leaseId: int, rent: RentInput) -> Rent:
    async with aiohttp.ClientSession() as session:
        monad = await leaseRepository.update_rent(session, leaseId, rent.to_json())
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return Rent(**monad.get_param_at(0))

async def update_tenancy_terms(leaseId: int, tenancyTerms: TenancyTermsInput) -> TenancyTerms:
    async with aiohttp.ClientSession() as session:
        monad = await leaseRepository.update_tenancy_terms(session, leaseId, tenancyTerms.to_json())
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return TenancyTerms(**monad.get_param_at(0))

async def update_services(leaseId: int, services: List[ServiceInput]) -> List[Service]:
    async with aiohttp.ClientSession() as session:
        monad = await leaseRepository.update_services(session, leaseId, services)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return [Service(**service) for service in monad.get_param_at(0)]

async def update_utilities(leaseId: int, utilities: List[UtilityInput]) -> List[Utility]:
    async with aiohttp.ClientSession() as session:
        monad = await leaseRepository.update_utilities(session, leaseId, utilities)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return [Utility(**utility) for utility in monad.get_param_at(0)]

async def update_rent_discounts(leaseId: int, rentDiscounts: List[RentDiscountInput]) -> List[RentDiscount]:
    async with aiohttp.ClientSession() as session:
        monad = await leaseRepository.udpate_rent_discounts(session, leaseId, rentDiscounts)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return [RentDiscount(**rentDiscount) for rentDiscount in monad.get_param_at(0)]

async def update_rent_deposits(leaseId: int, rentDeposits: List[RentDepositInput]) -> List[RentDeposit]:
    async with aiohttp.ClientSession() as session:
        monad = await leaseRepository.update_rent_deposits(session, leaseId, rentDeposits)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return [RentDeposit(**rentDeposit) for rentDeposit in monad.get_param_at(0)]

async def update_additional_terms(leaseId: int, additionalTerms: List[AdditionalTermInput]) -> List[AdditionalTerm]:
    async with aiohttp.ClientSession() as session:
        monad = await leaseRepository.update_additional_terms(session, leaseId, additionalTerms)
        if monad.has_errors():
            raise Exception(monad.error_status["reason"])
        return [AdditionalTerm(**additionalTerm) for additionalTerm in monad.get_param_at(0)]













    