"""
Data models for contract sections
Defines structure for each section of the contract document
"""
from pydantic import BaseModel, EmailStr
from typing import List, Optional


class CustomerInfo(BaseModel):
    """Section 1: Customer Information"""
    customerName: str
    primaryContact: str
    addressLine1: str
    city: str
    state: str
    zip: str
    emailAddress: str
    billingAddressLine: str
    billingCity: str
    billingState: str
    billingZip: str
    language: str = "English"


class Site(BaseModel):
    """Individual site information"""
    esiid: str
    startOption: str  # "move-in", "switch", "renew"
    startDate: str
    addressLine: str
    city: str
    state: str
    zip: str


class SitesInfo(BaseModel):
    """Section 2: Sites and Contract Terms Information"""
    sites: List[Site]
    contractStartDate: str
    contractEndDate: str
    contractDuration: str


class EFLInfo(BaseModel):
    """Section 3: Electricity Facts Label Information"""
    contractPrice: str  # Price per kWh
    averagePrice: Optional[str] = None
    basePricePerKwh: Optional[str] = None
    # Additional EFL fields can be added as needed


class NRGTerms(BaseModel):
    """Section 4: NRG Terms of Service (Hardcoded - no dynamic fields)"""
    pass  # Static content, no variables needed


class CustomerRights(BaseModel):
    """Section 5: Your Rights as a Customer (Hardcoded - no dynamic fields)"""
    pass  # Static content, no variables needed


class ContractData(BaseModel):
    """Complete contract data structure combining all sections"""
    customer_info: CustomerInfo
    sites_info: SitesInfo
    efl_info: EFLInfo
    nrg_terms: Optional[NRGTerms] = None
    customer_rights: Optional[CustomerRights] = None


# Helper function to convert from existing flat structure to section-based structure
def convert_legacy_data(legacy_data: dict) -> ContractData:
    """
    Convert existing flat contract data structure to section-based structure
    Maintains backward compatibility with existing API
    """
    customer_info = CustomerInfo(
        customerName=legacy_data.get('customerName', ''),
        primaryContact=legacy_data.get('primaryContact', ''),
        addressLine1=legacy_data.get('addressLine1', ''),
        city=legacy_data.get('city', ''),
        state=legacy_data.get('state', ''),
        zip=legacy_data.get('zip', ''),
        emailAddress=legacy_data.get('emailAddress', ''),
        billingAddressLine=legacy_data.get('billingAddressLine', ''),
        billingCity=legacy_data.get('billingCity', ''),
        billingState=legacy_data.get('billingState', ''),
        billingZip=legacy_data.get('billingZip', ''),
        language=legacy_data.get('language', 'English')
    )

    sites_info = SitesInfo(
        sites=[Site(**site) for site in legacy_data.get('sites', [])],
        contractStartDate=legacy_data.get('startDate', ''),
        contractEndDate=legacy_data.get('endDate', ''),
        contractDuration=legacy_data.get('contractDuration', '')
    )

    efl_info = EFLInfo(
        contractPrice=legacy_data.get('contractPrice', ''),
        averagePrice=legacy_data.get('averagePrice'),
        basePricePerKwh=legacy_data.get('basePricePerKwh')
    )

    return ContractData(
        customer_info=customer_info,
        sites_info=sites_info,
        efl_info=efl_info
    )
