# **![][image1]** 

# **Process Document**

**Stripe x Zamp \- Contract Extraction**  
**November 2025**  
---

## **1\. Process Identification**

### **Process Name**

Stripe Contract Extraction (Master Agreements & Amendments)

### **Brief Objective**

To automatically ingest, classify, and extract structured commercial contract data from Stripe agreements delivered via email. The system parses contractual PDFs, identifies whether each document is a master agreement or an amendment, extracts the required business fields, and maintains an accurate and continuously updated dataset of Stripe commercial terms.

### **Business Value**

* **Accuracy:** Ensures reliable visibility into key commercial terms such as pricing, renewal dates, incentives, and product entitlements.

* **Operational Efficiency:** Removes manual data entry effort and accelerates contract processing for Stripe’s commercial teams.

* **Compliance:** Maintains a consistent and auditable record of financial and legal obligations.

* **Continuity:** Tracks amendments and automatically updates affected contract records, ensuring contract truth is always current.

---

## **2\. Process Executive Summary**

The Stripe Contract Extraction system receives contract PDFs via email. Once ingested, each document is classified as either a new master agreement or an amendment to an existing one. Autonomous agents extract all required contract fields, following predefined field definitions aligned with the contract dataset schema.

When amendments are detected, the system links the amendment to its corresponding original agreement using the *Header* field referenced within the amendment text. Extracted amendment values partially overwrite only those fields explicitly changed, ensuring continuity of terms across the contract lifecycle. Updated contract records are stored in Stripe’s internal dataset, maintaining a central and up-to-date source of commercial truth.

This pipeline ensures Stripe’s commercial, legal, finance, and revenue teams have consistent, validated, and searchable contract data, enabling better operational visibility and strategic insight.

---

## **3\. Detailed Process Walkthrough**

---

### **Step 1: Ingestion & Filtering**

**Performed by:** Pace Email Parse  
**Tools / Systems:** Email Inbox, PDF Reader  
**Input:** Emails containing **PDF contract attachments**  
**Output:** A queue of extracted PDF documents ready for parsing

**Process Summary**

* Emails are monitored for incoming Stripe contract PDFs.

* Only attachments in PDF format are considered.

* Non-contract formats (images, inline text, unsupported files) are ignored or flagged.

* Duplicate files (based on filename \+ metadata) are filtered out.

**Decision Points**

* Is the attachment a valid contractual PDF?

* Has this document been processed before?

**Exception Handling**

* Invalid or unreadable PDFs are logged for manual review.

* Duplicate files are skipped and recorded.

---

### **Step 2: Document Parsing & Classification**

**Performed by:** Pace OCR  
**Tools / Systems:** Text Extraction, Document Classifier  
**Input:** PDF content  
**Output:** Parsed text \+ Classification (Master Agreement / Amendment)

**Process Summary**

* PDF text and structural segments are extracted.

* Title blocks, headers, and key phrases are analyzed.

* The system determines whether:

  * The document is a **new master agreement**, or

  * An **amendment** referencing a previous agreement.

**Decision Points**

* Does the document header, title block, or body contain phrases indicating an amendment (e.g., “Amendment”, “Amends Agreement titled…”)?

* Does the amendment reference the *Header* (agreement title) of an existing contract?

---

### 

### 

### **Step 3: Field Extraction (Master Agreements)**

**Performed by:** Pace OCR  
**Tools:** Field Extraction Models (Gemini), Field Dictionary  
**Input:** Parsed text from a master agreement  
**Output:** Structured dataset record populated with Stripe contract fields

**Process Summary**  
The agent extracts all required business fields aligned to the table schema, including:

* **Contract metadata**  
   `contract_effective_date`, `contract_start_date`, `contract_end_date`, `header`, `client`

* **Commercial values**  
   `total_contract_value`, `product_rates`, `product_skus`, `products`, `autorenewal`

* **Territory fields**  
   `direct_platform_territories`, `connect_territories`, `active_in_multiple_territories`

