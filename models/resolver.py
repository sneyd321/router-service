import strawberry
from typing import Optional, Union, List, AsyncGenerator
from models.graphql_inputs import *
from models.graphql_types import *
from models.request import Request
from models.monad import MaybeMonad
import json, itertools, asyncio
from strawberry.types import Info
from strawberry.file_uploads import Upload
import base64

from models.repository import HouseRepsository, LeaseRepository, SchedulerRepository, MaintenanceTicketRepository, TenantRepository, LandlordRepository

houseRepository = HouseRepsository()
leaseRepository = LeaseRepository()
schedulerRepository = SchedulerRepository()
maintenanceTicketRepository = MaintenanceTicketRepository()
tenantRepository = TenantRepository()
landlordRepository = LandlordRepository()

async def maintenance_tickets() -> List[MaintenanceTicket]:
    request = Request("http://localhost:8080")
    monad = await MaybeMonad(*("/House/1/MaintenanceTicket")).bind(request.post)
    if monad.errors:
        raise Exception(monad.errors["Error"])
    jsonArray = monad.result
    return [MaintenanceTicket(**json) for json in jsonArray]


async def get_maintenance_ticket_by_id(houseKey: str, maintenanceTicketId: int) -> MaintenanceTicket:
    monad = await houseRepository.get_house_by_house_key(houseKey)
    if monad.errors:
        raise Exception(monad.errors["Error"])
    houseResponse = monad.data
    houseId = str(houseResponse["id"])

    monad = await maintenanceTicketRepository.get_maintenance_ticket_by_id(maintenanceTicketId)
    if monad.errors:
        raise Exception(monad.errors["Error"])
    print(monad.data)
    return MaintenanceTicket(**monad.data)


async def add_maintenance_ticket(houseKey: str, maintenanceTicket: MaintenanceTicketInput, picture: Upload) -> MaintenanceTicket:
    monad = await houseRepository.get_house_by_house_key(houseKey)
    if monad.errors:
        raise Exception(monad.errors["reason"])
    print(monad.data)
    houseId = monad.data["id"]
    firebaseId = monad.data["firebaseId"]
    monad = await maintenanceTicketRepository.create_maintenance_ticket(houseId, maintenanceTicket.to_json())
    if monad.errors:
        raise Exception(monad.errors["reason"])
    print(monad.result)
    maintenanceTicket = MaintenanceTicket(**monad.result)
 
    monad = await schedulerRepository.schedule_maintenance_ticket_upload(houseKey, firebaseId, maintenanceTicket, picture)
    if monad.errors:
        raise Exception(monad.errors["reason"])

    print(monad.result)

    return maintenanceTicket



async def add_house(homeownerId: int, leaseInput: LeaseInput) -> House:
    monad = await houseRepository.insert_house(homeownerId)
    if monad.errors:
        raise Exception(monad.errors["reason"])
    house = House(**monad.result, lease=houseInput.lease)

    monad = await leaseRepository.insert_lease(house.id, leaseInput.to_json())
    if monad.errors:
        raise Exception(monad.errors["reason"])
    return house
    

async def get_lease(houseId: strawberry.ID) -> Lease:
    monad = await leaseRepository.get_lease_by_houseIds([houseId])
    if monad.errors:
        raise Exception(monad.errors["Error"])
    leaseResponse = monad.data[0]
    return Lease(**leaseResponse)


async def get_houses(id: int) -> AsyncGenerator[List[House], None]:
    monad = await houseRepository.get_house(id)
    if monad.errors:
        raise Exception(monad.errors["Error"])
    houseResponse = monad.data
    houseIds = [str(house["id"]) for house in houseResponse]
    if not houseIds:
        return []
    monad = await leaseRepository.get_lease_by_houseIds(houseIds)
    if monad.errors:
        raise Exception(monad.errors["Error"])
    leaseResponse = monad.data
    houses = []
    for lease in leaseResponse:
        index = houseIds.index(str(lease["houseId"]))
        houses.append(House(**houseResponse[index], lease=Lease(**lease)))
  
    return houses

    
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


async def udpate_tenant_names(id: strawberry.ID, inputData: List[TenantNameInput]) -> List[TenantName]:
    tenantNames = [tenantName.to_json() for tenantName in inputData]
    monad = await leaseRepository.update(id, tenantNames, "TenantNames")
    if monad.errors:
        raise Exception(monad.errors["Error"])
    return [TenantName(**tenantName) for tenantName in tenantNames]





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
    
