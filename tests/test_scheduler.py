from models.repository import Repository
from models.request import Request
from models.cloud_run import CloudRun

import json

cloudRun = CloudRun()
cloudRun.discover_dev()


async def test_Router_schedules_maintenance_ticket_upload_successfully():
    request = Request(cloudRun.get_scheduler_hostname(), "/MaintenanceTicket")
    repository = Repository(request)
    monad = await repository.insert(**{
        "firebaseId": "str",
        "imageURL": "str",
        "houseKey": "str",
        "maintenanceTicketId": 1,
        "description": "str",
        "firstName": "str",
        "lastName": "str",
        "image": "str"
    })
    assert monad.get_param_at(0) == {"status": "Job scheduled successfully"}
    
   

async def test_Router_schedules_generate_lease_upload_successfully():
    request = Request(cloudRun.get_scheduler_hostname(), "/Lease/Ontario")
    repository = Repository(request)
    with open(r"./tests/lease_test.json", mode="r") as lease_json:
        leaseData = json.load(lease_json)
    monad = await repository.insert(**leaseData)
    assert monad.get_param_at(0) == {"status": "Job scheduled successfully"}

async def test_Router_schedules_add_tenant_email_upload_successfully():
    request = Request(cloudRun.get_scheduler_hostname(), "/AddTenantEmail")
    repository = Repository(request)
    monad = await repository.insert(**{
        "firstName": "str",
        "lastName": "str",
        "email": "str",
        "houseKey": "str",
        "documentURL": "str",
        "firebaseId": "str",
    })
    assert monad.get_param_at(0) == {"status": "Job scheduled successfully"}

async def test_Router_schedules_sign_tenant_upload_successfully():
    request = Request(cloudRun.get_scheduler_hostname(), "/SignLease")
    repository = Repository(request)
    monad = await repository.insert(**{
        "firstName": "str",
        "lastName": "str",
        "email": "str",
        "documentURL": "str",
        "tenantPosition": 0,
        "tenantState": "str",
        "signiture": "str",
        "firebaseId": "str",
    })
    assert monad.get_param_at(0) == {"status": "Job scheduled successfully"}
