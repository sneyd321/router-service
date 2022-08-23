import strawberry
from typing import Optional, Union, List
from graphql_inputs import *
from graphql_types import *
from resolver import maintenance_tickets, get_maintenance_ticket_by_id

@strawberry.type
class Query:
    getMaintenanceTickets: List[MaintenanceTicket] = strawberry.field(resolver=maintenance_tickets)
    getMaintenanceTicket:  MaintenanceTicket = strawberry.field(resolver=get_maintenance_ticket_by_id)