async def get_house_by_house_key(houseKey: strawberry.ID) -> House:
    print(houseKey)
    monad = await houseRepository.get_house_by_house_key(houseKey)
    if monad.errors:
        raise Exception(monad.errors["Error"])
    houseResponse = monad.data
    houseId = str(houseResponse["id"])

    monad = await leaseRepository.get_lease_by_houseIds([houseId])
    if monad.errors:
        raise Exception(monad.errors["Error"])
    leaseResponse = monad.data
    if leaseResponse:
        return House(**houseResponse, lease=Lease(**leaseResponse[0]))
    return None
        
async def add_tenant(houseKey: strawberry.ID, tenant: TenantInput) -> Tenant:
    monad = await houseRepository.get_house_by_house_key(houseKey)
    if monad.errors:
        raise Exception(monad.errors["Error"])
    houseResponse = monad.data
    houseId = str(houseResponse["id"])

    monad = await leaseRepository.get_lease_by_houseIds([houseId])
    if monad.errors:
        raise Exception(monad.errors["Error"])
    leaseResponse = monad.data
    if not leaseResponse:
        return None
    house = House(**houseResponse, lease=Lease(**leaseResponse[0]))
    
    monad = await schedulerRepository.schedule_add_tenant_email(tenant.firstName, tenant.lastName, tenant.email, house, "")
    if monad.errors:
        raise Exception(monad.errors["Error"])
    return Tenant(**tenant.to_json(), houseId=0, tenantPosition=0)


async def create_tenant_account(houseKey: strawberry.ID, tenant: CreateTenantAccountInput, signature: Upload, registrationToken: str, documentURL: str) -> Tenant:
    monad = await houseRepository.get_house_by_house_key(houseKey)
    if monad.errors:
        raise Exception(monad.errors["Error"])
    houseResponse = monad.data

    houseId = str(houseResponse["id"])
    firebaseId = houseResponse["firebaseId"]

    monad = await tenantRepository.create_tenant(tenant.to_json(), houseId)
    if monad.errors:
        raise Exception(monad.errors["Error"])
   
    tenant = Tenant(**monad.result)
    monad = await schedulerRepository.schedule_sign_lease(tenant, firebaseId, documentURL, signature, registrationToken)
    if monad.errors:
        raise Exception(monad.errors["Error"])
    return tenant


async def tenant_login(login: LoginTenantInput) -> Tenant:
    monad = await houseRepository.get_house_by_house_key(login.houseKey)
    if monad.errors:
        raise Exception(monad.errors["Error"])

    houseResponse = monad.data

    houseId = str(houseResponse["id"])

    monad = await tenantRepository.login(houseId, login.email, login.password, login.deviceId)
    if monad.errors:
        raise Exception(monad.errors["Error"])
    return Tenant(**monad.result)

async def create_landlord_account(landlord: LandlordInput) -> Landlord:
    monad = await landlordRepository.create_landlord(landlord.to_json())
    if monad.errors:
        raise Exception(monad.errors["Error"])
    return Landlord(**monad.result)
    
async def landlord_login(login: LoginLandlordInput) -> Landlord:
   
    monad = await landlordRepository.login(login.email, login.password, login.deviceId)
    if monad.errors:
        raise Exception(monad.errors["Error"])
    return Landlord(**monad.result)



async def get_device_ids(houseKey: str) -> DeviceId:
    monad = await houseRepository.get_house_by_house_key(houseKey)
    if monad.errors:
        raise Exception(monad.errors["Error"])
    house = NewHouse(**monad.data)
    print(house)
    monad = await tenantRepository.get_tenants_by_house_id(house.id)
    if monad.errors:
        raise Exception(monad.errors["Error"])
    tenants = map(lambda tenant: Tenant(**tenant), monad.data)
    tenantDeviceIds = map(lambda tenant: tenant.deviceId, tenants)
    tenantDeviceIds = filter(lambda tenant: tenant != None, tenantDeviceIds)
    
    monad = await landlordRepository.get_landlord_by_landlord_id(1)#house.landlordId)
    if monad.errors:
        raise Exception(monad.errors["Error"])
    landlord = Landlord(**monad.data)
    
    deviceIds = list(tenantDeviceIds)
    deviceIds.append(landlord.deviceId)

    return DeviceId(deviceIds)







    