* **Incentive structures**  
   `incentives_credits_discounts_rebates_type`,  
   `incentives_credits_discounts_rebates_amount`,  
   `incentives_credits_discounts_rebates_start_date`,  
   `incentives_credits_discounts_rebates_end_date`

* **Legal Terms**  
   `notice_period`, `stripe_legal_entity`, `signing_user_entity_country_geography`,  
   `legal_entity_modification`

* **Subscription Details**  
   `subscription_start_date`, `contract_renewal_date`

All fields are extracted following standardized formatting rules (date normalization, numeric extraction, text summarization, etc.).

## 

## **`Field Recognition Logic & Descriptions`**

### **`1. Contract Metadata`**

**`contract_effective_date`**

* **`Description`**`: The date when the contract becomes legally binding and enforceable`  
* **`Recognition Logic`**`: Look for "Effective Date" label followed by signature date or explicit date statement`

**`contract_start_date`**

* **`Description`**`: The date when services under the contract begin`  
* **`Recognition Logic`**`: Often same as effective date unless explicitly stated otherwise; look for "Services commence on" or similar language`

**`contract_end_date`**

* **`Description`**`: The date when the initial contract term expires`  
* **`Recognition Logic`**`: Calculate from effective_date + initial_term; look for "expires on" or explicit end date`

**`header`**

* **`Description`**`: The official title/name of the contract document`  
* **`Recognition Logic`**`: Usually found at top of document, often in larger font or bold`

**`client`**

* **`Description`**`: The customer/user entity entering into the agreement`  
* **`Recognition Logic`**`: Look for "User" field in header table or signature block; may list multiple entities`

### **`2. Commercial Values`**

**`total_contract_value`**

* **`Description`**`: The total monetary value of the contract over its lifetime`  
* **`Recognition Logic`**`: Usually not explicitly stated in usage-based contracts; would need to be calculated from volume commitments × rates`

**`product_rates`**

* **`Description`**`: The pricing/fees charged for each service or product`  
* **`Recognition Logic`**`: Found in fee tables; look for percentage rates and fixed fees per transaction/service`

**`product_skus`**

* **`Description`**`: Specific product/service identifiers or categories`  
* **`Recognition Logic`**`: Look for service type names in fee tables and section headers`

**`products`**

* **`Description`**`: High-level product categories being offered`  
* **`Recognition Logic`**`: Found in section headers and "Services" definitions`

**`autorenewal`**

* **`Description`**`: Whether the contract automatically renews at term end`  
* **`Recognition Logic`**`: Look in "Term" section for language about "automatically renew"`

### **`3. Territory Fields`**

**`direct_platform_territories`**

* **`Description`**`: Geographic locations where the direct/platform services are provided`  
* **`Recognition Logic`**`: Look for "Territory" field in header table listing countries/regions`

**`connect_territories`**

* **`Description`**`: Territories where Stripe Connect (platform) services are available`  
* **`Recognition Logic`**`: May be separate from direct territories; look for Connect-specific territory lists`

**`active_in_multiple_territories`**

* **`Description`**`: Boolean indicating if services span multiple countries/regions`  
* **`Recognition Logic`**`: Check if territory list contains more than one country/region`

### **`4. Incentive Structures`**

**`incentives_credits_discounts_rebates_type`**

* **`Description`**`: The category/nature of financial incentives provided`  
* **`Recognition Logic`**`: Look for sections mentioning "discounts," "credits," "rebates," "incentives," volume-based pricing tiers, or promotional terms`

**`incentives_credits_discounts_rebates_amount`**

* **`Description`**`: The monetary value or percentage of the incentive`  
* **`Recognition Logic`**`: Calculate difference between tier rates or look for explicit credit amounts`

**`incentives_credits_discounts_rebates_start_date`**

* **`Description`**`: When the incentive becomes active`  
* **`Recognition Logic`**`: Look for effective dates of promotional tiers or explicit incentive start dates`

**`incentives_credits_discounts_rebates_end_date`**

* **`Description`**`: When the incentive expires`  
* **`Recognition Logic`**`: Look for expiration dates, tier change dates, or contract end dates`

### **`5. Legal Terms`**

