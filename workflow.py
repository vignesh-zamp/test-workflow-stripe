import uuid
import json
import os
from datetime import date, datetime
from typing import List, Dict, Optional
from schemas import ContractExtractionDataset
from validators import run_validation

# Persistent Database File
DB_FILE = "processed_contracts.json"

def load_database() -> List[Dict]:
    """Loads the contract database from a JSON file."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_database(database: List[Dict]):
    """Saves the contract database to a JSON file."""
    # Helper for dates
    def json_serial(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")

    with open(DB_FILE, "w") as f:
        json.dump(database, f, indent=4, default=json_serial)

def get_existing_contract(client: str, effective_date: date, database: List[Dict]) -> Optional[Dict]:
    """
    Matches an amendment to an existing contract using Client and Effective Date.
    """
    # Convert input date to string for comparison if needed, or ensure DB has consistent format
    # The DB loaded from JSON will have dates as strings (ISO format YYYY-MM-DD)
    eff_date_str = effective_date.isoformat() if isinstance(effective_date, (date, datetime)) else str(effective_date)

    for record in database:
        # Check if record matches Client and Effective Date
        # We compare loosely on date strings to avoid parsing issues
        db_date = record.get("contract_effective_date")
        # Handle potential None values
        if not db_date: 
            continue
            
        # Simple string match for date (assuming ISO format from save_database)
        if (record.get("client") == client and db_date == eff_date_str):
            return record
    return None

def process_document(file_path: str, extracted_data: Optional[Dict] = None, is_amendment: Optional[bool] = None):
    """
    Main workflow entry point for a single document.
    """
    run_id = str(uuid.uuid4())
    print(f"--- Processing Run: {run_id} ---")
    print(f"File: {file_path}")

    # Load existing data
    database = load_database()

    # Step 3: Field Extraction (via OCR Agent)
    if not extracted_data:
        from ocr_agent import extract_contract_data
        print("Calling Gemini OCR Agent...")
        extracted_data = extract_contract_data(file_path)
        
        # Convert date strings to date objects for validation logic
        for date_field in ["contract_effective_date", "contract_start_date", "contract_end_date"]:
            if extracted_data.get(date_field):
                try:
                    extracted_data[date_field] = datetime.strptime(extracted_data[date_field], "%Y-%m-%d").date()
                except ValueError:
                    pass 

    # Determine Document Type
    doc_type = extracted_data.get("document_type", "Agreement")
    print(f"Document Type: {doc_type}")
    
    # Logic: Amendment vs Agreement
    is_amendment_doc = (doc_type.lower() == "amendment")

    # Step 4: Amendment Processing
    if is_amendment_doc:
        print("Processing as Amendment...")
        # Match against existing DB
        original_contract = get_existing_contract(
            client=extracted_data.get("client"),
            effective_date=extracted_data.get("contract_effective_date"),
            database=database
        )
        
        if original_contract:
            print("Match Found: Linking to existing contract.")
            # Merge logic: Update original with new data
            # Create a copy to avoid mutating the DB directly before validation
            merged_data = original_contract.copy()
            # Update only non-null fields from amendment
            merged_data.update({k: v for k, v in extracted_data.items() if v is not None})
            
            candidate_data = merged_data
            candidate_data["status"] = "In Progress"
        else:
            print("No Match Found: Treating as new/unlinked document.")
            candidate_data = extracted_data
            candidate_data["status"] = "In Progress"
    else:
        # Master Agreement
        print("Processing as Master Agreement...")
        candidate_data = extracted_data
        candidate_data["status"] = "In Progress"

    # Add System Fields
    candidate_data["activity_run_id"] = run_id
    candidate_data["file_path"] = file_path
    candidate_data["document_type"] = doc_type

    # Step 5: Validation
    validation_result = run_validation(candidate_data)
    
    # Step 6: Storage (Artifact)
    import json
    import os
    output_dir = "output_data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_file = os.path.join(output_dir, f"{run_id}.json")
    
    def json_serial(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError (f"Type {type(obj)} not serializable")

    with open(output_file, "w") as f:
        json.dump(candidate_data, f, indent=4, default=json_serial)
    print(f"Artifact Saved: {output_file}")

    # Update Persistent Database
    if validation_result["is_valid"]:
        print("Validation: PASSED")
        candidate_data["status"] = "Completed"
        
        if is_amendment_doc and 'original_contract' in locals() and original_contract:
             # Find index and update
             # We need a robust way to find the index, assuming object identity might fail after reload
             # We'll match by activity_run_id of the original if possible, or just client/date again
             # For now, let's assume we can find it by the original match
             try:
                 idx = database.index(original_contract)
                 database[idx] = candidate_data
                 print("Storage: Updated existing record in persistent DB.")
             except ValueError:
                 # Fallback if object identity fails (shouldn't if we haven't reloaded)
                 database.append(candidate_data)
                 print("Storage: Warning - Could not update in place, appended new version.")
        else:
            database.append(candidate_data)
            print("Storage: Inserted new record into persistent DB.")
            
    else:
        print("Validation: FAILED")
        print(f"Errors: {validation_result['errors']}")
        candidate_data["status"] = "Needs Attention"
        database.append(candidate_data)
        print("Storage: Saved as 'Needs Attention' in persistent DB.")

    # Save DB back to disk
    save_database(database)

    return candidate_data
