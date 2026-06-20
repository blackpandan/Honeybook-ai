// ============================================================
// ZAPIER STEP 3 — "Code by Zapier" (JavaScript)
// ACTION: Follow-Up & Missing Action Alert
//
// USE CASE:
//   Run this as a SCHEDULED Zap (e.g. daily at 9am) to pull
//   the full missing-action report and send an email summary
//   or create tasks in your project management tool.
//
// INPUT FIELDS: none required (this is a scheduled pull)
//
// TRIGGER: Schedule by Zapier → Every Day
// ============================================================

const API_BASE_URL = inputData.apiUrl;  // ← CHANGE THIS
const API_KEY      = inputData.apiKey;     // ← CHANGE THIS

// ── Fetch the follow-up report ────────────────────────────────────────────────
let response;
try {
  response = await fetch(`${API_BASE_URL}/followup-report`, {
    method: "GET",
    headers: { "X-API-Key": API_KEY },
  });
} catch (err) {
  throw new Error(`Network error: ${err.message}`);
}

if (!response.ok) {
  const text = await response.text();
  throw new Error(`API error ${response.status}: ${text.slice(0, 200)}`);
}

const report = await response.json();
const items  = report.items || [];
const total  = report.total || 0;

// ── Build a formatted digest ───────────────────────────────────────────────────
function formatItem(item) {
  const actions = Array.isArray(item.missing_actions)
    ? item.missing_actions.map(a => `  • ${a}`).join("\n")
    : "  • Unknown";

  return [
    `Client: ${item.client_name || "Unknown"}`,
    `Email:  ${item.client_email || "N/A"}`,
    `Missing:\n${actions}`,
  ].join("\n");
}

const digestLines = items.map((item, i) =>
  `[${i + 1}] ${formatItem(item)}`
);

const emailBody = total === 0
  ? "All clients are up to date. No follow-ups needed today."
  : [
      `${total} client(s) need follow-up:\n`,
      ...digestLines,
      "\n---",
      ""
      // "Log in to review: https://your-api.com/docs#/Reports/followup_report_followup_report_get",
    ].join("\n\n");

// ── Build per-client output lines for Zapier's "line items" ──────────────────
// Zapier can loop over these to create one task/email per client.
const clientList = items.map(item => ({
  name:           item.client_name    || "Unknown",
  email:          item.client_email   || "",
  missing:        Array.isArray(item.missing_actions)
                  ? item.missing_actions.join(" | ")
                  : "",
  missing_count:  String(Array.isArray(item.missing_actions)
                  ? item.missing_actions.length : 0),
  project_id:     item.project_id     || "",
  created_at:     item.created_at     || "",
}));

// ── Output ────────────────────────────────────────────────────────────────────
output = {
  // Summary numbers
  total_needing_followup: String(total),
  has_followups:          total > 0 ? "true" : "false",

  // Full formatted email body — map this to Gmail / Outlook action
  email_subject: total === 0
    ? "HoneyBook Follow-Up Report — All Clear"
    : `HoneyBook Follow-Up Report — ${total} Client(s) Need Attention`,
  email_body: emailBody,

  // First client details (useful if Zapier needs flat fields)
  first_client_name:    clientList[0]?.name    || "",
  first_client_email:   clientList[0]?.email   || "",
  first_client_missing: clientList[0]?.missing || "",

  // JSON string of all clients — use with Zapier's Looping app
  all_clients_json: JSON.stringify(clientList),

  report_generated_at: new Date().toISOString(),
};