**`notice_period`**

* **`Description`**`: Required advance notice for termination or non-renewal`  
* **`Recognition Logic`**`: Look in "Term" section for "notice of non-renewal at least X days"`

**`stripe_legal_entity`**

* **`Description`**`: The specific Stripe corporate entity that is the contracting party`  
* **`Recognition Logic`**`: Look for "Stripe entity" in header or "Stripe" definition section`

**`signing_user_entity_country_geography`**

* **`Description`**`: The country/region where the customer entity is located/incorporated`  
* **`Recognition Logic`**`: Extract from user entity description, look for incorporation language or address`

**`legal_entity_modification`**

* **`Description`**`: Whether there are changes to legal entity structure or rights during the contract`  
* **`Recognition Logic`**`: Look for amendments, entity changes, or modification clauses`

### **`6. Subscription Details`**

**`subscription_start_date`**

* **`Description`**`: When the ongoing subscription/service relationship begins`  
* **`Recognition Logic`**`: Usually same as contract start date for service agreements`

**`contract_renewal_date`**

* **`Description`**`: The date when the contract is up for renewal`  
* **`Recognition Logic`**`: Calculate from start_date + initial_term; look for renewal language`

## **`Additional Extraction Logic Guidelines`**

### **`General Recognition Patterns:`**

1. **`Date Formats`**`: Watch for various formats (April 30, 2024 / 30/04/2024 / 2024-04-30)`  
2. **`Currency Indicators`**`: Fees will have currency codes (USD, CAD, AUD, GBP, EUR, etc.)`  
3. **`Percentage vs Fixed Fees`**`: Percentages have "%" symbol; fixed fees have currency codes`  
4. **`Tier Structures`**`: Look for "Fee Tier X" or volume brackets like "USD 0 to 5,000,000"`  
5. **`Entity Lists`**`: Multiple entities often listed with "By:" signature blocks or in comma-separated lists`  
6. **`Section Headers`**`: Key terms often in dedicated sections (Term, Definitions, Fees, Territory)`  
7. **`Tables`**`: Commercial terms typically in tabular format with clear column headers`  
8. **`Signature Blocks`**`: Effective dates, parties, and authorized signatories appear here`  
9. **`DocuSign Elements`**`: Electronic signature systems add envelope IDs and signature dates`  
10. **`Supersession Clauses`**`: Look for language about replacing previous agreements`

### **`Complex Field Relationships:`**

* **`Volume Tiers → Incentives`**`: Lower rates at higher volumes = implicit volume discounts`  
* **`Multiple Territories → FX Fees`**`: Cross-border transactions trigger foreign exchange fees`  
* **`Contract Type → Fee Structure`**`: Platform agreements have Connect fees; Direct agreements may not`  
* **`Initial Term + Auto-renewal → Total Duration`**`: Indefinite unless terminated with proper notice`

---

### **Step 4: Amendment Detection & Processing**

**Performed by:** Pace  
**Input:** Parsed PDF \+ Extracted Header, User, Contract Effective Date  
**Output:** Updated contract record or new contract entry

**Core Logic**

When a document is suspected to be an amendment:

**Determine Amendment Status**

* Classification logic checks for amendment-specific keywords in the Header/title or document body.

**Match Against Existing Records**  
 To confirm the original agreement, the system performs a **3-Point Match**:

| Match Criteria | Field Source | Requirement |
| ----- | ----- | ----- |
| **Header** | Contract document title | Must reference the original contract title |
| **User** | Signing entity / customer | Must match existing record |
| **Contract Effective Date** | Effective date of original agreement | Must align with original stored value |

→ Only when **all three fields** match an existing record is the amendment linked to that contract.

**If Match Found → Original Agreement Identified**

* Extract modified fields from amendment

* **Partial Overwrite Logic** applies:

  * Only fields explicitly changed in the amendment replace original values

  * All untouched values remain as-is

* Original dataset entry is updated **in place** with version tracking

**If No Match Found → Treat as New Contract**

* Extract all fields as if it were a master agreement

* Create a **new entry** in the dataset

