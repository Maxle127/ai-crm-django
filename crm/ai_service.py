import os
from openai import OpenAI


def generate_follow_up(first_name, status, source, notes_text):
    try:
        api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key:
            return "OpenAI API key is not configured."

        client = OpenAI(api_key=api_key)

        prompt = f"""
Create a short professional follow-up message for this lead.

Lead data:
- Name: {first_name}
- Status: {status}
- Source: {source}

Notes from previous communication:
{notes_text if notes_text.strip() else "No notes provided."}

Rules:
1. You MUST use the notes as the main source of context.
2. If the notes are negative, cold, or show low interest, do NOT write an enthusiastic sales message.
3. Adapt the tone to the notes naturally.
4. Do NOT use placeholders like [Your Name], [Company], [Position], or [Contact Information].
5. Write only the final message text.
6. Keep it concise: 3-6 sentences.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a CRM assistant who writes realistic sales follow-up messages based primarily on the lead notes. Never ignore the notes. Never use placeholders."
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            temperature=0.4,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("OPENAI ERROR:", repr(e))
        return f"AI error: {e}"