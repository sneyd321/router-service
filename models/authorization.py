import jwt, os, datetime
from datetime import timezone, datetime, timedelta


class Authorization:


    def get_tenant_scope(self, house):
        scope = [
            "/Tenant",
            "/Profile/Tenant",
            "/SignLease",
            "/MaintenanceTicket",
            f"/House/{house.id}/MaintenanceTicket",
            f"/House/{house.houseKey}"
        ]
        return scope

    def get_landlord_scope(self, landlordId, houses):
        scope = [
            "/Tenant",
            "/Tenant/TempAccountCreated",
            "/Tenant/PendingInvite",
            "/Tenant/Approved",
            "/AddTenantEmail",
            "/Lease/Ontario",
            "/Lease",
            "/House",
            "/Landlord",
            f"/Landlord/{landlordId}",
            f"/Landlord/{landlordId}/House"
        ]
        for house in houses:
            scope.append(f"/House/{house.id}/Tenant")
            scope.append(f"/House/{house.houseKey}")
           
            scope.append(f"/Lease/{house.id}/LandlordInfo")
            scope.append(f"/Lease/{house.id}/LandlordAddress")
            scope.append(f"/Lease/{house.id}/RentalAddress")
            scope.append(f"/Lease/{house.id}/Rent")
            scope.append(f"/Lease/{house.id}/TenancyTerms")
            scope.append(f"/Lease/{house.id}/Services")
            scope.append(f"/Lease/{house.id}/Utilities")
            scope.append(f"/Lease/{house.id}/RentDeposits")
            scope.append(f"/Lease/{house.id}/RentDiscounts")
            scope.append(f"/Lease/{house.id}/AdditionalTerms")
            scope.append(f"/House/{house.id}/MaintenanceTicket")
         
        return scope




    def generate_tenant_token(self, scope):
        payload = {
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=10),
            "scope": scope
        }
        return jwt.encode(payload, os.environ.get("JWT_SECRET", "secret"), algorithm="HS256")
            


    def generate_landlord_token(self, scope):
        payload = {
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=10),
            "scope": scope
        }
        return jwt.encode(payload, os.environ.get("JWT_SECRET", "secret"), algorithm="HS256")


    def get_token_payload(self, token):
        try:
            return jwt.decode(token, os.environ.get("JWT_SECRET", "secret"), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return {}


        
        