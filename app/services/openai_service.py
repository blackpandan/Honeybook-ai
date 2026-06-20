import json
import openai
from app.core.config import settings
from app.models.schemas import ExtractedFields

client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

EXTRACTION_PROMPT = """
You are an AI assistant for a wedding/event planning business using HoneyBook.
Given raw client inquiry data, extract and return a JSON object with these exact keys:

{
  "client_name": "string or null",
  "budget": "string or null (e.g. '$5,000')",
  "event_date": "string or null (ISO format preferred)",
  "missing_tasks": ["list of strings — items that seem incomplete or need follow-up"],
  "followup_status": "one of: needs_quote | awaiting_contract | awaiting_payment | ready | unknown"
}

Return ONLY valid JSON. No explanation, no markdown, no extra text.
"""

SUMMARY_PROMPT = """
You are a concise business assistant for an event planning company.
Given this client inquiry data, write:
1. A 2-3 sentence SUMMARY of the client and their needs.
2. A short, professional FOLLOW-UP MESSAGE (3-5 sentences) to send to the client.

Respond ONLY as JSON:
{
  "summary": "...",
  "followup": "..."
}

No markdown, no extra text.
"""


async def extract_fields(raw_data: dict) -> ExtractedFields:
    """Call OpenAI to extract structured fields from raw HoneyBook payload."""
    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": EXTRACTION_PROMPT},
            {"role": "user", "content": json.dumps(raw_data, default=str)},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content
    data = json.loads(content)
    return ExtractedFields(**data)


async def generate_summary_and_followup(raw_data: dict, extracted: ExtractedFields) -> dict:
    """Call OpenAI to produce a human-readable summary + follow-up message."""
    combined = {**raw_data, "extracted": extracted.model_dump()}
    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SUMMARY_PROMPT},
            {"role": "user", "content": json.dumps(combined, default=str)},
        ],
        temperature=0.5,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content
    return json.loads(content)
