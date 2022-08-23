from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.retry import KazooRetry

class Zookeeper:

    def __init__(self, zookeeperHost):
        self.client = KazooClient(hosts=zookeeperHost)
        self.name = "Router"
        self.host = b"http://localhost:8000"

    def initialize(self):
        self.client.start()
        if not self.client.connected:
            self.client.stop()
            raise Exception("Unable to connect.")

    def create_node(self):
        self.client.ensure_path("Services")
        if not self.client.exists(f"Services/{self.name}"):
            self.client.create(f"Services/{self.name}", ephemeral=True)
        self.client.set(f"Services/{self.name}", self.host)

    def get_children(self):
        return self.client.get_children("Services")

    def get_hostname(self, serviceName):
        if not self.client.exists(f"Services/{serviceName}"):
            return None
        data, stats = self.client.get(f"Services/{serviceName}")
        return data.decode("utf-8")

    def get_maintenance_ticket_hostname(self):
        return self.get_hostname("Maintenance-Ticket-Service")

    def get_lease_hostname(self):
        return self.get_hostname("Lease-Service")

    def get_house_hostname(self):
        return self.get_hostname("House-Service")