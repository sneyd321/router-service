from models.cloud_run import CloudRun


async def test_Router_service_lists_services_as_dictionary():
    cloudRun = CloudRun()
    cloudRun.discover()
    assert cloudRun.get_maintenance_ticket_hostname() == "https://maintenance-ticket-service-s5xgw6tidq-uc.a.run.app"
        

async def test_Router_return_None_when_service_is_not_discovered():
    cloudRun = CloudRun()
    assert cloudRun.get_service("router") == None



