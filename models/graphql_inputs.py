from typing import Optional, Union, List
import strawberry

@strawberry.input
class DescriptionInput:
    descriptionText: str

    def to_json(self):
        return {
            "descriptionText": self.descriptionText
        }

@strawberry.input
class UrgencyInput:
    name: str

    def to_json(self):
        return {
            "name": self.name
        }

@strawberry.input
class MaintenanceTicketSenderInput:
    firstName: str
    lastName: str
    email: str

    def to_json(self):
        return {
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email
        } 

@strawberry.input
class MaintenanceTicketInput:
    houseId: int
    description: DescriptionInput
    urgency: UrgencyInput
    sender: MaintenanceTicketSenderInput

    def to_json(self):
        return {
            "description": self.description.to_json(),
            "urgency": self.urgency.to_json(),
            "sender": self.sender.to_json()
        }



@strawberry.input
class LandlordAddressInput:
    streetNumber: str
    streetName: str
    city: str
    province: str
    postalCode: str
    unitNumber: str
    poBox: str

    def to_json(self):
        return {
            "streetNumber": self.streetNumber,
            "streetName": self.streetName,
            "city": self.city,
            "province": self.province,
            "postalCode": self.postalCode,
            "unitNumber": self.unitNumber,
            "poBox": self.poBox
        }
 

@strawberry.input
class EmailInput:
    email: str

    def to_json(self): 
        return  {
            "email": self.email
        }

@strawberry.input
class ContactInfoInput:
    contact: str

    def to_json(self): 
        return  {
            "contact": self.contact
        }

@strawberry.input
class LandlordInfoInput:
    fullName: str
    receiveDocumentsByEmail: bool
    emails: List[EmailInput]
    contactInfo: bool
    contacts: List[ContactInfoInput]

    def to_json(self): 
        return  {
            "fullName": self.fullName,
            "receiveDocumentsByEmail": self.receiveDocumentsByEmail,
            "contactInfo": self.contactInfo,
            "contacts": self.contacts,
            "emails": self.emails
        }

@strawberry.input
class ParkingDescriptionInput:
    description: str

    def to_json(self): 
        return {
            "description": self.description
        }

@strawberry.input
class RentalAddressInput:
    streetNumber: str
    streetName: str
    city: str
    province: str
    postalCode: str
    unitName: str
    isCondo: bool
    parkingDescriptions: List[ParkingDescriptionInput]


@strawberry.input
class RentServiceInput:
    name: str
    amount: str

    def to_json(self):
        return {
            "name": self.name,
            "amount": self.amount
        }

@strawberry.input
class PaymentOptionInput:
    name: str

    def to_json(self):
        return {
            "name": self.name
        }

@strawberry.input
class RentInput:
    baseRent: str
    rentMadePayableTo: str
    rentServices: List[RentServiceInput]
    paymentOptions: List[PaymentOptionInput]

    def to_json(self):
        return {
            "baseRent": self.baseRent,
            "rentMadePayableTo": self.rentMadePayableTo,
            "rentServices": [rentService.to_json() for rentService in self.rentServices],
            "paymentOptions": [paymentOption.to_json() for paymentOption in self.paymentOptions]
        }

@strawberry.input
class RentalPeriodInput:
    rentalPeriod: str
    endDate: str

    def to_json(self):
        return {
            "rentalPeriod": self.rentalPeriod,
            "endDate": self.endDate
        }

@strawberry.input
class PartialPeriodInput:
    amount: str
    dueDate: str
    startDate: str
    endDate: str
    isEnabled: bool

    def to_json(self):
        return {
            "amount": self.amount,
            "dueDate": self.dueDate,
            "startDate": self.startDate,
            "endDate": self.endDate,
            "isEnabled": self.isEnabled
        }

@strawberry.input
class TenancyTermsInput:
    rentalPeriod: RentalPeriodInput
    startDate: str
    rentDueDate: str
    paymentPeriod: str
    partialPeriod: PartialPeriodInput

    def to_json(self):
        return {
            "startDate": self.startDate,
            "rentDueDate": self.rentDueDate,
            "paymentPeriod": self.paymentPeriod,
            "rentalPeriod": self.rentalPeriod.to_json(),
            "partialPeriod": self.partialPeriod.to_json()
        }

    

@strawberry.input
class DetailInput:
    detail: str

    def to_json(self):
        return {
            "detail": self.detail
        }

@strawberry.input
class ServiceInput:
    name: str
    isIncludedInRent: bool
    isPayPerUse: Optional[bool]
    details: List[DetailInput]

    def to_json(self):
        return {
            "name": self.name,
            "isIncludedInRent": self.isIncludedInRent,
            "isPayPerUse": self.isPayPerUse,
            "details": [detail.to_json() for detail in self.details]
        }


@strawberry.input
class UtilityInput:
    name: str
    responsibility: str
    details: List[DetailInput]

    def to_json(self):
        return {
            "name": self.name,
            "responsibility": self.responsibility,
            "details": [detail.to_json() for detail in self.details]
        }

@strawberry.input
class RentDiscountInput:
    name: str
    amount: str
    details: List[DetailInput]

    def to_json(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "details": [detail.to_json() for detail in self.details]
        }

@strawberry.input
class RentDepositInput:
    name: str
    amount: str
    details: List[DetailInput]

    def to_json(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "details": [detail.to_json() for detail in self.details]
        }

@strawberry.input
class AdditionalTermInput:
    name: str 
    details: List[DetailInput]

    def to_json(self):
        return {
            "name": self.name,
            "details": [detail.to_json() for detail in self.details]
        }


    


@strawberry.input
class LeaseInput:
    landlordInfo: LandlordInfoInput
    landlordAddress: LandlordAddressInput
    rentalAddress: RentalAddressInput
    rent: RentInput
    tenancyTerms: TenancyTermsInput
    services: List[ServiceInput]
    utilities: List[UtilityInput]
    rentDeposits: List[RentDepositInput]
    rentDiscounts: List[RentDiscountInput]
    additionalTerms: List[AdditionalTermInput]

    def to_json(self):
        return {
            "landlordInfo": self.landlordInfo,
            "landlordAddress": self.landlordAddress,
            "rentalAddress": self.rentalAddress,
            "rent": self.rent,
            "tenancyTerms": self.tenancyTerms,
            "services": self.services,
            "utilities": self.utilities,
            "rentDiscounts": self.rentDiscounts,
            "rentDeposits": self.rentDeposits,
            "additionalTerms": self.additionalTerms
        }

  




@strawberry.input
class AddTenantEmailInput:
    firstName: str
    lastName: str
    email: str
    tenantState: str


    def to_json(self):
        return {
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "tenantState": self.tenantState,
        }


@strawberry.input
class TenantInput:
    firstName: str
    lastName: str
    email: str
    password: str
    tenantState: str



    def to_json(self):
        return {
            'firstName': self.firstName, 
            'lastName': self.lastName, 
            'email': self.email, 
            'password': self.password, 
            'tenantState': self.tenantState
        }

@strawberry.input
class LoginTenantInput:
    email: str
    password: str
    houseKey: str
    deviceId: str

@strawberry.input
class LandlordInput:
    firstName: str
    lastName: str
    email: str
    password: str

    def to_json(self):
        return {
            "firstName": self.firstName,
            "lastName": self.lastName,
            'email': self.email, 
            'password': self.password, 
        }


@strawberry.input
class LoginLandlordInput:
    email: str
    password: str
    deviceId: str




