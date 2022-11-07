from google.cloud import run_v2
from google.oauth2 import service_account

class CloudRun:

    def __init__(self, filePath=r"./models/static/ServiceAccount.json"):
        self.services = {}
        credentials = service_account.Credentials.from_service_account_file(filePath)
        self.client = run_v2.ServicesClient(credentials=credentials)

    def discover(self):
        request = run_v2.ListServicesRequest(parent="projects/roomr-222721/locations/us-central1")
        page_result = self.client.list_services(request=request)
        for service in page_result:
            self.services[service.name.split("/")[-1]] = service.uri

    def discover_dev(self):
        self.services = {
        'router': 'http://localhost:8081', 
        'landlord-service': 'http://localhost:8086', 
        'tenant-service': 'http://localhost:8085', 
        'roomr-tenant': '', 
        'lease-service': 'http://localhost:8000', 
        'house-service': 'http://localhost:8082', 
        'scheduler': 'https://scheduler-s5xgw6tidq-uc.a.run.app', 
        'maintenance-ticket-service': 'http://localhost:8083'
    }

    
    def get_service(self, name):
        try:
            return self.services[name]
        except KeyError:
            return None
            
    def get_maintenance_ticket_hostname(self):
        return self.get_service("maintenance-ticket-service")

    def get_maintenance_ticket_test_hostname(self):
        return self.get_service("maintenance-ticket-service-test")

    def get_lease_hostname(self):
        return self.get_service("lease-service")

    def get_lease_test_hostname(self):
        return self.get_service("lease-service-test")

    def get_house_hostname(self):
        return self.get_service("house-service")

    def get_house_test_hostname(self):
        return self.get_service("house-service-test")

    def get_scheduler_hostname(self):
        return self.get_service("scheduler")

    def get_scheduler_test_hostname(self):
        return self.get_service("scheduler-test")

    def get_tenant_hostname(self):
        return self.get_service("tenant-service")

    def get_tenant_test_hostname(self):
        return self.get_service("tenant-service-test")

    def get_landlord_hostname(self):
        return self.get_service("landlord-service")

    def get_landlord_test_hostname(self):
        return self.get_service("landlord-service-test")


