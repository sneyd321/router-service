from models.repository import TenantRepository
from models.cloud_run import CloudRun
from models.graphql_inputs import TenantInput, LoginTenantInput
import uuid
import aiohttp
import json
import pytest

cloudRun = CloudRun()
#cloudRun.discover_dev()
cloudRun.discover()
repository = TenantRepository(cloudRun.get_tenant_hostname())


async def test_Router_create_temp_tenant_returns_successfully():
    async with aiohttp.ClientSession() as session:
        with open("./tests/samples/temp_tenant.json", mode="r") as temp_tenant:
            tenantInput = json.load(temp_tenant)
            tenantInput["email"] = str(uuid.uuid4())
        monad = await repository.create_temp_tenant(session, "/Tenant", 1, tenantInput, isTest=True)
        assert not monad.has_errors()


async def test_Router_tenant_login_returns_successfully():
    async with aiohttp.ClientSession() as session:
        email = str(uuid.uuid4())
        with open("./tests/samples/temp_tenant.json", mode="r") as temp_tenant:
            tenantEmailInput = json.load(temp_tenant)
            tenantEmailInput["email"] = email
        monad = await repository.create_temp_tenant(session, "/Tenant", 1, tenantEmailInput, isTest=True)
        
        with open("./tests/samples/tenant.json", mode="r") as tenant:
            tenantInput = json.load(tenant)
            tenantInput["email"] = email
        monad = await repository.update_tenant_state(session, "/Tenant/Approved", "Approved", tenantInput)

        with open("./tests/samples/tenant.json", mode="r") as tenant:
            tenantInput = json.load(tenant)
            tenantInput["email"] = email
        monad = await repository.update_tenant_state(session, "/Tenant/Approved", "Approved", tenantInput)
        monad = await repository.update_tenant(session, "/Tenant", tenantInput)


        with open("./tests/samples/tenant_login.json", mode="r") as tenant_login:
            tenantLoginInput = json.load(tenant_login)
            tenantLoginInput["email"] = email
        monad = await repository.login(session, 1, tenantLoginInput)
        assert not monad.has_errors()


async def test_Router_get_tenants_house_id_returns_successfully():
    async with aiohttp.ClientSession() as session:
        email = str(uuid.uuid4())
        with open("./tests/samples/temp_tenant.json", mode="r") as temp_tenant:
            tenantEmailInput = json.load(temp_tenant)
            tenantEmailInput["email"] = email
        await repository.create_temp_tenant(session, "/Tenant", 4, tenantEmailInput, isTest=True)
        
        monad = await repository.get_tenants_by_house_id(session, "/House/4/Tenant", 4)
        assert len(monad.get_param_at(0)) > 0

async def test_Router_update_tenant_state_successfully():
    async with aiohttp.ClientSession() as session:
        email = str(uuid.uuid4())
        with open("./tests/samples/temp_tenant.json", mode="r") as temp_tenant:
            tenantEmailInput = json.load(temp_tenant)
            tenantEmailInput["email"] = email
        await repository.create_temp_tenant(session, "/Tenant", 1, tenantEmailInput, isTest=True)
        
        with open("./tests/tenant.json", mode="r") as tenant:
            tenantInput = json.load(tenant)
            tenantInput["email"] = email
        monad = await repository.update_tenant_state(session, "/Tenant/Approved", "Approved", tenantInput)
        assert not monad.has_errors()


async def test_Router_update_tenant_successfully():
    async with aiohttp.ClientSession() as session:
        email = str(uuid.uuid4())
        with open("./tests/samples/temp_tenant.json", mode="r") as temp_tenant:
            tenantEmailInput = json.load(temp_tenant)
            tenantEmailInput["email"] = email
        monad = await repository.create_temp_tenant(session, "/Tenant", 1, tenantEmailInput, isTest=True)
        
        with open("./tests/samples/tenant.json", mode="r") as tenant:
            tenantInput = json.load(tenant)
            tenantInput["email"] = email
        await repository.update_tenant_state(session, "/Tenant/Approved", "Approved", tenantInput)
        monad = await repository.update_tenant(session, "/Tenant", tenantInput)

        assert not monad.has_errors()


async def test_Router_delete_tenant_successfully():
    async with aiohttp.ClientSession() as session:
        email = str(uuid.uuid4())
        with open("./tests/samples/temp_tenant.json", mode="r") as temp_tenant:
            tenantEmailInput = json.load(temp_tenant)
            tenantEmailInput["email"] = email
        monad = await repository.create_temp_tenant(session, "/Tenant", 1, tenantEmailInput, isTest=True)
        
        with open("./tests/samples/tenant.json", mode="r") as tenant:
            tenantInput = json.load(tenant)
            tenantInput["email"] = email
        await repository.update_tenant_state(session, "/Tenant/Approved", "Approved", tenantInput)
        monad = await repository.delete_tenant(session, "/Tenant", tenantInput)

        assert not monad.has_errors()