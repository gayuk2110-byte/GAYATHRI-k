from google import genai
from google.genai import types

from .config import (
    DEMO_MODE,
    GEMINI_API_KEY,
    GEMINI_WORKOUT_MODEL,
)

_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def _demo_plan(username: str, goal: str, intensity: str) -> str:
    return f"""FITBUDDY DEMO PLAN FOR {username}

Goal: {goal}
Intensity: {intensity}

Day 1 – Full-body movement
• Warm-up: 5 minutes of easy movement
• Main: chair squats, wall push-ups, bird-dogs
• Cool-down: gentle stretching

Day 2 – Mobility
• Warm-up: 5 minutes
• Main: shoulder rolls, hip mobility, gentle walking
• Cool-down: relaxed breathing and stretching

Day 3 – Recovery
• Easy walk or other comfortable movement
• Gentle mobility for 10–15 minutes

Day 4 – Full-body movement
• Warm-up: 5 minutes
• Main: supported squats, wall push-ups, glute bridges
• Cool-down: gentle stretching

Day 5 – Mobility and balance
• Easy movement and balance practice near a stable support
• Finish with comfortable stretching

Day 6 – Light activity
• Choose a comfortable activity such as walking
• Keep the effort conversational

Day 7 – Rest and recovery
• Rest, hydration, sleep, and gentle mobility if comfortable

Safety note: This educational demo avoids calorie targets, weight-loss prescriptions,
and high-risk exercise instructions. Stop if something hurts and seek professional
advice for medical or exercise-specific concerns."""


def generate_workout_gemini(
    username: str, age: int, weight: float, goal: str, intensity: str
) -> str:
    if not GEMINI_API_KEY:
        if DEMO_MODE:
            return _demo_plan(username, goal, intensity)
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    prompt = f"""
Create a general wellness-oriented 7-day activity plan for an adult user.

User name: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Requested intensity: {intensity}

Safety constraints:
- This is an educational wellness application, not medical advice.
- Use only low-to-moderate, broadly accessible activities.
- Do not prescribe calorie restriction, fasting, supplements, weight-loss targets,
  body-shape targets, or extreme exercise.
- Do not diagnose medical conditions.
- Include warm-up, main activity, and cool-down/recovery guidance.
- Encourage rest, hydration, gradual progression, and stopping when pain/dizziness
  or unusual symptoms occur.
- Clearly say that people with medical conditions or exercise concerns should consult
  a qualified health professional.
- Return clean plain text with Day 1 through Day 7 headings.
"""

    response = _client.models.generate_content(
        model=GEMINI_WORKOUT_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.4,
            max_output_tokens=1800,
        ),
    )
    return response.text or "The AI did not return a plan."


def update_workout_plan(original_plan: str, feedback: str, goal: str, intensity: str) -> str:
    if not GEMINI_API_KEY:
        if DEMO_MODE:
            return (
                original_plan
                + "\n\nUPDATED AFTER FEEDBACK\n"
                + f"Feedback received: {feedback}\n"
                + "Adjustment: keep activities comfortable and reduce or increase "
                  "duration gradually rather than adding strenuous exercises."
            )
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    prompt = f"""
Revise this general wellness activity plan based on user feedback.

Goal: {goal}
Intensity: {intensity}

Original plan:
{original_plan}

Feedback:
{feedback}

Rules:
- Keep the plan low-to-moderate risk and general wellness focused.
- Do not add calorie restriction, fasting, supplements, weight-loss targets,
  extreme exercise, or unsafe challenges.
- Do not diagnose the user.
- Make practical adjustments such as shorter duration, more recovery, easier
  variations, or gradual progression.
- Return Day 1 through Day 7 in plain text.
"""

    response = _client.models.generate_content(
        model=GEMINI_WORKOUT_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.4,
            max_output_tokens=1800,
        ),
    )
    return response.text or "The AI did not return an updated plan."
