import strawberry
from typing import Optional, Union
from graphql_inputs import *
from graphql_types import *
from resolver import *


@strawberry.type
class Mutation:
    
    #createMaintenanceTicket: MaintenanceTicket = strawberry.mutation(resolver=add_maintenance_ticket)
    #updateMaintenanceTicket: MaintenanceTicket = strawberry.mutation(resolver=update_maintenance_ticket)
    createHouse: House = strawberry.mutation(resolver=add_house)