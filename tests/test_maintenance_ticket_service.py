from models.repository import Repository
from models.request import Request
from models.cloud_run import CloudRun

cloudRun = CloudRun()
cloudRun.discover_dev()

async def test_Router_insert_maintenance_ticket_successfully():
    request = Request(cloudRun.get_maintenance_ticket_hostname(), "/MaintenanceTicket")
    repository = Repository(request)
    monad = await repository.insert(**{
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
    assert list(monad.get_param_at(0).keys()) == ['houseId', 'id', 'name', 'urgency', 'description', 'sender', 'imageURL', 'datePosted', 'firebaseId']



async def test_Router_get_maintenance_tickets_successfully():
    request = Request(cloudRun.get_maintenance_ticket_hostname(), "/MaintenanceTicket")
    repository = Repository(request)
    monad = await repository.insert(**{
        "houseId": 1,
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
    
    request = Request(cloudRun.get_maintenance_ticket_hostname(), f"/House/1/MaintenanceTicket")
    maintenanceTicketRepository = Repository(request)
    monad = await maintenanceTicketRepository.get()
    print(monad.error_status)
    assert len(monad.get_param_at(0)) > 1


async def test_Router_get_maintenance_ticket_successfully():
    request = Request(cloudRun.get_maintenance_ticket_hostname(), "/MaintenanceTicket")
    repository = Repository(request)
    monad = await repository.insert(**{
        "houseId": 2,
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

    maintenanceTicketId = monad.get_param_at(0)["id"]
    
    request = Request(cloudRun.get_maintenance_ticket_hostname(), f"/House/2/MaintenanceTicket?query={maintenanceTicketId}")
    maintenanceTicketRepository = Repository(request)
    monad = await maintenanceTicketRepository.get()
    print(monad.error_status)
    assert monad.get_param_at(0) != None

