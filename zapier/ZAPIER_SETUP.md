# Zapier Setup Guide — HoneyBook AI Workflow

---

## ZAP 1 — Main Pipeline (Triggered by New HoneyBook Project)

```
TRIGGER:   HoneyBook → New Project / New Inquiry
STEP 1:    Code by Zapier → step1_send_event.js
STEP 2:    Code by Zapier → step2_fetch_result.js
STEP 3:    Filter by Zapier → only continue if Step 2 says ready
STEP 4:    Code by Zapier → step4_format_honeybook_output.js
STEP 5:    HoneyBook → Create Note  (paste internalNote)
STEP 6:    HoneyBook → Update Project  (paste smart fields)
STEP 7:    Gmail / Outlook → Send Email  (optional — paste email_body)
```

---

## ZAP 2 — Daily Follow-Up Report (Scheduled)

```
TRIGGER:   Schedule by Zapier → Every Day at 9:00 AM
STEP 1:    Code by Zapier → step3_followup_report.js
STEP 2:    Gmail → Send Email
              To:      your@email.com
              Subject: {{email_subject}} from Step 1
              Body:    {{email_body}} from Step 1
```

---

## HOW TO ADD CODE IN ZAPIER

1. In your Zap, click **+** to add an action
2. Search for **"Code by Zapier"**
3. Choose **Run Javascript**
4. In **Input Data**, add these fields and map from your trigger:

```
project_url                → HoneyBook: Project URL
project_name               → HoneyBook: Project Name
project_date               → HoneyBook: Project Date
project_time               → HoneyBook: Project Time
project_end_date           → HoneyBook: Project End Date
project_end_time           → HoneyBook: Project End Time
project_location           → HoneyBook: Project Location
project_type               → HoneyBook: Project Type
workspace_id               → HoneyBook: Workspace ID
project_timezone           → HoneyBook: Project Timezone
project_id                 → HoneyBook: Project ID
first_client_email         → HoneyBook: First Client Email
first_client_first_name    → HoneyBook: First Client First Name
first_client_last_name     → HoneyBook: First Client Last Name
first_client_phone_number  → HoneyBook: First Client Phone Number
first_client_address       → HoneyBook: First Client Address
second_client_email        → HoneyBook: Second Client Email
second_client_first_name   → HoneyBook: Second Client First Name
second_client_last_name    → HoneyBook: Second Client Last Name
second_client_phone_number → HoneyBook: Second Client Phone Number
second_client_address      → HoneyBook: Second Client Address
```

This step uses the first client for the top-level `name` and `email`, then sends both clients inside `raw`.

5. Paste the full contents of the `.js` file into the **Code** box
6. Update these two lines at the top of EVERY script:

```javascript
const API_BASE_URL = "https://your-api.com";   // ← Your AWS URL
const API_KEY      = "your-api-key-here";      // ← Your API_KEY from .env
```

7. Click **Test Step** — you should see output keys appear

---

## FILTER BETWEEN STEP 2 AND STEP 4

Add **Filter by Zapier** after Step 2.

Condition:

```
should_continue  Exactly Matches  true
```

This makes the Zap return safely when OpenAI is still processing, without failing the run.

---

## MAPPING STEP 2 OUTPUT → STEP 4 INPUT

In Step 4 (format output), map these Input Data fields:

```
summary                → Step 2: summary
followup_message       → Step 2: followup_message
missing_tasks          → Step 2: missing_tasks
missing_tasks_count    → Step 2: missing_tasks_count
extracted_client_name  → Step 2: extracted_client_name
extracted_budget       → Step 2: extracted_budget
extracted_event_date   → Step 2: extracted_event_date
extracted_followup_status → Step 2: extracted_followup_status
```

---

## ADDING A FILTER (ONLY SEND EMAIL IF MISSING ACTIONS EXIST)

Between the format step and your email step:

1. Add **Filter by Zapier**
2. Condition: `has_missing_tasks` **Exactly Matches** `true`
3. This ensures follow-up emails only go out when something is actually missing

---

## HONEYBOOK "CREATE NOTE" MAPPING

In the HoneyBook → Create Note action:
- **Project:** map the HoneyBook project ID from trigger
- **Note:** map `honeybook_note` from your format step

## HONEYBOOK "UPDATE PROJECT" MAPPING

Map `field_*` outputs from the format step to your HoneyBook custom fields.
The exact field names depend on what you've set up in HoneyBook.

---

## TESTING WITHOUT LIVE HONEYBOOK DATA

Use Zapier's **"Test trigger"** to grab a real sample from HoneyBook,
or use the provided script locally:

```bash
python scripts/send_test_event.py --url https://your-api.com --key your-api-key
```
