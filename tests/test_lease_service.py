from models.repository import LeaseRepository
from models.request import Request
from models.cloud_run import CloudRun
from models.graphql_inputs import LeaseInput, LandlordInfoInput, LandlordAddressInput, RentalAddressInput, RentInput, TenancyTermsInput, ServiceInput, UtilityInput, RentDiscountInput, RentDepositInput, AdditionalTermInput
from models.graphql_types import Lease
from models.request import Request
import json
import aiohttp

cloudRun = CloudRun()
#cloudRun.discover_dev()

cloudRun.discover()
leaseRepository = LeaseRepository(cloudRun.get_lease_test_hostname())


async def test_Router_insert_lease_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)
            lease = LeaseInput(**leaseData)
        monad = await leaseRepository.create_lease(session, 1, lease)
    assert not monad.has_errors()

async def test_Router_get_lease_by_house_id():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)
            lease = LeaseInput(**leaseData)
        monad = await leaseRepository.create_lease(session, 1, lease)
        if monad.has_errors():
            print(monad.error_status)
        monad = await leaseRepository.get_lease_by_houseIds(session, [1])
    assert len(monad.get_param_at(0)) > 0


async def test_Router_returns_error_with_invalid_query_parameter_on_lease_service():
    async with aiohttp.ClientSession() as session:
        request = Request(cloudRun.get_lease_hostname(), f"/Lease?houses=vcxzfdvcxz")
        request.set_session(session)
        monad = await leaseRepository.get(request)
    assert monad.error_status == {"status": 400, "reason": f"Invalid query parameter. Must be in format 1,2 not vcxzfdvcxz"}


async def test_Router_updates_landlord_info_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)
            lease = LeaseInput(**leaseData)
            landlordInfo = LandlordInfoInput(**leaseData["landlordInfo"])

        monad = await leaseRepository.create_lease(session, 1, lease)
        monad.get_param_at(0)["id"]

        monad = await leaseRepository.update_landlord_info(session, monad.get_param_at(0)["id"], landlordInfo)
    assert monad.get_param_at(0) == leaseData["landlordInfo"]


async def test_Router_updates_landlord_address_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)
            lease = LeaseInput(**leaseData)
            landlordAddress = LandlordAddressInput(**leaseData["landlordAddress"])

        monad = await leaseRepository.create_lease(session, 1, lease)
        monad = await leaseRepository.update_landlord_address(session, monad.get_param_at(0)["id"], landlordAddress)
        assert monad.get_param_at(0) == leaseData["landlordAddress"]


async def test_Router_updates_rental_address_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)
            lease = LeaseInput(**leaseData)
            rentalAddress = RentalAddressInput(**leaseData["rentalAddress"])

        monad = await leaseRepository.create_lease(session, 1, lease)
        print(rentalAddress.__dict__)
        monad = await leaseRepository.update_rental_address(session, monad.get_param_at(0)["id"], rentalAddress)
        assert monad.get_param_at(0) == leaseData["rentalAddress"]


async def test_Router_updates_rent_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)
            lease = LeaseInput(**leaseData)
            rent = RentInput(**leaseData["rent"])

        monad = await leaseRepository.create_lease(session, 1, lease)
        monad = await leaseRepository.update_rent(session, monad.get_param_at(0)["id"], rent)
        assert monad.get_param_at(0) == leaseData["rent"]


async def test_Router_updates_tenancy_terms_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)
            lease = LeaseInput(**leaseData)
            tenanyTerms = TenancyTermsInput(**leaseData["tenancyTerms"])

        monad = await leaseRepository.create_lease(session, 1, lease)
        monad = await leaseRepository.update_tenancy_terms(session, monad.get_param_at(0)["id"], tenanyTerms)
        assert monad.get_param_at(0) == leaseData["tenancyTerms"]

async def test_Router_updates_services_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)
            lease = LeaseInput(**leaseData)
            services = [ServiceInput(**service) for service in leaseData["services"]]

        monad = await leaseRepository.create_lease(session, 1, lease)
        monad = await leaseRepository.update_services(session, monad.get_param_at(0)["id"], services)
        assert monad.get_param_at(0) == leaseData["services"]


async def test_Router_updates_utilities_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)
            lease = LeaseInput(**leaseData)
            utilities = [UtilityInput(**utility) for utility in leaseData["utilities"]]

        monad = await leaseRepository.create_lease(session, 1, lease)
        monad = await leaseRepository.update_utilities(session, monad.get_param_at(0)["id"], utilities)
        assert monad.get_param_at(0) == leaseData["utilities"]


async def test_Router_updates_rent_deposits_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)
            lease = LeaseInput(**leaseData)
            rentDeposits = [RentDepositInput(**rentDeposit) for rentDeposit in leaseData["rentDeposits"]]

        monad = await leaseRepository.create_lease(session, 1, lease)
        monad = await leaseRepository.udpate_rent_deposits(session, monad.get_param_at(0)["id"], rentDeposits)
        assert monad.get_param_at(0) == leaseData["rentDeposits"]


async def test_Router_updates_rent_discounts_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)
            lease = LeaseInput(**leaseData)
            rentDiscounts = [RentDiscountInput(**rentDiscount) for rentDiscount in leaseData["rentDiscounts"]]

        monad = await leaseRepository.create_lease(session, 1, lease)
        monad = await leaseRepository.udpate_rent_discounts(session, monad.get_param_at(0)["id"], rentDiscounts)
        assert monad.get_param_at(0) == leaseData["rentDiscounts"]


async def test_Router_updates_additional_terms_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/lease_test.json") as lease_test:
            leaseData = json.load(lease_test)
            lease = LeaseInput(**leaseData)
            additionalTerms = [AdditionalTermInput(**additionalTerm) for additionalTerm in leaseData["additionalTerms"]]

        monad = await leaseRepository.create_lease(session, 1, lease)
        monad = await leaseRepository.udpate_additional_terms(session, monad.get_param_at(0)["id"], additionalTerms)
        assert monad.get_param_at(0) == leaseData["additionalTerms"]
