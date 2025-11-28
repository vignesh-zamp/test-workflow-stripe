# Comparative Analysis: Stripe Contract Extraction Workflows

## 1. Executive Summary

| Feature | Version A (Existing `contract_extraction`) | Version B (New Implementation) |
| :--- | :--- | :--- |
| **Architecture** | Complex, Event-Driven Framework (`pantheon_v2`) | Lightweight, Standalone Python Script |
| **AI Models** | Bedrock Claude 3.5 Sonnet & 3.7 | Google Gemini 2.5 Flash |
| **Execution** | Asynchronous, Distributed (Child Workflows) | Synchronous, Single-Process |
| **Classification** | Agent-based Reasoning (Probabilistic) | **Rule-based (Header Check) + AI (Deterministic)** |
| **Extraction** | 6 Parallel Agents (High Latency/Cost) | **Single Pass Extraction (Low Latency/Cost)** |
| **Storage** | Database Activity (Abstracted) | **Local Persistent JSON (`processed_contracts.json`)** |
| **Runnability** | Requires complex environment/SDK setup | **Runs immediately with `python main.py`** |

**Verdict:**
**Version B is superior for this specific use case** because it strictly adheres to your custom business logic (e.g., "Header must contain Amendment"), runs locally without heavy dependencies, and uses a deterministic matching strategy that is easier to debug and maintain. Version A is over-engineered for a local extraction task and lacks the specific strict rules you requested.

---

## 2. Deep Dive: Version A (`contract_extraction` folder)

### Logic & Flow
*   **Framework**: Built on `pantheon_v2`, utilizing `ActionsHub` for orchestration. This suggests it's designed for a distributed, serverless, or temporal-like environment.
*   **Step 1: Ingestion**: Handles Email and PDF inputs via `_process_email_ingestion`.
*   **Step 2: Classification**: Uses a `ChainOfThoughtWorkflow` with Claude 3.5 Sonnet.
    *   *Critique*: It relies on the LLM to "reason" about the document type. It **does not** enforce the strict "Header must contain 'Amendment'" rule you specified. This can lead to hallucinations or inconsistent classification.
*   **Step 3: Extraction**: Spawns **6 parallel child workflows** (`_extract_metadata_fields`, `_extract_commercial_fields`, etc.).
    *   *Critique*: While parallel, this triples or quadruples the API costs and complexity. A single modern LLM context window can easily handle all 31 fields in one pass.
*   **Step 4: Amendment Processing**: Uses another agent to "query database" and "match contracts".
    *   *Critique*: The matching logic is opaque (hidden inside the agent's "reasoning"). It doesn't explicitly enforce the "Client + Effective Date" exact match rule.
*   **Step 5: Validation**: Another agent-based validation step.

### Errors & Gaps
1.  **Over-Complexity**: The code requires a specific SDK (`zamp_public_workflow_sdk`, `pantheon_v2`) which is likely not installed or configured locally, making it unrunnable "out of the box".
2.  **Missing Strict Rules**: The classification and matching logic are delegated to AI agents without the strict guardrails you requested (Header check, specific field matching).
3.  **No Local Persistence**: It seems to rely on an external DB service via `ContractStorageActivity`, so you wouldn't see a local JSON file updating.

---

## 3. Deep Dive: Version B (New Implementation)

### Logic & Flow
*   **Architecture**: A clean Python script (`workflow.py`) orchestrated by `main.py`.
*   **Step 1: Ingestion**: Scans a local `input_contracts` folder.
*   **Step 2: Classification (Strict)**:
    *   **Rule**: The OCR agent prompt explicitly instructs: *"If the header contains the word 'Amendment'... set 'document_type' to 'Amendment'. Otherwise... 'Agreement'."*
    *   **Code**: `workflow.py` reads this `document_type` directly.
*   **Step 3: Extraction (Efficient)**:
    *   Uses a single Gemini 2.5 Flash call to extract all fields at once.
    *   Schema is strictly defined in `schemas.py` using Pydantic.
*   **Step 4: Amendment Matching (Deterministic)**:
    *   **Rule**: `workflow.py` loads `processed_contracts.json` and iterates through it.
    *   **Logic**: It explicitly checks `if record['client'] == new_client and record['contract_effective_date'] == new_date`. This guarantees a correct match if the data exists.
*   **Step 5: Storage**:
    *   Updates `processed_contracts.json` in place.
    *   Saves individual run artifacts in `output_data/`.

### Why it fits your needs
*   **Custom Logic**: It implements the *exact* logic you dictated (Header check, Client+Date match).
*   **Transparency**: You can open `processed_contracts.json` and see exactly what the "database" looks like.
*   **Speed**: Single-pass extraction is significantly faster than spinning up 6 parallel agents.

---

## 4. Recommendations for Correction (if using Version A)

If you *must* use the Version A codebase, here is what needs to be corrected to match your requirements:

1.  **Hardcode Classification Rule**: Modify `_classify_document` in `stripe_contract_extraction_workflow.py` to parse the `ocr_result` header *before* calling the agent. If "Amendment" is in the header, force the type to `AMENDMENT`.
2.  **Simplify Extraction**: Merge the 6 parallel extraction activities into one `_extract_all_fields` activity to reduce overhead and cost.
3.  **Implement Deterministic Matching**: In `_process_amendment`, instead of asking an agent to "query database", write code that queries your actual backend using the specific `client` and `contract_effective_date` filters.
4.  **Local Mode**: Add a "Local Mode" to the `ContractStorageActivity` that writes to a JSON file instead of trying to connect to a cloud database.
