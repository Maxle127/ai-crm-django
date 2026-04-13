import os
from openai import OpenAI


def generate_follow_up(lead):
    try:
        api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key:
            return "OpenAI API key is not configured."

        client = OpenAI(api_key=api_key)

        prompt = f"""
        Write a short professional follow-up message for this lead.

        Name: {lead.first_name} {lead.last_name}
        Email: {lead.email}
        Phone: {lead.phone}
        Source: {lead.get_source_display()}
        Status: {lead.get_status_display()}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You write short professional sales follow-up messages."
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("OPENAI ERROR:", repr(e))
        return f"AI error: {e}"