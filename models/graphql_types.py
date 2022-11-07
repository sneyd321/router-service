from typing import Optional, Union, List
import strawberry
@strawberry.type
class MaintenanceTicket:
    id: int
    houseId: int
    name: str
    imageURL: str
    datePosted: str
    firebaseId: str
    description: 'Description'
    urgency: 'Urgency'
    sender: 'MaintenanceTicketSender'


    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.houseId = kwargs.get("houseId")
        self.name = kwargs.get("name")
        self.imageURL = kwargs.get("imageURL")
        self.urgency = Urgency(**kwargs.get("urgency", {}))
        self.description = Description(**kwargs.get("description", {}))
        self.sender = MaintenanceTicketSender(**kwargs.get("sender", {}))
        self.datePosted = kwargs.get("datePosted")
        self.firebaseId = kwargs.get("firebaseId")



@strawberry.type
class MaintenanceTicketSender:
    firstName: str
    lastName: str
    email: str

    def __init__(self, **kwargs):
        self.firstName = kwargs.get("firstName")
        self.lastName = kwargs.get("lastName")
        self.email = kwargs.get("email")


@strawberry.type
class Description:
    descriptionText: str

    def __init__(self, **kwargs):
        self.descriptionText = kwargs.get("descriptionText", "")

@strawberry.type
class Urgency:
    name: str

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")


@strawberry.type
class LandlordAddress:
    streetNumber: str
    streetName: str
    city: str
    province: str
    postalCode: str
    unitNumber: str
    poBox: str

    def __init__(self, **kwargs):
        self.streetNumber = kwargs.get("streetNumber")
        self.streetName = kwargs.get("streetName")
        self.city = kwargs.get("city")
        self.province = kwargs.get("province")
        self.postalCode = kwargs.get("postalCode")
        self.unitNumber = kwargs.get("unitNumber")
        self.poBox = kwargs.get("poBox")



    


@strawberry.type
class Email:
    email: str
    def __init__(self, **kwargs):
        self.email = kwargs.get("email")


   

@strawberry.type
class ContactInfo:
    contact: str
    def __init__(self, **kwargs):
        self.contact = kwargs.get("contact")

 
    

@strawberry.type
class LandlordInfo:
    fullName: str
    receiveDocumentsByEmail: bool
    emails: List[Email]
    contactInfo: bool
    contacts: List[ContactInfo]

    def __init__(self, **kwargs):
        self.fullName = kwargs.get("fullName")
        self.receiveDocumentsByEmail = kwargs.get("receiveDocumentsByEmail")
        self.contactInfo = kwargs.get("contactInfo")
        self.contacts = [ContactInfo(**json) for json in kwargs.get("contacts")]
        self.emails = [Email(**json) for json in kwargs.get("emails")]



    

@strawberry.type
class ParkingDescription:
    description: str

    def __init__(self, **kwargs):
        self.description = kwargs.get("description")

   

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

    def __init__(self, **kwargs):
        self.streetNumber = kwargs.get("streetNumber")
        self.streetName = kwargs.get("streetName")
        self.city = kwargs.get("city")
        self.province = kwargs.get("province")
        self.postalCode = kwargs.get("postalCode")
        self.unitName = kwargs.get("unitName")
        self.isCondo = kwargs.get("isCondo")
        self.parkingDescriptions = [ParkingDescription(**json) for json in kwargs.get("parkingDescriptions", [])]


    

@strawberry.type
class RentService:
    name: str
    amount: str

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.amount = kwargs.get("amount")

   


    

@strawberry.type
class PaymentOption:
    name: str

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")


    

@strawberry.type
class Rent:
    baseRent: str
    rentMadePayableTo: str
    rentServices: List[RentService]
    paymentOptions: List[PaymentOption]

    def __init__(self, **kwargs):
        self.baseRent = kwargs.get("baseRent")
        self.rentMadePayableTo = kwargs.get("rentMadePayableTo")
        self.rentServices = [RentService(**json) for json in kwargs.get("rentServices")]
        self.paymentOptions = [PaymentOption(**json) for json in kwargs.get("paymentOptions")]





@strawberry.type
class RentalPeriod:
    rentalPeriod: str
    endDate: str

    def __init__(self, **kwargs):
        self.rentalPeriod = kwargs.get("rentalPeriod")
        self.endDate = kwargs.get("endDate", "")



    

