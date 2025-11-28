from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

class ContractMetadata(BaseModel):
    contract_effective_date: date = Field(..., description="The date when the contract becomes legally binding and enforceable")
    contract_start_date: date = Field(..., description="The date when services under the contract begin")
    contract_end_date: date = Field(..., description="The date when the initial contract term expires")
    header: str = Field(..., description="The official title/name of the contract document")
    client: str = Field(..., description="The customer/user entity entering into the agreement")

class CommercialValues(BaseModel):
    total_contract_value: int = Field(..., description="The total monetary value of the contract over its lifetime")
    product_rates: Optional[str] = Field(None, description="The pricing/fees charged for each service or product")
    product_skus: Optional[str] = Field(None, description="Specific product/service identifiers or categories")
    products: Optional[str] = Field(None, description="High-level product categories being offered")
    autorenewal: Optional[str] = Field(None, description="Whether the contract automatically renews at term end")

class TerritoryFields(BaseModel):
    direct_platform_territories: Optional[str] = Field(None, description="Geographic locations where the direct/platform services are provided")
    connect_territories: Optional[str] = Field(None, description="Territories where Stripe Connect (platform) services are available")
    active_in_multiple_territories: Optional[str] = Field(None, description="Boolean indicating if services span multiple countries/regions")

class IncentiveStructures(BaseModel):
    incentives_credits_discounts_rebates_type: Optional[str] = Field(None, description="The category/nature of financial incentives provided")
    incentives_credits_discounts_rebates_amount: Optional[str] = Field(None, description="The monetary value or percentage of the incentive")
    incentives_credits_discounts_rebates_start_date: Optional[date] = Field(None, description="When the incentive becomes active")
    incentives_credits_discounts_rebates_end_date: Optional[date] = Field(None, description="When the incentive expires")

class LegalTerms(BaseModel):
    notice_period: Optional[str] = Field(None, description="Required advance notice for termination or non-renewal")
    stripe_legal_entity: Optional[str] = Field(None, description="The specific Stripe corporate entity that is the contracting party")
    signing_user_entity_country_geography: Optional[str] = Field(None, description="The country/region where the customer entity is located/incorporated")
    legal_entity_modification: Optional[str] = Field(None, description="Whether there are changes to legal entity structure or rights during the contract")

class SubscriptionDetails(BaseModel):
    subscription_start_date: Optional[date] = Field(None, description="When the ongoing subscription/service relationship begins")
    contract_renewal_date: Optional[date] = Field(None, description="The date when the contract is up for renewal")

class SystemFields(BaseModel):
    activity_run_id: str = Field(..., description="Unique ID for the process run")
    status: str = Field(..., description="Current status of the process run")
    file_path: str = Field(..., description="Path to the source file")

class ContractExtractionDataset(BaseModel):
    # Flattened structure for the dataset as per the SOP requirements
    # System Fields
    activity_run_id: str
    status: str
    file_path: str
    document_type: str = Field(..., description="Type of document: 'Agreement' or 'Amendment'")
    
    # Contract Metadata
    contract_effective_date: date
    contract_start_date: date
    contract_end_date: date
    header: str
    client: str
    
    # Commercial Values
    total_contract_value: int
    product_rates: Optional[str] = None
    product_skus: Optional[str] = None
    products: Optional[str] = None
    autorenewal: Optional[str] = None
    
    # Territory Fields
    direct_platform_territories: Optional[str] = None
    connect_territories: Optional[str] = None
    active_in_multiple_territories: Optional[str] = None
    
    # Incentive Structures
    incentives_credits_discounts_rebates_type: Optional[str] = None
    incentives_credits_discounts_rebates_amount: Optional[str] = None
    incentives_credits_discounts_rebates_start_date: Optional[date] = None
    incentives_credits_discounts_rebates_end_date: Optional[date] = None
    
    # Legal Terms
    notice_period: Optional[str] = None
    stripe_legal_entity: Optional[str] = None
    signing_user_entity_country_geography: Optional[str] = None
    legal_entity_modification: Optional[str] = None
    
    # Subscription Details
    subscription_start_date: Optional[date] = None
    contract_renewal_date: Optional[date] = None
