import os
import json
import typing
import google.generativeai as genai
from schemas import ContractExtractionDataset

# Configure the API key
# Best practice: Read from environment variable
API_KEY = os.environ.get("GEMINI_API_KEY")

def configure_genai(api_key: str = None):
    """Configures the Gemini API with the provided key."""
    key = api_key or API_KEY
    if not key:
        raise ValueError("Gemini API Key not found. Please set GEMINI_API_KEY environment variable or pass it explicitly.")
    genai.configure(api_key=key)

def extract_contract_data(file_path: str, mime_type: str = "application/pdf") -> typing.Dict:
    """
    Uploads a file to Gemini and extracts contract data according to the schema.
    """
    if not API_KEY and not os.environ.get("GEMINI_API_KEY"):
         print("Warning: No API Key provided. Returning mock data for simulation.")
         return _get_mock_data(file_path)

    try:
        configure_genai()
        
        # 1. Upload the file
        print(f"Uploading file: {file_path}...")
        sample_file = genai.upload_file(path=file_path, display_name="Contract PDF")
        print(f"File uploaded: {sample_file.uri}")

        # 2. Initialize the model
        # Using Gemini 1.5 Pro (or Flash) which supports document understanding
        model = genai.GenerativeModel(model_name="gemini-2.5-flash")

        # 3. Construct the prompt
        prompt = """
        You are an expert legal AI assistant. Your task is to extract structured data from the attached contract PDF.
        
        **Classification Rule:**
        - Check the 'header' (Document Title). 
        - If the header contains the word "Amendment" (case-insensitive), set 'document_type' to "Amendment".
        - Otherwise (e.g., if it says "Fee Schedule", "Master Services Agreement", etc.), set 'document_type' to "Agreement".

        **Field Recognition Logic:**
        
        1. Contract Metadata
        - contract_effective_date: The date when the contract becomes legally binding. Look for "Effective Date" label followed by signature date or explicit date statement.
        - contract_start_date: Date services begin. Often same as effective date unless explicitly stated. Look for "Services commence on".
        - contract_end_date: Date initial term expires. Calculate from effective_date + initial_term; look for "expires on".
        - header: Official title/name of the contract. Usually at top, large font/bold.
        - client: Customer/user entity. Look for "User" field in header table or signature block.
        
        2. Commercial Values
        - total_contract_value: Total monetary value. Calculate from volume commitments x rates if not explicit.
        - product_rates: Pricing/fees. Found in fee tables (percentage or fixed).
        - product_skus: Specific product identifiers. Look in fee tables/section headers.
        - products: High-level product categories. Found in section headers and "Services" definitions.
        - autorenewal: "Yes" or "No". Look in "Term" section for "automatically renew".
        
        3. Territory Fields
        - direct_platform_territories: Locations for direct services. Look for "Territory" field.
        - connect_territories: Territories where Stripe Connect is available.
        - active_in_multiple_territories: Boolean. Check if territory list has >1 country.
        
        4. Incentive Structures
        - incentives_credits_discounts_rebates_type: Category of incentive (discount, credit, rebate).
        - incentives_credits_discounts_rebates_amount: Monetary value or percentage.
        - incentives_credits_discounts_rebates_start_date: When incentive becomes active.
        - incentives_credits_discounts_rebates_end_date: When incentive expires.
        
        5. Legal Terms
        - notice_period: Advance notice for termination. Look in "Term" section.
        - stripe_legal_entity: Specific Stripe entity contracting.
        - signing_user_entity_country_geography: Customer country/region.
        - legal_entity_modification: Changes to legal entity structure. Look for amendments/entity changes.
        
        6. Subscription Details
        - subscription_start_date: When subscription begins. Usually same as contract start date.
        - contract_renewal_date: Date up for renewal. Calculate from start_date + initial_term.

        **Output Format:**
        Return a valid JSON object with these fields. If a field is not found, return null.
        - document_type (String: "Agreement" or "Amendment")
        - contract_effective_date (YYYY-MM-DD)
        - contract_start_date (YYYY-MM-DD)
        - contract_end_date (YYYY-MM-DD)
        - header
        - client
        - total_contract_value (Integer)
        - product_rates
        - product_skus
        - products
        - autorenewal
        - direct_platform_territories
        - connect_territories
        - active_in_multiple_territories
        - incentives_credits_discounts_rebates_type
        - incentives_credits_discounts_rebates_amount
        - incentives_credits_discounts_rebates_start_date
        - incentives_credits_discounts_rebates_end_date
        - notice_period
        - stripe_legal_entity
        - signing_user_entity_country_geography
        - legal_entity_modification
        - subscription_start_date
        - contract_renewal_date
        """

        # 4. Generate content
        print("Generating extraction...")
        response = model.generate_content([sample_file, prompt])
        
        # 5. Parse response
        response_text = response.text.strip()
        # Clean up markdown if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        data = json.loads(response_text)
        return data

    except Exception as e:
        print(f"Error during OCR extraction: {e}")
        return {}

def _get_mock_data(file_path: str) -> typing.Dict:
    """Returns mock data for testing without API key."""
    from datetime import date
    # Simple logic to return different mock data based on filename
    if "001" in file_path:
         return {
            "header": "Master Services Agreement",
            "client": "Acme Corp",
            "contract_effective_date": "2024-01-01",
            "contract_start_date": "2024-01-01",
            "contract_end_date": "2025-01-01",
            "total_contract_value": 120000,
            "products": "Payments, Connect",
            "direct_platform_territories": "US, CA"
        }
    elif "002" in file_path:
        return {
            "header": "Master Services Agreement",
            "client": "Acme Corp",
            "contract_effective_date": "2024-01-01",
            "total_contract_value": 150000,
            "products": "Payments, Connect, Radar"
        }
    return {}
