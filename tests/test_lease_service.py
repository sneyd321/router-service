from models.repository import LeaseRepository
from models.request import Request
from models.cloud_run import CloudRun
from models.graphql_inputs import LeaseInput, LandlordInfoInput, LandlordAddressInput, RentalAddressInput, RentInput, TenancyTermsInput, ServiceInput, UtilityInput, RentDiscountInput, RentDepositInput, AdditionalTermInput, DetailInput
from models.graphql_types import Lease
from models.request import Request
import json
import aiohttp

cloudRun = CloudRun()
cloudRun.discover_dev()
leaseRepository = LeaseRepository(cloudRun.get_lease_hostname())
#cloudRun.discover()
#leaseRepository = LeaseRepository(cloudRun.get_lease_test_hostname())


async def test_Router_insert_lease_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)
        monad = await leaseRepository.create_lease(session, 1, leaseData)
        print(monad.error_status)
        assert monad.get_param_at(0) is not None

async def test_Router_get_lease_by_house_id():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)
        monad = await leaseRepository.create_lease(session, 1, leaseData)
      
        monad = await leaseRepository.get_lease_by_houseId(session, 1)
        assert monad.get_param_at(0) is not None


async def test_Router_updates_landlord_info_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)
          

        monad = await leaseRepository.create_lease(session, 1, leaseData)

        monad = await leaseRepository.update_landlord_info(session, 1, leaseData["landlordInfo"])
        assert monad.get_param_at(0) == leaseData["landlordInfo"]


async def test_Router_updates_landlord_address_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)
           
        monad = await leaseRepository.create_lease(session, 1, leaseData)
        monad = await leaseRepository.update_landlord_address(session, 1, leaseData["landlordAddress"])
        assert monad.get_param_at(0) == leaseData["landlordAddress"]


async def test_Router_updates_rental_address_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)

        monad = await leaseRepository.create_lease(session, 1, leaseData)
        monad = await leaseRepository.update_rental_address(session, 1, leaseData["rentalAddress"])
        assert monad.get_param_at(0) == leaseData["rentalAddress"]


async def test_Router_updates_rent_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)
            
        monad = await leaseRepository.create_lease(session, 1, leaseData)
        monad = await leaseRepository.update_rent(session, 1, leaseData["rent"])
        assert monad.get_param_at(0) == leaseData["rent"]


async def test_Router_updates_tenancy_terms_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)

        monad = await leaseRepository.create_lease(session, 1, leaseData)
        monad = await leaseRepository.update_tenancy_terms(session, 1, leaseData["tenancyTerms"])
        assert monad.get_param_at(0) == leaseData["tenancyTerms"]

async def test_Router_updates_services_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)

        monad = await leaseRepository.create_lease(session, 1, leaseData)
        inputs = []
        for data in leaseData["services"]:
            listItemInput = ServiceInput(**data)
            details = []
            for detail in data["details"]:
                detailInput = DetailInput(**detail)
                details.append(detailInput)
            listItemInput.details = details
            inputs.append(listItemInput)
        monad = await leaseRepository.update_services(session, 1, inputs)
        assert monad.get_param_at(0) == leaseData["services"]


async def test_Router_updates_utilities_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)

        monad = await leaseRepository.create_lease(session, 1, leaseData)
        inputs = []
        for data in leaseData["utilities"]:
            listItemInput = UtilityInput(**data)
            details = []
            for detail in data["details"]:
                detailInput = DetailInput(**detail)
                details.append(detailInput)
            listItemInput.details = details
            inputs.append(listItemInput)
        monad = await leaseRepository.update_utilities(session, 1, inputs)
        assert monad.get_param_at(0) == leaseData["utilities"]


async def test_Router_updates_rent_deposits_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)

        monad = await leaseRepository.create_lease(session, 1, leaseData)
        inputs = []
        for data in leaseData["rentDeposits"]:
            listItemInput = RentDepositInput(**data)
            details = []
            for detail in data["details"]:
                detailInput = DetailInput(**detail)
                details.append(detailInput)
            listItemInput.details = details
            inputs.append(listItemInput)

        monad = await leaseRepository.update_rent_deposits(session, 1, inputs)
        assert monad.get_param_at(0) == leaseData["rentDeposits"]


async def test_Router_updates_rent_discounts_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)
        inputs = []
        for data in leaseData["rentDiscounts"]:
            listItemInput = RentDiscountInput(**data)
            details = []
            for detail in data["details"]:
                detailInput = DetailInput(**detail)
                details.append(detailInput)
            listItemInput.details = details
            inputs.append(listItemInput)

        monad = await leaseRepository.create_lease(session, 1, leaseData)
        monad = await leaseRepository.udpate_rent_discounts(session, 1, inputs)
        assert monad.get_param_at(0) == leaseData["rentDiscounts"]


async def test_Router_updates_additional_terms_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)
        
        monad = await leaseRepository.create_lease(session, 1, leaseData)
        inputs = []
        for data in leaseData["additionalTerms"]:
            listItemInput = AdditionalTermInput(**data)
            details = []
            for detail in data["details"]:
                detailInput = DetailInput(**detail)
                details.append(detailInput)
            listItemInput.details = details
            inputs.append(listItemInput)

        monad = await leaseRepository.update_additional_terms(session, 1, inputs)
        assert monad.get_param_at(0) == leaseData["additionalTerms"]
