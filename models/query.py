import strawberry
from typing import Optional, Union, List
from models.graphql_inputs import *
from models.graphql_types import *
from models.resolver import *

@strawberry.type
class Query:
    getMaintenanceTickets: List[MaintenanceTicket] = strawberry.field(resolver=get_maintenance_tickets)
    getMaintenanceTicket: MaintenanceTicket = strawberry.field(resolver=get_maintenance_ticket_by_id)
    getHouses: List[House] = strawberry.field(resolver=get_houses)
    getHouse: House = strawberry.field(resolver=get_house_by_house_key)
    #getDeviceIds: DeviceId = strawberry.field(resolver=get_device_ids)
    