* Status marked for internal review if classification uncertainty exists

#### **Decision Points**

* **Is this document classified as an amendment?**

* **Do Header, User, and Effective Date unanimously match an existing agreement?**

* **Which fields are explicitly updated and should be overwritten?**

---

### **Step 5: Validation & Quality Assurance**

**Performed by:** Pace Validation  
**Tools / Systems:** Field Consistency Rules, Date Validators  
**Input:** Extracted fields (new or updated)  
**Output:** Validated dataset record

**Process Summary**

* Dates are checked for chronological validity.

* Numeric values are verified for format and consistency.

* Required fields (e.g., effective date, header) must be present.

* Missing or ambiguous fields may be marked as “Not specified”.

If issues are detected:

* A re-extraction loop is initiated.

* If ambiguity persists, the record is flagged for manual review.

---

### **Step 6: Storage & Integration**

**Performed by:** Pace Dashboard  
**Tools:** Internal Databases (Postgres)  
**Input:** Validated contract record  
**Output:** Updated or newly inserted row in the **contract\_extraction\_dataset** table

**Process Summary**

* Newly extracted agreements are inserted.

* Amendments apply a partial update to the existing agreement row.

* All updates are audited via timestamps and internal tracking fields.

---

## **4\. Supporting Materials**

* **Field Dictionary / Extraction Rules**  
   Defines how each field (e.g., `contract_effective_date`, `product_skus`, `autorenewal`) is identified, formatted, and validated.

* **Amendment Handling Guide**  
   Rules for header matching and partial overwrite logic.

* **Data Model Reference**  
   `contract_extraction_dataset` schema, including all field names and types.

---

**5\. Data Requirements (Field Dictionary Overview)**

The system extracts and maintains the following fields as defined in the dataset schema:

* **Core Contract Fields:**  
   `total_contract_value`, `contract_effective_date`, `contract_start_date`, `contract_end_date`

* **Renewal & Subscription Fields:**  
   `autorenewal`, `contract_renewal_date`, `subscription_start_date`

* **Product & Pricing Fields:**  
   `products`, `product_rates`, `product_skus`

* **Geographic & Entity Fields:**  
   `stripe_legal_entity`, `signing_user_entity_country_geography`,  
   `direct_platform_territories`, `connect_territories`, `active_in_multiple_territories`

* **Incentives & Discounts:**  
   Types, amounts, start and end dates

* **Administrative Fields:**  
   `header`, `client`, plus system metadata

These fields are the authoritative outputs for dataset ingestion and serve as the basis for amendment comparison and updates.

| State | Entry Trigger | Exit Trigger | Example Scenario |
| ----- | ----- | ----- | ----- |
| **In Progress** | File received, parsing, extraction or amendment processing begins | Extraction \+ validation completed | Contract PDF parsing and OCR underway |
| **Needs Attention** | Mandatory fields missing, ambiguous extraction, amendment header mismatch | User resolves issue or provides correction | Incentive amount unclear; header cannot match original |
| **Void** | File unreadable, invalid PDF, duplicate, or non-contract document | N/A | Duplicate PDF or corrupted file |
| **Done** | All fields validated and stored successfully | N/A | Contract successfully extracted and saved |

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEMAAAA1CAYAAAAasVavAAAA7klEQVR4Xu2XwWkDQRTFXEoq200nKSEluBSX4lImm9uiPRj5YhBfoKtgYODN3G6WbT0PV1INAxU1DFTcj9uuYaSihoGK+3rwqK9hpKKGgYqamdITDFTUMFBSw0BFDQMV54F1UsNAxe/1xaO+hpGKGgYq6luxrZ9LpKKGgYoaBkpqGKioYaCkhoGKGgYq6ikdhmEYhuHj7Ot+2fSKGgYqahgoqWGgooaBkhoGKmoYqKh/tvv6vUQqahioqJkH1gkGKmoYKKlhoKKGgZIaBipqGKj4v4waRipqGKioYaCkhoGKGgZKahioqGGg4htT+gcMMxgON4n4oQAAAABJRU5ErkJggg==>