@strawberry.type
class PartialPeriod:
    amount: str
    dueDate: str
    startDate: str
    endDate: str
    isEnabled: bool

    def __init__(self, **kwargs):
        self.amount = kwargs.get("amount")
        self.dueDate = kwargs.get("dueDate")
        self.startDate = kwargs.get("startDate")
        self.endDate = kwargs.get("endDate")
        self.isEnabled = kwargs.get("isEnabled")



    

@strawberry.type
class TenancyTerms:
    rentalPeriod: RentalPeriod
    startDate: str
    rentDueDate: str
    paymentPeriod: str
    partialPeriod: PartialPeriod

    def __init__(self, **kwargs):
        self.startDate = kwargs.get("startDate")
        self.rentDueDate = kwargs.get("rentDueDate")
        self.paymentPeriod = kwargs.get("paymentPeriod")
        self.rentalPeriod = RentalPeriod(**kwargs.get("rentalPeriod"))
        self.partialPeriod = PartialPeriod(**kwargs.get("partialPeriod"))



    

@strawberry.type
class Detail:
    detail: str

    def __init__(self, **kwargs):
        self.detail = kwargs.get("detail")



    

@strawberry.type
class Service:
    name: str
    isIncludedInRent: bool
    isPayPerUse: Optional[bool] 
    details: List[Detail]

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.isIncludedInRent = kwargs.get("isIncludedInRent")
        self.isPayPerUse = kwargs.get("isPayPerUse", False)
        self.details = [Detail(**json) for json in kwargs.get("details")]




    


@strawberry.type
class Utility:
    name: str
    responsibility: str
    details: List[Detail]

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.responsibility = kwargs.get("responsibility")
        self.details = [Detail(**json) for json in kwargs.get("details")]



    

@strawberry.type
class RentDiscount:
    name: str
    amount: str
    details: List[Detail]

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.amount = kwargs.get("amount")
        self.details = [Detail(**json) for json in kwargs.get("details")]


@strawberry.type
class RentDeposit:
    name: str
    amount: str
    details: List[Detail]

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.amount = kwargs.get("amount")
        self.details = [Detail(**json) for json in kwargs.get("details")]





@strawberry.type
class AdditionalTerm:
    name: str 
    details: List[Detail]

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.details = [Detail(**json) for json in kwargs.get("details")]



@strawberry.type
class Lease:
    id: int
    houseId: int
    documentURL: Optional[str]
    documentName: str
    documentState: str
    landlordInfo: LandlordInfo
    landlordAddress: LandlordAddress
    rentalAddress: RentalAddress
    rent: Rent
    tenancyTerms: TenancyTerms
    services: List[Service]
    utilities: List[Utility]
    rentDeposits: List[RentDeposit]
    rentDiscounts: List[RentDiscount]
    additionalTerms: List[AdditionalTerm]

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.houseId = kwargs.get("houseId")
        self.landlordInfo = LandlordInfo(**kwargs.get("landlordInfo"))
        self.landlordAddress = LandlordAddress(**kwargs.get("landlordAddress"))
        self.rentalAddress = RentalAddress(**kwargs.get("rentalAddress"))
        self.rent = Rent(**kwargs.get("rent"))
        self.tenancyTerms = TenancyTerms(**kwargs.get("tenancyTerms"))
        self.services = [Service(**service) for service in kwargs.get("services")]
        self.utilities = [Utility(**utility) for utility in kwargs.get("utilities")]
        self.rentDiscounts = [RentDiscount(**rentDiscount) for rentDiscount in kwargs.get("rentDiscounts")]
        self.rentDeposits = [RentDeposit(**rentDeposit) for rentDeposit in kwargs.get("rentDeposits")]
        self.additionalTerms = [AdditionalTerm(**additionalTerm) for additionalTerm in kwargs.get("additionalTerms")]
        self.documentURL = kwargs.get("documentURL")
        self.documentName = kwargs.get("documentName")
        self.documentState = kwargs.get("documentState")


    

@strawberry.type
class House:
    id: int
    landlordId: int
    houseKey: str
    firebaseId: str
    lease: Lease

@strawberry.type
class NewHouse:
    id: int
    landlordId: int
    houseKey: str
    firebaseId: str


@strawberry.type
class LeaseSchedule:
    firebaseId: str
    lease: Lease

@strawberry.type
class Tenant:
    firstName: str
    lastName: str
    email: str
    tenantState: str
    tenantPosition: int
    houseId: int
    deviceId: str


@strawberry.type
class Landlord:
    id: int
    firstName: str
    lastName: str
    email: str
    deviceId: str

@strawberry.type
class DeviceId:
    landlordDeviceId: str
    tenantDeviceIds: List[str]

    
