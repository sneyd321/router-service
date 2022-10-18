from models.repository import Repository
from models.request import Request
from models.cloud_run import CloudRun

cloudRun = CloudRun()
cloudRun.discover_dev()


async def test_Router_insert_tenant_returns_successfully():
    request = Request(cloudRun.get_tenant_hostname(), "/Tenant")
    repository = Repository(request)
    monad = await repository.insert(**{
        "firstName": "Timmy11",
        "lastName": "Tenant",
        "email": "aaa@s.com",
        "password": "aaaaaa",
        "tenantState": "Not Approved",
        "houseId": 1
    })
    assert list(monad.get_param_at(0).keys()) == ['houseId', 'firstName', 'lastName', 'email', 'tenantState', 'tenantPosition', 'deviceId']


async def test_Router_insert_tenant_returns_conflict_error_on_duplicate_email():
    request = Request(cloudRun.get_tenant_hostname(), "/Tenant")
    repository = Repository(request)
    monad = await repository.insert(**{
        "firstName": "Timmy11",
        "lastName": "Tenant",
        "email": "aaaa@s.com",
        "password": "aaaaaa",
        "tenantState": "Not Approved",
        "houseId": 1
    })
    request = Request(cloudRun.get_tenant_hostname(), "/Tenant")
    repository = Repository(request)
    monad = await repository.insert(**{
        "firstName": "Timmy11",
        "lastName": "Tenant",
        "email": "aaaa@s.com",
        "password": "aaaaaa",
        "tenantState": "Not Approved",
        "houseId": 1
    })
    monad.error_status == {"status": 409, "reason": "Failed to insert data into database" }


async def test_Router_tenant_login_returns_successfully():
    request = Request(cloudRun.get_tenant_hostname(), "/Tenant")
    repository = Repository(request)
    monad = await repository.insert(**{
        "firstName": "Timmy11",
        "lastName": "Tenant",
        "email": "g@s.com",
        "password": "aaaaaa",
        "tenantState": "Not Approved",
        "houseId": 2
    })
    
    request = Request(cloudRun.get_tenant_hostname(), "/Login")
    repository = Repository(request)
    monad = await repository.insert(**{
        "email": "g@s.com",
        "password": "aaaaaa",
        "houseId": 2,
        "deviceId": "eigTlTqf3fuwYzBIC1jEv_:APA91bGKdeWytYJrBfCZHiqDg4_1Bs-MDi6zYcQECyZdL01dxaVljVTGmxL3E2Jnr97oUkQmyy_yDvyXqR9tRsRJFzUfG22snpLYyoDR5NwfhjZmyMhpyV83GzNOH9ollgS1QU7zMNvr"
    })
    print(monad.error_status)
    assert list(monad.get_param_at(0).keys()) == ['houseId', 'firstName', 'lastName', 'email', 'tenantState', 'tenantPosition', 'deviceId']


async def test_Router_tenant_login_returns_401_error_on_invalid_password():
    request = Request(cloudRun.get_tenant_hostname(), "/Tenant")
    repository = Repository(request)
    monad = await repository.insert(**{
        "firstName": "Timmy11",
        "lastName": "Tenant",
        "email": "g@s.com",
        "password": "aaaaaa",
        "tenantState": "Not Approved",
        "houseId": 2
    })
    
    request = Request(cloudRun.get_tenant_hostname(), "/Login")
    repository = Repository(request)
    monad = await repository.insert(**{
        "email": "g@s.com",
        "password": "bbbbbb",
        "houseId": 2,
        "deviceId": "eigTlTqf3fuwYzBIC1jEv_:APA91bGKdeWytYJrBfCZHiqDg4_1Bs-MDi6zYcQECyZdL01dxaVljVTGmxL3E2Jnr97oUkQmyy_yDvyXqR9tRsRJFzUfG22snpLYyoDR5NwfhjZmyMhpyV83GzNOH9ollgS1QU7zMNvr"
    })
    assert monad.error_status == {"status": 401, "reason": "Invalid email or password" }


async def test_Router_tenant_login_returns_404_error_on_non_existing_account():
    request = Request(cloudRun.get_tenant_hostname(), "/Login")
    repository = Repository(request)
    monad = await repository.insert(**{
        "email": "fdasfdsafa@h.com",
        "password": "aaaaaa",
        "houseId": 2,
        "deviceId": "eigTlTqf3fuwYzBIC1jEv_:APA91bGKdeWytYJrBfCZHiqDg4_1Bs-MDi6zYcQECyZdL01dxaVljVTGmxL3E2Jnr97oUkQmyy_yDvyXqR9tRsRJFzUfG22snpLYyoDR5NwfhjZmyMhpyV83GzNOH9ollgS1QU7zMNvr"
    })
    assert monad.error_status == {"status": 404, "reason": "Invalid email or password" }


async def test_Router_tenant_login_returns_403_error_on_invalid_house_id():
    request = Request(cloudRun.get_tenant_hostname(), "/Tenant")
    repository = Repository(request)
    monad = await repository.insert(**{
        "firstName": "Timmy11",
        "lastName": "Tenant",
        "email": "g@s.com",
        "password": "aaaaaa",
        "tenantState": "Not Approved",
        "houseId": 5
    })
    
    request = Request(cloudRun.get_tenant_hostname(), "/Login")
    repository = Repository(request)
    monad = await repository.insert(**{
        "email": "g@s.com",
        "password": "aaaaaa",
        "houseId": 5,
        "deviceId": "eigTlTqf3fuwYzBIC1jEv_:APA91bGKdeWytYJrBfCZHiqDg4_1Bs-MDi6zYcQECyZdL01dxaVljVTGmxL3E2Jnr97oUkQmyy_yDvyXqR9tRsRJFzUfG22snpLYyoDR5NwfhjZmyMhpyV83GzNOH9ollgS1QU7zMNvr"
    })
    assert monad.error_status == {"status": 403, "reason": "Invalid house key"}


async def test_Router_get_tenants_house_id_returns_successfully():
    request = Request(cloudRun.get_tenant_hostname(), "/Tenant")
    repository = Repository(request)
    monad = await repository.insert(**{
        "firstName": "Timmy11",
        "lastName": "Tenant",
        "email": "fdfsassafdsafas@s.com",
        "password": "aaaaaa",
        "tenantState": "Not Approved",
        "houseId": 4
    })
    print(monad.error_status)
    
    request = Request(cloudRun.get_tenant_hostname(), "/House/4/Tenant")
    repository = Repository(request)
    monad = await repository.get()
    print(monad.error_status)
    assert len(monad.get_param_at(0)) > 1
