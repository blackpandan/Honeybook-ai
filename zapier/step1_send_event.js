// ============================================================
// ZAPIER STEP 1 — "Code by Zapier" (JavaScript)
// ACTION: Send HoneyBook event to your backend API
//
// INPUT FIELDS TO MAP IN ZAPIER (from HoneyBook trigger):
//   project_url
//   project_name
//   project_date
//   project_time
//   project_end_date
//   project_end_time
//   project_location
//   project_type
//   workspace_id
//   project_timezone
//   project_id
//   first_client_email
//   first_client_first_name
//   first_client_last_name
//   first_client_phone_number
//   first_client_address
//   second_client_email
//   second_client_first_name
//   second_client_last_name
//   second_client_phone_number
//   second_client_address
// ============================================================

const API_BASE_URL = inputData.apiUrl;   // ← CHANGE THIS to your AWS URL
const API_KEY      = inputData.apiKey;      // ← CHANGE THIS to your API_KEY from .env

const clean = (value) => {
  if (value === undefined || value === null) return "";
  return String(value).trim();
};

const buildFullName = (firstName, lastName) => {
  return [clean(firstName), clean(lastName)].filter(Boolean).join(" ");
};

// ── Build the payload ─────────────────────────────────────────────────────────
const payload = {
  client_id: clean(inputData.workspace_id) || clean(inputData.project_id) || null,
  project_id: clean(inputData.project_id) || clean(inputData.workspace_id) || null,
  name: buildFullName(inputData.first_client_first_name, inputData.first_client_last_name) ||
    clean(inputData.project_name) ||
    null,
  email: clean(inputData.first_client_email) || clean(inputData.second_client_email) || null,
  budget: null,
  event_date: clean(inputData.project_date) || null,

  // raw = everything from HoneyBook, so the AI has full context
  raw: {
    project_url: clean(inputData.project_url),
    project_name: clean(inputData.project_name),
    project_date: clean(inputData.project_date),
    project_time: clean(inputData.project_time),
    project_end_date: clean(inputData.project_end_date),
    project_end_time: clean(inputData.project_end_time),
    project_location: clean(inputData.project_location),
    project_type: clean(inputData.project_type),
    workspace_id: clean(inputData.workspace_id),
    project_timezone: clean(inputData.project_timezone),
    project_id: clean(inputData.project_id),
    first_client: {
      email: clean(inputData.first_client_email),
      first_name: clean(inputData.first_client_first_name),
      last_name: clean(inputData.first_client_last_name),
      phone_number: clean(inputData.first_client_phone_number),
      address: clean(inputData.first_client_address),
    },
    second_client: {
      email: clean(inputData.second_client_email),
      first_name: clean(inputData.second_client_first_name),
      last_name: clean(inputData.second_client_last_name),
      phone_number: clean(inputData.second_client_phone_number),
      address: clean(inputData.second_client_address),
    },
    submitted_at: new Date().toISOString(),
  }
};

// ── POST to your backend ──────────────────────────────────────────────────────
let response;
try {
  response = await fetch(`${API_BASE_URL}/hb-event`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY,
    },
    body: JSON.stringify(payload),
  });
} catch (networkErr) {
  throw new Error(`Network error reaching API: ${networkErr.message}`);
}

// ── Parse response ─────────────────────────────────────────────────────────────
const responseText = await response.text();

if (!response.ok) {
  throw new Error(
    `API returned ${response.status}: ${responseText.slice(0, 300)}`
  );
}

let data;
try {
  data = JSON.parse(responseText);
} catch (parseErr) {
  throw new Error(`Could not parse API response as JSON: ${responseText.slice(0, 200)}`);
}

// ── Output for later Zap steps ────────────────────────────────────────────────
output = {
  project_id: data.project_id || payload.project_id || "",
  status: data.status || "",
  message: data.message || "",

  project_name: clean(inputData.project_name),
  project_date: clean(inputData.project_date),
  first_client_name: buildFullName(
    inputData.first_client_first_name,
    inputData.first_client_last_name
  ),
  first_client_email: clean(inputData.first_client_email),
  second_client_name: buildFullName(
    inputData.second_client_first_name,
    inputData.second_client_last_name
  ),
  second_client_email: clean(inputData.second_client_email),
  raw_json: JSON.stringify(payload.raw),
};
