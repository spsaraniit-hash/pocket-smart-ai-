import json
import httpx

from .config import GEMINI_API_KEY, GEMINI_MODEL
from .utils import demo_recommendations


def build_prompt(planner: str, budget: float, details: dict) -> str:
    return f"""
You are PocketSmart AI, a budget planning assistant.

Planner: {planner}
Budget: ₹{budget:,.2f}
User details:
{json.dumps(details, indent=2, ensure_ascii=False)}

Create practical, budget-aware recommendations. Do not claim live product availability,
live prices, stock status, discounts, or vendor APIs unless the user has provided them.
Treat platform names as example marketplaces/services.

Return ONLY valid JSON in this exact shape:
{{
  "allocation": {{"category": number}},
  "recommendations": [
    {{
      "category": "string",
      "suggestion": "string",
      "estimated_price": "string",
      "platform": "string",
      "reason": "string"
    }}
  ],
  "tips": ["string", "string", "string"]
}}
Keep the recommendations concise and useful.
"""


async def generate_recommendations(planner: str, budget: float, details: dict):
    if not GEMINI_API_KEY:
        items, tips, allocation = demo_recommendations(planner, budget, details)
        recommendations = [
            {
                "category": x[0],
                "suggestion": x[1],
                "estimated_price": x[2],
                "platform": x[3],
                "reason": x[4],
            }
            for x in items
        ]
        return {
            "allocation": allocation,
            "recommendations": recommendations,
            "tips": tips,
            "mode": "demo",
        }

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    )

    payload = {
        "contents": [{"parts": [{"text": build_prompt(planner, budget, details)}]}],
        "generationConfig": {
            "temperature": 0.4,
            "responseMimeType": "application/json",
        },
    }

    try:
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()

        text = data["candidates"][0]["content"]["parts"][0]["text"]
        parsed = json.loads(text)
        parsed["mode"] = "gemini"
        return parsed

    except Exception:
        items, tips, allocation = demo_recommendations(planner, budget, details)
        recommendations = [
            {
                "category": x[0],
                "suggestion": x[1],
                "estimated_price": x[2],
                "platform": x[3],
                "reason": x[4],
            }
            for x in items
        ]
        return {
            "allocation": allocation,
            "recommendations": recommendations,
            "tips": tips + ["Gemini was unavailable, so demo recommendations were displayed."],
            "mode": "fallback",
        }
