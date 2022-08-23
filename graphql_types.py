from typing import Optional, Union, List
import strawberry

@strawberry.type
class MaintenanceTicket:
    id: int
    houseId: int
    name: str
    imageURL: Optional[str]
    datePosted: str
    firebaseId: Optional[str]
    description: 'Description'
    urgency: 'Urgency'

@strawberry.type
class Description:
    descriptionText: str

@strawberry.type
class Urgency:
    name: str


@strawberry.type
class LandlordAddress:
    streetNumber: str
    streetName: str
    city: str
    province: str
    postalCode: str
    unitNumber: str
    poBox: str

    


@strawberry.type
class Email:
    email: str
   

@strawberry.type
class ContactInfo:
    contact: str

    

@strawberry.type
class LandlordInfo:
    fullName: str
    receiveDocumentsByEmail: bool
    emails: List[Email]
    contactInfo: bool
    contacts: List[ContactInfo]

    

@strawberry.type
class ParkingDescription:
    description: str

   

@strawberry.type
class RentalAddress:
    streetNumber: str
    streetName: str
    city: str
    province: str
    postalCode: str
    unitName: str
    isCondo: bool
    parkingDescriptions: List[ParkingDescription]

    

@strawberry.type
class RentService:
    name: str
    amount: str

    

@strawberry.type
class PaymentOption:
    name: str

    

@strawberry.type
class Rent:
    baseRent: str
    rentMadePayableTo: str
    rentServices: List[RentService]
    paymentOptions: List[PaymentOption]

    


@strawberry.type
class RentalPeriod:
    rentalPeriod: str
    endDate: str

    

@strawberry.type
class PartialPeriod:
    amount: str
    dueDate: str
    startDate: str
    endDate: str
    isEnabled: bool

    

@strawberry.type
class TenancyTerms:
    rentalPeriod: RentalPeriod
    startDate: str
    rentDueDate: str
    paymentPeriod: str
    partialPeriod: PartialPeriod

    

@strawberry.type
class Detail:
    detail: str

    

@strawberry.type
class Service:
    name: str
    isIncludedInRent: bool
    isPayPerUse: Optional[bool] 
    details: List[Detail]

    


@strawberry.type
class Utility:
    name: str
    responsibility: str
    details: List[Detail]

    

@strawberry.type
class RentDiscout:
    name: str
    amount: str
    details: List[Detail]

    

@strawberry.type
class RentDeposit:
    name: str
    amount: str
    details: List[Detail]

    


@strawberry.type
class AdditionalTerm:
    name: str 
    details: List[Detail]

   
@strawberry.type
class TenantName:
    name: str

    


@strawberry.type
class Lease:
    landlordInfo: LandlordInfo
    landlordAddress: LandlordAddress
    rentalAddress: RentalAddress
    rent: Rent
    tenancyTerms: TenancyTerms
    services: List[Service]
    utilities: List[Utility]
    rentDeposits: List[RentDeposit]
    rentDiscounts: List[RentDiscout]
    additionalTerms: List[AdditionalTerm]
    tenantNames: List[TenantName]

    

@strawberry.type
class House:
    id: int
    houseKey: str
    firebaseId: str
    lease: Lease

