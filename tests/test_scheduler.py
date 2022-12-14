from models.repository import SchedulerRepository
from models.request import Request
from models.cloud_run import CloudRun
from models.graphql_types import MaintenanceTicket, Lease, Tenant

import json, aiohttp

cloudRun = CloudRun()
#cloudRun.discover_dev()
cloudRun.discover()
repository = SchedulerRepository(cloudRun.get_scheduler_test_hostname())

async def test_Router_schedules_maintenance_ticket_upload_successfully():
    async with aiohttp.ClientSession() as session:
        maintenanceTicket = MaintenanceTicket(**{
                "id": 1,
                "name": "MaintenanceTicket",
                "imageURL": "str",
                "datePosted": "str",
                "firebaseId": "str",
                "houseId": 3,
                "description": {
                    "descriptionText": "fdagfdasfsdfasdfa"
                },
                "urgency": {
                    "name": "Low"
                },
                "sender": {
                    "firstName": "Ryan",
                    "lastName": "Sneyd",
                    "email": "a@s.com"
                }
            })
        monad = await repository.schedule_maintenance_ticket_upload(session, "DAFFDS", "FirebaseID", maintenanceTicket, "<Base 64 String>")
        assert monad.get_param_at(0) == {"status": "Job scheduled successfully"}
    
   

async def test_Router_schedules_generate_lease_upload_successfully():
    async with aiohttp.ClientSession() as session:
        with open(r"./tests/schedule_lease.json", mode="r") as lease_json:
            leaseData = json.load(lease_json)
        monad = await repository.schedule_lease(session, "FirebaseID", leaseData)
        assert monad.get_param_at(0) == {"status": "Job scheduled successfully"}

async def test_Router_schedules_add_tenant_email_upload_successfully():
    async with aiohttp.ClientSession() as session:
        tenant = Tenant(**{
            "firstName": "Timmy11",
            "lastName": "Tenant",
            "email": "a@s.com",
            "tenantState": "Not Approved",
            "tenantPosition": 1,
            "houseId": 1,
            "deviceId": ""
        })
        monad = await repository.schedule_add_tenant_email(session, "ADASDS", "FirebaseID", "URL", tenant)
        assert monad.get_param_at(0) == {"status": "Job scheduled successfully"}

async def test_Router_schedules_sign_tenant_upload_successfully():
    async with aiohttp.ClientSession() as session:
        tenant = Tenant(**{
            "firstName": "Timmy11",
            "lastName": "Tenant",
            "email": "a@s.com",
            "tenantState": "Not Approved",
            "tenantPosition": 1,
            "houseId": 1,
            "deviceId": ""
        })
        monad = await repository.schedule_sign_lease(session, tenant, "firebaseId", "documentURL", "signature")
        assert monad.get_param_at(0) == {"status": "Job scheduled successfully"}
