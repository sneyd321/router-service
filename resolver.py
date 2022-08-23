import strawberry
from typing import Optional, Union, List
from graphql_inputs import *
from graphql_types import *
from request import Request
from monad import MaybeMonad
from zookeeper import Zookeeper
import json
zk = Zookeeper("localhost:2181")


async def maintenance_tickets() -> List[MaintenanceTicket]:
    request = Request("http://localhost:8080")
    monad = await MaybeMonad(*("/House/1/MaintenanceTicket")).bind(request.post)
    if monad.errors:
        raise Exception(monad.errors["Error"])
    jsonArray = monad.result
    return [MaintenanceTicket(**json) for json in jsonArray]


async def get_maintenance_ticket_by_id(id: strawberry.ID) -> MaintenanceTicket:
    request = Request("http://localhost:8080")
    monad = await MaybeMonad(*("/House/1/MaintenanceTicket")).bind(request.post)
    if monad.errors:
        raise Exception(monad.errors["Error"])

    for json in monad.result:
        if json["id"] == int(id):
            return MaintenanceTicket(**json)


async def add_maintenance_ticket(maintenanceTicket: MaintenanceTicketInput) -> MaintenanceTicket:
        data = maintenanceTicket.__dict__
        data["description"] = maintenanceTicket.description.__dict__
        data["urgency"] = maintenanceTicket.urgency.__dict__

   
        hostname = zk.get_maintenance_ticket_hostname()
        if not hostname:
            raise Exception("Maintenance Ticket Service not available")

        request = Request(monad.result, "/MaintenanceTicket")
        monad = MaybeMonad(data)
        monad = await monad.bind(request.post)
        if monad.errors:
            raise Exception(monad.errors["Error"])

        return MaintenanceTicket(**monad.result)


async def update_maintenance_ticket(id: strawberry.ID, maintenanceTicket: ImageURLFirebaseInput) -> MaintenanceTicket:
        data = maintenanceTicket.__dict__
        hostname = zk.get_maintenance_ticket_hostname()
        if not hostname:
           raise Exception("Maintenance Ticket Service not available")
        request = Request(hostname, f"/MaintenanceTicket/{id}", payload=data)
        monad = MaybeMonad(data)
        monad = await monad.bind(request.put)
        if monad.errors:
            raise Exception(monad.errors["Error"])
        return MaintenanceTicket(**monad.result)


async def add_house(houseInput: HouseInput) -> House:
    #Get house service
    hostname = zk.get_house_hostname()
    if not hostname:
        raise Exception("House Service not available")
    request = Request(hostname, f"/Landlord/2/House")
    monad = MaybeMonad(data={"firebaseId": houseInput.firebaseId})
    monad = await monad.bind(request.post)
    if monad.errors:
        raise Exception(monad.errors["Error"])
    print(monad.result)
    house = House(**monad.result, lease=houseInput.lease)
    
    #Get lease service
    hostname = zk.get_lease_hostname()
    if not hostname:
        raise Exception("Lease Service not available")
    request = Request(hostname, f"/House/{house.id}/Lease")
    monad = MaybeMonad(houseInput.lease.to_json())
    monad = await monad.bind(request.post)
    if monad.errors:
        raise Exception(monad.errors["Error"])

    return house
    

