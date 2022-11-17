import jwt, os, datetime
from datetime import timezone, datetime, timedelta


class Authorization:

    def get_landlord_scope(self, landlordId, houses):
        scope = [
            "/Tenant",
            "/Tenant/TempAccountCreated",
            "/Tenant/InvitePending",
            "/Tenant/Approved",
            "/AddTenantEmail",
            "/Lease/Ontario",
            "/House",
            f"/Landlord/{landlordId}/House"
        ]
        for house in houses:
            scope.append(f"/House/{house.id}/Tenant")
            scope.append(f"/House/{house.houseKey}")
            scope.append(f"/Lease")
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
            scope.append(f"/Lease/{house.id}/MaintenanceTicket")
         
        return scope




    
            

    

    def generate_landlord_token(self, scope):
        payload = {
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=10),
            "scope": scope
        }
        return jwt.encode(payload, "secret", algorithm="HS256")


    def get_token_payload(self, token):
        try:
            return jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return {}


        
        