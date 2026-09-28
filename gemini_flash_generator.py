from google import genai
from google.genai import types

from .config import DEMO_MODE, GEMINI_API_KEY, GEMINI_TIP_MODEL

_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def generate_nutrition_tip_with_flash(goal: str) -> str:
    if not GEMINI_API_KEY:
        if DEMO_MODE:
            return (
                "Wellness tip: Keep meals varied and regular, drink water according "
                "to thirst, and include a variety of fruits/vegetables, grains and "
                "protein foods. Avoid extreme diets. For personal nutrition advice, "
                "talk with a qualified health professional."
            )
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    prompt = f"""
Give one short, general wellness nutrition or recovery tip for the goal:
{goal}

Do not provide calorie targets, restrictive diets, fasting instructions, supplements,
or weight-loss prescriptions. Keep it practical and suitable for a general audience.
End with a brief note that personal nutrition needs should be discussed with a
qualified health professional.
"""

    response = _client.models.generate_content(
        model=GEMINI_TIP_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=300,
        ),
    )
    return response.text or "Keep meals varied, stay hydrated, and prioritize recovery."
