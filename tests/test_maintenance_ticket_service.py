from models.repository import MaintenanceTicketRepository
from models.request import Request
from models.cloud_run import CloudRun
from models.graphql_inputs import MaintenanceTicketInput
import aiohttp

cloudRun = CloudRun()
cloudRun.discover_dev()
#cloudRun.discover()

maintenanceTicketRepository = MaintenanceTicketRepository(cloudRun.get_maintenance_ticket_hostname())

async def test_Router_insert_maintenance_ticket_successfully():
    async with aiohttp.ClientSession() as session:
        maintenanceTicket = MaintenanceTicketInput(**{
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
        monad = await maintenanceTicketRepository.create_maintenance_ticket(session, 1, maintenanceTicket)
        assert monad.get_param_at(0) != None



async def test_Router_get_maintenance_tickets_successfully():
    async with aiohttp.ClientSession() as session:
        maintenanceTicket = MaintenanceTicketInput(**{
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
        monad = await maintenanceTicketRepository.create_maintenance_ticket(session, 1, maintenanceTicket)
        monad = await maintenanceTicketRepository.get_maintenance_tickets(session, 1)
        assert len(monad.get_param_at(0)) > 1


async def test_Router_get_maintenance_ticket_successfully():
    async with aiohttp.ClientSession() as session:
        maintenanceTicket = MaintenanceTicketInput(**{
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
        monad = await maintenanceTicketRepository.create_maintenance_ticket(session, 1, maintenanceTicket)
        maintenanceTicketId = monad.get_param_at(0)["id"]
        monad = await maintenanceTicketRepository.get_maintenance_tickets_by_house_key(session, 1, maintenanceTicketId)
        assert isinstance(monad.get_param_at(0), dict)

