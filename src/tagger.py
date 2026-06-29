"""
The tagging pipeline. Takes article text, returns a validated result.
This file holds your two best interview talking points:
  1. Structured JSON output that feeds downstream systems
  2. Designing for the model being wrong (validation + fallback)
"""
from src.llm import call_llm_json

# Grounding: the model must pick from THIS list, not invent categories.
# In real CMS work this would come from your taxonomy/tag system.
ALLOWED_CATEGORIES = [
    "Technology", "Business", "Sports", "Politics",
    "Health", "Entertainment", "Science", "Other",
]

SYSTEM_PROMPT = (
    "You are an editorial assistant that classifies and summarizes articles. "
    "Always respond with valid JSON and nothing else."
)


def build_prompt(article_text: str) -> str:
    return f"""Analyze the article below and return a JSON object with exactly these keys:
- "summary": a 2-sentence summary
- "tags": an array of 3-5 short topic tags
- "category": ONE value chosen ONLY from this list: {ALLOWED_CATEGORIES}

Article:
\"\"\"
{article_text}
\"\"\"

Return only the JSON object."""


def tag_article(article_text: str) -> dict:
    """
    Returns a result dict. Always includes a 'status' field so downstream
    code knows whether to trust it or route to a human.
    """
    result = call_llm_json(build_prompt(article_text), SYSTEM_PROMPT)

    # Guardrail 1: the model returned something unparseable
    if result is None:
        return {"status": "needs_review", "reason": "invalid_json"}

    # Guardrail 2: required fields missing
    if not all(k in result for k in ("summary", "tags", "category")):
        return {"status": "needs_review", "reason": "missing_fields", "raw": result}

    # Guardrail 3: model invented a category outside our taxonomy
    if result["category"] not in ALLOWED_CATEGORIES:
        result["status"] = "needs_review"
        result["reason"] = "unknown_category"
        return result

    result["status"] = "ok"
    return result
