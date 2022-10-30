import strawberry
from typing import Optional, Union, List, AsyncGenerator
from strawberry.file_uploads import Upload

from models.cloud_run import CloudRun
from models.monad import RequestMaybeMonad
from models.repository import Repository
from models.request import Request
from models.graphql_inputs import *
from models.graphql_types import *

import json, itertools, asyncio, base64

cloudRun = CloudRun()
cloudRun.discover_dev()

async def get_maintenance_tickets(houseId: int) -> List[MaintenanceTicket]:
    request = Request(cloudRun.get_maintenance_ticket_hostname(), f"/House/{houseId}/MaintenanceTicket")
    maintenanceTicketRepository = Repository(request)
    monad = await maintenanceTicketRepository.get()
    if monad.has_errors():
        raise Exception(monad.error_status["reason"])
    return MaintenanceTicket(**monad.get_param_at(0))

async def get_maintenance_tickets_by_house_key(houseKey: str) -> List[MaintenanceTicket]:
    request = Request(cloudRun.get_house_hostname(), f"/House/{houseKey}")
    houseRepository = Repository(request)
    monad = await houseRepository.get()
    if monad.has_errors():
        raise Exception(monad.errors["reason"])
    house = NewHouse(**monad.get_param_at(0))
    
    request = Request(cloudRun.get_maintenance_ticket_hostname(), f"/House/{house.id}/MaintenanceTicket")
    maintenanceTicketRepository = Repository(request)
    monad = await maintenanceTicketRepository.get()
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



async def add_house(landlordId: int) -> NewHouse:
    request = Request(cloudRun.get_house_hostname(), f"/House")
    repository = Repository(request)
    monad = await repository.insert(landlordId=landlordId)
    if monad.has_errors():
        raise Exception(monad.error_status["reason"])
    return NewHouse(**monad.get_param_at(0))

    


async def get_houses(landlordId: int) -> List[NewHouse]:
    request = Request(hostname, f"/Landlord/{landlordId}/House")
    repository = Repository(request)
    monad = await houseRepository.get()
    if monad.errors:
        raise Exception(monad.errors["reason"])
    return NewHouse(**monad.data)

async def get_house_by_house_key(houseKey: str) -> NewHouse:
    request = Request(hostname, f"/House/{houseKey}")
    repository = Repository(request)
    monad = await repository.get()
    if monad.errors:
        raise Exception(monad.errors["reason"])
    return NewHouse(**monad.get_param_at(0))




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































async def get_lease(houseId: strawberry.ID) -> Lease:
    monad = await leaseRepository.get_lease_by_houseIds([houseId])
    if monad.errors:
        raise Exception(monad.errors["reason"])
    leaseResponse = monad.data[0]
    return Lease(**leaseResponse)

    
async def update_landlord_info(id: strawberry.ID, inputData: LandlordInfoInput) -> LandlordInfo:
    monad = await leaseRepository.update(id, inputData.to_json(), "LandlordInfo")
    if monad.errors:
        raise Exception(monad.errors["Error"])
    print(inputData.to_json())
    return LandlordInfo(**inputData.to_json())

async def update_landlord_address(id: strawberry.ID, inputData: LandlordAddressInput) -> LandlordAddress:
    monad = await leaseRepository.update(id, inputData.to_json(), "LandlordAddress")
    if monad.errors:
        raise Exception(monad.errors["Error"])
    return LandlordAddress(**inputData.to_json())

async def update_rental_address(id: strawberry.ID, inputData: RentalAddressInput) -> RentalAddress:
    monad = await leaseRepository.update(id, inputData.to_json(), "RentalAddress")
    if monad.errors:
        raise Exception(monad.errors["Error"])
    return RentalAddress(**inputData.to_json())

async def update_rent(id: strawberry.ID, inputData: RentInput) -> Rent:
    monad = await leaseRepository.update(id, inputData.to_json(), "Rent")
    if monad.errors:
        raise Exception(monad.errors["Error"])
    return Rent(**inputData.to_json())

async def update_tenancy_terms(id: strawberry.ID, inputData: TenancyTermsInput) -> TenancyTerms:
    monad = await leaseRepository.update(id, inputData.to_json(), "TenancyTerms")
    if monad.errors:
        raise Exception(monad.errors["Error"])
    return TenancyTerms(**inputData.to_json())

async def update_services(id: strawberry.ID, inputData: List[ServiceInput]) -> List[Service]:
    services = [service.to_json() for service in inputData]
    monad = await leaseRepository.update(id, services, "Services")
    if monad.errors:

        raise Exception(monad.errors["Error"])
    return [Service(**service) for service in services]

async def update_utilities(id: strawberry.ID, inputData: List[UtilityInput]) -> List[Utility]:
    utilities = [utililty.to_json() for utililty in inputData]
    monad = await leaseRepository.update(id, utilities, "Utilities")
    if monad.errors:
        raise Exception(monad.errors["Error"])
    return [Utility(**utility) for utility in utilities]

async def udpate_rent_discounts(id: strawberry.ID, inputData: List[RentDiscountInput]) -> List[RentDiscount]:
    rentDiscounts = [rentDiscount.to_json() for rentDiscount in inputData]
    monad = await leaseRepository.update(id, rentDiscounts, "RentDiscounts")
    if monad.errors:
        raise Exception(monad.errors["Error"])
    return [RentDiscount(**rentDiscount) for rentDiscount in rentDiscounts]

async def udpate_rent_deposits(id: strawberry.ID, inputData: List[RentDepositInput]) -> List[RentDeposit]:
    rentDeposits = [rentDeposit.to_json() for rentDeposit in inputData]
    monad = await leaseRepository.update(id, rentDeposits, "RentDeposits")
    if monad.errors:
        raise Exception(monad.errors["Error"])
    return [RentDeposit(**rentDeposit) for rentDeposit in rentDeposits]

async def udpate_additional_terms(id: strawberry.ID, inputData: List[AdditionalTermInput]) -> List[AdditionalTerm]:
    additionalTerms = [additionalTerm.to_json() for additionalTerm in inputData]
    monad = await leaseRepository.update(id, additionalTerms, "AdditionalTerms")
    if monad.errors:
        raise Exception(monad.errors["Error"])
    return [AdditionalTerm(**additionalTerm) for additionalTerm in additionalTerms]













    