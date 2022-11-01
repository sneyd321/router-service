from models.repository import TenantRepository
from models.cloud_run import CloudRun
from models.graphql_inputs import TenantInput, LoginTenantInput
import uuid
import aiohttp

cloudRun = CloudRun()
cloudRun.discover_dev()
#cloudRun.discover()

repository = TenantRepository(cloudRun.get_tenant_hostname())

async def test_Router_insert_tenant_returns_successfully():
    async with aiohttp.ClientSession() as session:
        tenant = {
            "firstName": "Timmy11",
            "lastName": "Tenant",
            "email": f"{uuid.uuid4()}@s.com",
            "password": "aaaaaa",
            "tenantState": "Not Approved",
        }
        monad = await repository.create_tenant(session, 1, tenant)
        assert list(monad.get_param_at(0).keys()) == ['houseId', 'firstName', 'lastName', 'email', 'tenantState', 'tenantPosition', 'deviceId']


async def test_Router_insert_tenant_returns_conflict_error_on_duplicate_email():
    async with aiohttp.ClientSession() as session:
        tenant = {
            "firstName": "Timmy11",
            "lastName": "Tenant",
            "email": "aaaa@s.com",
            "password": "aaaaaa",
            "tenantState": "Not Approved",
        }
        monad = await repository.create_tenant(session, 1, tenant)
        monad = await repository.create_tenant(session, 1, tenant)
        monad.error_status == {"status": 409, "reason": "Failed to insert data into database" }


async def test_Router_tenant_login_returns_successfully():
    async with aiohttp.ClientSession() as session:
        tenant = {
            "firstName": "Timmy11",
            "lastName": "Tenant",
            "email": "aaaa@s.com",
            "password": "aaaaaa",
            "tenantState": "Not Approved",
        }
    
        monad = await repository.create_tenant(session, 1, tenant)
        tenantLogin ={
            "email": "aaaa@s.com",
            "password": "aaaaaa",
            "houseKey": "DASFDSF",
            "deviceId": "eigTlTqf3fuwYzBIC1jEv_:APA91bGKdeWytYJrBfCZHiqDg4_1Bs-MDi6zYcQECyZdL01dxaVljVTGmxL3E2Jnr97oUkQmyy_yDvyXqR9tRsRJFzUfG22snpLYyoDR5NwfhjZmyMhpyV83GzNOH9ollgS1QU7zMNvr"
        }
        monad = await repository.login(session, 1, tenantLogin)
        assert list(monad.get_param_at(0).keys()) == ['houseId', 'firstName', 'lastName', 'email', 'tenantState', 'tenantPosition', 'deviceId']


async def test_Router_tenant_login_returns_401_error_on_invalid_password():
    async with aiohttp.ClientSession() as session:
        tenant = {
            "firstName": "Timmy11",
            "lastName": "Tenant",
            "email": "aaaa@s.com",
            "password": "aaaaaa",
            "tenantState": "Not Approved",
        }
    
        monad = await repository.create_tenant(session, 1, tenant)
        tenantLogin = {
            "email": "aaaa@s.com",
            "password": "bbbbbb",
            "houseKey": "DASFDSF",
            "deviceId": "eigTlTqf3fuwYzBIC1jEv_:APA91bGKdeWytYJrBfCZHiqDg4_1Bs-MDi6zYcQECyZdL01dxaVljVTGmxL3E2Jnr97oUkQmyy_yDvyXqR9tRsRJFzUfG22snpLYyoDR5NwfhjZmyMhpyV83GzNOH9ollgS1QU7zMNvr"
        }
        monad = await repository.login(session, 1, tenantLogin)
        assert monad.error_status == {"status": 401, "reason": "Invalid email or password" }


async def test_Router_tenant_login_returns_404_error_on_non_existing_account():
    async with aiohttp.ClientSession() as session:
        tenantLogin = {
            "email": "fdsafdsafadsf@s.com",
            "password": "bbbbbb",
            "houseKey": "DASFDSF",
            "deviceId": "eigTlTqf3fuwYzBIC1jEv_:APA91bGKdeWytYJrBfCZHiqDg4_1Bs-MDi6zYcQECyZdL01dxaVljVTGmxL3E2Jnr97oUkQmyy_yDvyXqR9tRsRJFzUfG22snpLYyoDR5NwfhjZmyMhpyV83GzNOH9ollgS1QU7zMNvr"
        }
        monad = await repository.login(session, 1, tenantLogin)
        assert monad.error_status == {"status": 404, "reason": "Invalid email or password" }


async def test_Router_tenant_login_returns_403_error_on_invalid_house_id():
    async with aiohttp.ClientSession() as session:
        tenant = {
            "firstName": "Timmy11",
            "lastName": "Tenant",
            "email": "aaaa@s.com",
            "password": "aaaaaa",
            "tenantState": "Not Approved",
        }
        monad = await repository.create_tenant(session, 1, tenant)
        tenantLogin = {
            "email": "aaaa@s.com",
            "password": "aaaaaa",
            "houseKey": "FDSAF",
            "deviceId": "eigTlTqf3fuwYzBIC1jEv_:APA91bGKdeWytYJrBfCZHiqDg4_1Bs-MDi6zYcQECyZdL01dxaVljVTGmxL3E2Jnr97oUkQmyy_yDvyXqR9tRsRJFzUfG22snpLYyoDR5NwfhjZmyMhpyV83GzNOH9ollgS1QU7zMNvr"
        }
        monad = await repository.login(session, 5, tenantLogin)
        assert monad.error_status == {"status": 403, "reason": "Invalid house key"}


async def test_Router_get_tenants_house_id_returns_successfully():
    async with aiohttp.ClientSession() as session:
        tenant = {
            "firstName": "Timmy11",
            "lastName": "Tenant",
            "email": "aaaa@s.com",
            "password": "aaaaaa",
            "tenantState": "Not Approved",
        }
        monad = await repository.create_tenant(session, 1, tenant)
        monad = await repository.get_tenants_by_house_id(session, 1)
        assert len(monad.get_param_at(0)) > 1
