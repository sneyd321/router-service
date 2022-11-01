import strawberry
from typing import Optional, Union
from models.graphql_inputs import *
from models.graphql_types import *
from models.resolver import *


@strawberry.type
class Mutation:
    
    createMaintenanceTicket: MaintenanceTicket = strawberry.mutation(resolver=add_maintenance_ticket)
    
    createHouse: House = strawberry.mutation(resolver=add_house)
    
    updateLandlordInfo: LandlordInfo = strawberry.mutation(resolver=update_landlord_info)
    updateLandlordAddress: LandlordAddress = strawberry.mutation(resolver=update_landlord_address)
    updateRentalAddress: RentalAddress = strawberry.mutation(resolver=update_rental_address)
    updateRent: Rent = strawberry.mutation(resolver=update_rent)
    updateTenancyTerms: TenancyTerms = strawberry.mutation(resolver=update_tenancy_terms)
    updateServices = strawberry.mutation(resolver=update_services)
    updateUtilities = strawberry.mutation(resolver=update_utilities)
    updateRentDiscounts = strawberry.mutation(resolver=update_rent_discounts)
    updateRentDeposits = strawberry.mutation(resolver=update_rent_deposits)
    updateAdditionalTerms = strawberry.mutation(resolver=update_additional_terms)

    #scheduleLease: LeaseSchedule = strawberry.field(resolver=schedule_lease)

    addTenant: Tenant = strawberry.field(resolver=add_tenant)
    createTenant: Tenant = strawberry.field(resolver=create_tenant_account)

    #createLandlord: Landlord = strawberry.field(resolver=create_landlord_account)

    loginTenant: Tenant = strawberry.field(resolver=tenant_login)
    #loginLandlord: Landlord = strawberry.field(resolver=landlord_login)
