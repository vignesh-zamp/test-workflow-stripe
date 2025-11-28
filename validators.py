from datetime import date
from typing import List, Dict, Any
from schemas import ContractExtractionDataset

def validate_mandatory_fields(data: Dict[str, Any]) -> List[str]:
    """Checks for presence of mandatory fields."""
    mandatory_fields = [
        "contract_effective_date",
        "contract_start_date",
        "contract_end_date",
        "header",
        "client",
        "total_contract_value"
    ]
    errors = []
    for field in mandatory_fields:
        if not data.get(field):
            errors.append(f"Missing mandatory field: {field}")
    return errors

def validate_logical_checks(data: Dict[str, Any]) -> List[str]:
    """Performs logical checks on dates and values."""
    errors = []
    
    # Date logic
    start_date = data.get("contract_start_date")
    end_date = data.get("contract_end_date")
    
    if start_date and end_date:
        if isinstance(start_date, str):
            # In a real scenario, we'd parse this. Assuming it's already a date object or valid string for now
            pass 
        if start_date > end_date:
            errors.append(f"Contract start date ({start_date}) cannot be after end date ({end_date})")

    # Numeric logic
    tcv = data.get("total_contract_value")
    if tcv is not None and tcv < 0:
        errors.append("Total contract value cannot be negative")

    return errors

def run_validation(data: Dict[str, Any]) -> Dict[str, Any]:
    """Runs all validation checks and returns a status and error list."""
    errors = []
    errors.extend(validate_mandatory_fields(data))
    errors.extend(validate_logical_checks(data))
    
    if errors:
        return {"is_valid": False, "errors": errors}
    return {"is_valid": True, "errors": []}
