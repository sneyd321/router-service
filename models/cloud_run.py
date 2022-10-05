from google.cloud import run_v2
from google.oauth2 import service_account

class CloudRun:

    def __init__(self):
        self.services = []

    def initialize(self):
        credentials = service_account.Credentials.from_service_account_file(r"./models/roomr-222721-c05604718d80.json")
        client = run_v2.ServicesClient(credentials=credentials)
        request = run_v2.ListServicesRequest(parent="projects/roomr-222721/locations/us-central1")
        page_result = client.list_services(request=request)
        for service in page_result:
            self.services.append({"name": service.name.split("/")[-1], "host": service.uri})
          
    def get_hostname(self, serviceName):
        for service in self.services:
            if service["name"] == serviceName:
                return service["host"]
        
    def get_maintenance_ticket_hostname(self):
        return self.get_hostname("maintenance-ticket-service")

    def get_lease_hostname(self):
        return self.get_hostname("lease-service")

    def get_house_hostname(self):
        return self.get_hostname("house-service")

    def get_scheduler_hostname(self):
        return self.get_hostname("scheduler")

    def get_tenant_hostname(self):
        return self.get_hostname("tenant-service")

    def get_landlord_hostname(self):
        return self.get_hostname("landlord-service")


