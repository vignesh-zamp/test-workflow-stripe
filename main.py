import os
import glob
from datetime import date
from workflow import process_document

def load_env():
    """Simple .env loader"""
    env_path = ".env"
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value

def main():
    load_env()
    print("=== Starting Stripe Contract Extraction System ===\n")
    
    input_dir = "input_contracts"
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in '{input_dir}'.")
        print("Please add contract PDFs to this folder and run again.")
    else:
        print(f"Found {len(pdf_files)} documents in '{input_dir}'. Processing...")
        for pdf_file in pdf_files:
            try:
                # We pass None for extracted_data to trigger the OCR agent
                # We pass None for is_amendment to let the agent detect it
                process_document(pdf_file, extracted_data=None, is_amendment=None)
                print("\n" + "-"*30 + "\n")
            except Exception as e:
                print(f"Failed to process {pdf_file}: {e}")

    print("=== Final Database State ===")
    from workflow import load_database
    database = load_database()
    for idx, record in enumerate(database):
        print(f"Record {idx + 1}:")
        print(f"  Client: {record.get('client')}")
        print(f"  Type: {record.get('document_type')}")
        print(f"  Status: {record.get('status')}")
        print(f"  TCV: {record.get('total_contract_value')}")
        print("-" * 20)

if __name__ == "__main__":
    main()
