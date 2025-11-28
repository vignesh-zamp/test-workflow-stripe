# SOP IMPL - Stripe + Contract Extraction

AST team to populate the following template and hand-off to FDEs so they can effectively and quickly execute delivery. This information is already provided by AST teams to FDEs in Slack customer squad groups and daily syncs during delivery. 

The aim of this template and hand-off process is to ensure we 

1. Increase customer delivery speed without a lot of back & forth and coordination cost
2. Ensure delivery SLAs are not affected even if FDE, SE or ASM switch
3. Centralised documentation of business context and requirements of all processes as we scale to 1000s of processes

Reference images for information available for guidance. 

## SOP document attachment - AST

*(Please upload SOP document here)*

[SOP DOCUMENT](https://docs.google.com/document/d/1gV3bKvwtYGHveDtAacCkoeS-bG6G_bJWQBgRLxG3zkU/edit?usp=sharing)

## High-level Workflow Chart - AST

*(Please input SOP document to Claude and attach output xml file or flowchart diagram)*

[Screenshot 2025-11-26 at 01.07.03.png](SOP%20IMPL%20-%20Stripe%20+%20Contract%20Extraction/Screenshot_2025-11-26_at_01.07.03.png)

## Prompt flow chart - AST (critical)

Each step in the below flow to be sequential. If to be executed parallely, mention 2a, 2b, 2c..

| **Step #** | **Prompt name** | **Called by** | **Objective** | **Input Variables : Type** | **Output Variables : Type** |
| --- | --- | --- | --- | --- | --- |
| 1 |  | Code/Prompt |  |  |  |
| 2 |  | Code/Prompt |  |  |  |

## External System Dependencies *(if applicable)* - AST

*(Please tick when done and whichever applicable)*

- [ ]  Option 1: API credentials and documentation - add details below

- [ ]  If not, feasibility check with FDE on reverse engineering APIs - add comments below

- [ ]  If not, feasibility check with product / eng on workarounds / browser agent - add comments below

## Access to existing Pace organization - AST

- [x]  If organization exists, please add FDE to existing org on Pace dashboard
- [ ]  NA - new organization

## New Org and Process Name - AST

- Organisation name = Stripe
- Process name = Contract Extraction

## What data needs to be captured - AST (critical)

*(What exhaustive data - tables and columns need to be captured by Pace for the process to run effectively. This includes input source, intermediate processed and output data)*

Where this goes: Check [here](https://www.notion.so/SOP-IMPL-Stripe-Contract-Extraction-2b6edc94e67f80c2beabe0f3b04c92aa?pvs=21) and [here](https://www.notion.so/SOP-IMPL-Stripe-Contract-Extraction-2b6edc94e67f80c2beabe0f3b04c92aa?pvs=21)

### Dataset Details:

| {Table name} | {column 1} | {column 2} | {column 3} | {column 4} | {column 5} | {column 6} | {column 7} | {column 8} | {column 9} |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_extraction_dataset | id (text) | activity_run_id (text) | status (text) | file_path (text) | total_contract_value (integer) | contract_effective_date (date) | contract_renewal_date (date) | contract_start_date (date) | contract_end_date (date) | notice_period (text) | products (text) | product_rates (text) | product_skus (text) | autorenewal (text) | subscription_start_date (date) | stripe_legal_entity (text) | signing_user_entity_country_geography (text) | legal_entity_modification (text) | direct_platform_territories (text) | connect_territories (text) | active_in_multiple_territories (text) | incentives_credits_discounts_rebates_type (text) | incentives_credits_discounts_rebates_amount (text) | incentives_credits_discounts_rebates_start_date (date) | incentives_credits_discounts_rebates_end_date (date) | header (text) | client (text) | _zamp_field_annotations (text) | _zamp_created_at (timestamp) | _zamp_updated_at (timestamp) | _zamp_is_deleted (boolean) |
- Decide whether the table should be hidden or visible on dashboard
1. contract_extraction_dataset
    - Visible

- Which fields or columns above should be hidden on the dashboard (but needed for Pace)
    - activity_run_id
    - status
    - file_path
    - _zamp_field_annotations
    - _zamp_created_at
    - _zamp_updated_at
    - _zamp_is_deleted

- Which fields or columns above are mandatory to be captured and which are optional
    - client
    - header
    - total_contract_value
    - contract_effective_date
    - contract_start_date
    - contract_end_date

## Field Recognition Logic & Descriptions

### **1. Contract Metadata**

**contract_effective_date**

- **Description**: The date when the contract becomes legally binding and enforceable
- **Recognition Logic**: Look for "Effective Date" label followed by signature date or explicit date statement

**contract_start_date**

- **Description**: The date when services under the contract begin
- **Recognition Logic**: Often same as effective date unless explicitly stated otherwise; look for "Services commence on" or similar language

**contract_end_date**

- **Description**: The date when the initial contract term expires
- **Recognition Logic**: Calculate from effective_date + initial_term; look for "expires on" or explicit end date

**header**

- **Description**: The official title/name of the contract document
- **Recognition Logic**: Usually found at top of document, often in larger font or bold

**client**

- **Description**: The customer/user entity entering into the agreement
- **Recognition Logic**: Look for "User" field in header table or signature block; may list multiple entities

---

### **2. Commercial Values**

**total_contract_value**

- **Description**: The total monetary value of the contract over its lifetime
- **Recognition Logic**: Usually not explicitly stated in usage-based contracts; would need to be calculated from volume commitments × rates

**product_rates**

- **Description**: The pricing/fees charged for each service or product
- **Recognition Logic**: Found in fee tables; look for percentage rates and fixed fees per transaction/service

**product_skus**

- **Description**: Specific product/service identifiers or categories
- **Recognition Logic**: Look for service type names in fee tables and section headers

**products**

- **Description**: High-level product categories being offered
- **Recognition Logic**: Found in section headers and "Services" definitions

**autorenewal**

- **Description**: Whether the contract automatically renews at term end
- **Recognition Logic**: Look in "Term" section for language about "automatically renew"

---

### **3. Territory Fields**

**direct_platform_territories**

- **Description**: Geographic locations where the direct/platform services are provided
- **Recognition Logic**: Look for "Territory" field in header table listing countries/regions

**connect_territories**

- **Description**: Territories where Stripe Connect (platform) services are available
- **Recognition Logic**: May be separate from direct territories; look for Connect-specific territory lists

**active_in_multiple_territories**

- **Description**: Boolean indicating if services span multiple countries/regions
- **Recognition Logic**: Check if territory list contains more than one country/region

---

### **4. Incentive Structures**

**incentives_credits_discounts_rebates_type**

- **Description**: The category/nature of financial incentives provided
- **Recognition Logic**: Look for sections mentioning "discounts," "credits," "rebates," "incentives," volume-based pricing tiers, or promotional terms

**incentives_credits_discounts_rebates_amount**

- **Description**: The monetary value or percentage of the incentive
- **Recognition Logic**: Calculate difference between tier rates or look for explicit credit amounts

**incentives_credits_discounts_rebates_start_date**

- **Description**: When the incentive becomes active
- **Recognition Logic**: Look for effective dates of promotional tiers or explicit incentive start dates

**incentives_credits_discounts_rebates_end_date**

- **Description**: When the incentive expires
- **Recognition Logic**: Look for expiration dates, tier change dates, or contract end dates

---

### **5. Legal Terms**

**notice_period**

- **Description**: Required advance notice for termination or non-renewal
- **Recognition Logic**: Look in "Term" section for "notice of non-renewal at least X days"

**stripe_legal_entity**

- **Description**: The specific Stripe corporate entity that is the contracting party
- **Recognition Logic**: Look for "Stripe entity" in header or "Stripe" definition section

**signing_user_entity_country_geography**

- **Description**: The country/region where the customer entity is located/incorporated
- **Recognition Logic**: Extract from user entity description, look for incorporation language or address

**legal_entity_modification**

- **Description**: Whether there are changes to legal entity structure or rights during the contract
- **Recognition Logic**: Look for amendments, entity changes, or modification clauses

---

### **6. Subscription Details**

**subscription_start_date**

- **Description**: When the ongoing subscription/service relationship begins
- **Recognition Logic**: Usually same as contract start date for service agreements

**contract_renewal_date**

- **Description**: The date when the contract is up for renewal
- **Recognition Logic**: Calculate from start_date + initial_term; look for renewal language

---

## Additional Extraction Logic Guidelines

### **General Recognition Patterns:**

1. **Date Formats**: Watch for various formats (April 30, 2024 / 30/04/2024 / 2024-04-30)
2. **Currency Indicators**: Fees will have currency codes (USD, CAD, AUD, GBP, EUR, etc.)
3. **Percentage vs Fixed Fees**: Percentages have "%" symbol; fixed fees have currency codes
4. **Tier Structures**: Look for "Fee Tier X" or volume brackets like "USD 0 to 5,000,000"
5. **Entity Lists**: Multiple entities often listed with "By:" signature blocks or in comma-separated lists
6. **Section Headers**: Key terms often in dedicated sections (Term, Definitions, Fees, Territory)
7. **Tables**: Commercial terms typically in tabular format with clear column headers
8. **Signature Blocks**: Effective dates, parties, and authorized signatories appear here
9. **DocuSign Elements**: Electronic signature systems add envelope IDs and signature dates
10. **Supersession Clauses**: Look for language about replacing previous agreements

### **Complex Field Relationships:**

- **Volume Tiers → Incentives**: Lower rates at higher volumes = implicit volume discounts
- **Multiple Territories → FX Fees**: Cross-border transactions trigger foreign exchange fees
- **Contract Type → Fee Structure**: Platform agreements have Connect fees; Direct agreements may not
- **Initial Term + Auto-renewal → Total Duration**: Indefinite unless terminated with proper notice

<aside>
🛑

Check-point: Once the FDE completes datasets and process creation, FDE should provide the input and expected output (golden-dataset) schema for AST team to create and run evals on Langfuse via Windmill Scripts ([Reference](https://www.notion.so/Building-AI-Agents-From-Process-to-Prompt-23bedc94e67f804ba452d4d0b06089fe?pvs=21) and [Reference Video](https://app.avoma.com/meetings/4fddee2f-0bfc-4722-9d87-1e3de0ac6ca7)) 

</aside>

## What gets shown on dashboard - AST (critical)

### Process Activity Run States

*(For the process, what are exhaustive states that runs will go through - for eg: Needs Attention, In-Progress, Done, Void)*

Where this goes: Check [here](https://www.notion.so/SOP-IMPL-Stripe-Contract-Extraction-2b6edc94e67f80c2beabe0f3b04c92aa?pvs=21)

- [x]  In progress
- [x]  Needs Attention
- [x]  Completed
- [x]  Void

### Process Activity Run State Change logic: check-in

- [x]  Quick check-in: Ensure the logic of when an item moves from one state to the other is mece detailed out in SOP document for workflow logic to be comprehensive (For eg: when all is an item supposed to be in progress, when all is an item supposed to be Void, when all is an item supposed to be in Needs Attention bucket, when all is an item supposed to be in Done bucket)

### Process View Table

*(On the process page, what columns should the customer see. This will be a sub-set of the [Datasets](https://www.notion.so/SOP-IMPL-Stripe-Contract-Extraction-2b6edc94e67f80c2beabe0f3b04c92aa?pvs=21) captured above. This will be 1 table only. Add as many columns as required to show to the customer)*

Where this goes: Check [here](https://www.notion.so/SOP-IMPL-Stripe-Contract-Extraction-2b6edc94e67f80c2beabe0f3b04c92aa?pvs=21)

| Process View Datasets | Status | {column 2} | {column 3} | … |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| contract_extraction_dataset (Process View) | total_contract_value (integer) | contract_effective_date (date) | contract_renewal_date (date) | contract_start_date (date) | contract_end_date (date) | notice_period (text) | products (text) | product_rates (text) | product_skus (text) |

### Process View run headers

*(When you click on a single run, what should the title and value of each run be named)*

Where this goes: Check [here](https://www.notion.so/SOP-IMPL-Stripe-Contract-Extraction-2b6edc94e67f80c2beabe0f3b04c92aa?pvs=21)

- Header Name = Client
- Header Value = {client}

### Process View Key Details

*(When you click on a single run, what dataset values do you want the customer to see specific to the run. You can have multiple tables added here)*

Where this goes: Check [here](https://www.notion.so/SOP-IMPL-Stripe-Contract-Extraction-2b6edc94e67f80c2beabe0f3b04c92aa?pvs=21)

### **Key Details Table 1:**

- Client: {client}
- Total Contract Value: {total_contract_value}
- Contract Effective Date: {contract_effective_date}
- Contract Start Date: {contract_start_date}
- Contract End Date: {contract_end_date}

### Process View Artefacts

*(When you click on a single run, what artefacts do you want the customer to see.* The same artefacts are referenced with logs*)*

Where this goes: Check [here](https://www.notion.so/SOP-IMPL-Stripe-Contract-Extraction-2b6edc94e67f80c2beabe0f3b04c92aa?pvs=21)

| Artefact of | Type (pdf, email, pdf-datasets, link etc.) | Artefact Display Name |
| --- | --- | --- |
| Agreement PDF | pdf | Contract Agreement |
| Amendment PDF | pdf | Contract Amendment |
| Parsed JSON | dataset | Extracted JSON |
| Extraction Log | dataset | Extraction Log |
| Validation Report | dataset | Validation Summary |

### Process View Log Groups Master <> Activity Run State

*(When you click on a single run, what log group or activity progress should be shown to the customer when a) the step begins b) when it is completed c) when it fails due to an error d) when it needs HITL, what log groups need to have See Reasoning steps by CoT agent, what artefacts need to be referenced for each log group. Typically each log group or activity is a job-to-be-done. If a particular activity requires Needs Attention (or HITL) by user, what actions should Pace ask the user to complete - MCQ / field entry etc. and whether communication should happen on Slack or dashboard only. Please detail exhaustive log group steps here and what activity state change they represent corresponding to the specific log status)*

Check [here](https://www.notion.so/SOP-IMPL-Stripe-Contract-Extraction-2b6edc94e67f80c2beabe0f3b04c92aa?pvs=21)

| Sr # | Log Group Overview | Initiated Message | Success Message | Failed Message | Needs Attention Message | Activity Run State Mapping | Reasoning Message | Artefacts / CTAs | User Action | HITL? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | File Ingestion | “Receiving contract PDF.” | “PDF successfully ingested.” | “Invalid or unreadable file.” | “Unsupported file format – needs user review.” | In Progress → Void / Needs Attention | “Checking PDF metadata.” | Uploaded PDF | Upload correct file | Dashboard |
| 2 | Parsing & Classification | “Parsing contract text.” | “Parsing complete.” | “Unable to extract text.” | “OCR unclear – needs clarification.” | In Progress → Needs Attention | “Detecting master vs amendment.” | Parsed JSON | Confirm document type | Dashboard |
| 3 | Field Extraction | “Extracting contract fields.” | “Fields extracted.” | “Missing key fields.” | “Ambiguous fields detected.” | In Progress → Needs Attention | “Analyzing dates, values, products.” | Extraction Log | Supply missing data | Dashboard |
| 4 | Amendment Processing | “Checking for amendment match.” | “Amendment applied.” | “Could not locate original contract.” | “Header mismatch – requires input.” | In Progress → Needs Attention or Done | “Matching header to existing dataset.” | Amendment PDF | Select master contract | Slack / Dashboard |
| 5 | Validation | “Validating extracted fields.” | “Validation successful.” | “Validation failed.” | “Manual validation required.” | In Progress → Needs Attention or Done | “Checking chronology + mandatory fields.” | Validation Report | Approve or edit | Dashboard |
| 6 | Storage | “Saving contract record.” | “Contract saved.” | “Database save failed.” | “Storage error – user review needed.” | In Progress → Done or Needs Attention | “Finalizing dataset update.” | Final Dataset Entry | Retry save | Dashboard |

## Validation Logic

**Mandatory Fields Check**

Is anything *required* missing?

For example:

- client
- header
- total_contract_value
- contract_effective_date
- contract_start_date
- contract_end_date

If any of these are missing → we don’t proceed → **Needs Attention**.

**Basic Logical Checks**

These prevent garbage data from entering the dataset.

Examples:

- contract_start_date must be ≤ contract_end_date
- contract_effective_date must be a real date
- total_contract_value must be a number
- no invalid strings like “$—” or “TBD” where integers are expected

This is extremely lightweight, not a heavy validation pipeline.

**Amendment Integrity Check**

When applying partial overwrite:

- Ensure updated fields don’t contradict chronology
- Ensure amendment does not break required fields
- Ensure amendment header actually matches the original contract

This protects the master dataset.

## Email trigger set-up hygiene - AST

*(If email is the primary trigger for the process, please coordinate with @Yashikha Jain to set-up emails for dev and prod environments separately)*

- [ ]  Done

---

## Change Log - FDE / AST

*(FDE / AST to list down all changes that’s happened to track scope creep)*

| Change Topic | Change Description | Time-stamp |
| --- | --- | --- |
|  |  |  |
|  |  |  |

---

## User, Org, Dataset, Process IDs - FDE

*(FDEs to enter all relevant ids for the org, datasets and process which need frequent referencing)*

| Type | Description | ID |
| --- | --- | --- |
|  |  |  |
|  |  |  |

---

## SOP IMPL Reference Images

- Data tables
    
    ![image.png](SOP%20IMPL%20-%20Stripe%20+%20Contract%20Extraction/image.png)
    
- Data table columns
    
    ![image.png](SOP%20IMPL%20-%20Stripe%20+%20Contract%20Extraction/image%201.png)
    
- Process State Groups
    
    ![image.png](SOP%20IMPL%20-%20Stripe%20+%20Contract%20Extraction/image%202.png)
    
- Process View Table
    
    ![image.png](SOP%20IMPL%20-%20Stripe%20+%20Contract%20Extraction/image%203.png)
    
    ![image.png](SOP%20IMPL%20-%20Stripe%20+%20Contract%20Extraction/image%204.png)
    
- Process View run-wise Header Name and Value Details
    
    ![image.png](SOP%20IMPL%20-%20Stripe%20+%20Contract%20Extraction/image%205.png)
    
- Process View run Key Details
    
    ![image.png](SOP%20IMPL%20-%20Stripe%20+%20Contract%20Extraction/image%206.png)
    
- Process View Artefacts
    
    ![image.png](SOP%20IMPL%20-%20Stripe%20+%20Contract%20Extraction/image%207.png)
    
    ![image.png](SOP%20IMPL%20-%20Stripe%20+%20Contract%20Extraction/image%208.png)
    
    ![image.png](SOP%20IMPL%20-%20Stripe%20+%20Contract%20Extraction/image%209.png)
    
    ![image.png](SOP%20IMPL%20-%20Stripe%20+%20Contract%20Extraction/image%2010.png)
    
- Process View Logs - Logs Master
    
    
    ![image.png](SOP%20IMPL%20-%20Stripe%20+%20Contract%20Extraction/image%2011.png)
    
    ![image.png](SOP%20IMPL%20-%20Stripe%20+%20Contract%20Extraction/image%2012.png)
    
    ![image.png](SOP%20IMPL%20-%20Stripe%20+%20Contract%20Extraction/image%2013.png)
    
    ![image.png](SOP%20IMPL%20-%20Stripe%20+%20Contract%20Extraction/image%2014.png)