// ============================================================
// ZAPIER STEP 2 — "Code by Zapier" (JavaScript)
// ACTION: Fetch AI result once and return a safe pending state if not ready yet
//
// INPUT FIELDS TO MAP IN ZAPIER:
//   project_id  → map from Step 1's "project_id" output
// ============================================================

const API_BASE_URL = inputData.apiUrl;   // ← CHANGE THIS to your AWS URL
const API_KEY      = inputData.apiKey;      // ← CHANGE THIS to your API_KEY from .env

const projectId = inputData.project_id;

if (!projectId) {
  throw new Error("project_id is required. Map it from Step 1 output.");
}

async function fetchResult(id) {
  const res = await fetch(
    `${API_BASE_URL}/hb-result?project_id=${encodeURIComponent(id)}`,
    {
      method: "GET",
      headers: { "X-API-Key": API_KEY },
    }
  );

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API returned ${res.status}: ${text.slice(0, 200)}`);
  }

  return res.json();
}

let data;
try {
  data = await fetchResult(projectId);
} catch (err) {
  throw err;
}

const fields = data.fields || {};
const missingTasks = Array.isArray(fields.missing_tasks) ? fields.missing_tasks : [];
const isReady = data.status === "processed";

output = {
  project_id: data.project_id || "",
  status: data.status || "",
  summary: data.summary || "",
  followup_message: data.followup || "",

  extracted_client_name: fields.client_name || "",
  extracted_budget: fields.budget || "",
  extracted_event_date: fields.event_date || "",
  extracted_followup_status: fields.followup_status || "",
  missing_tasks: missingTasks.join(" | "),
  missing_tasks_count: String(missingTasks.length),
  has_missing_tasks: missingTasks.length > 0 ? "true" : "false",

  fields_json: JSON.stringify(fields),
  updated_at: data.updated_at || "",
  is_ready: isReady ? "true" : "false",
  should_continue: isReady ? "true" : "false",
};
