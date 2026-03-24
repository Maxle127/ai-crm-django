from openai import OpenAI 
client = OpenAI()

def generate_folow_up(first_name, status, source, notes):
    prompt = f"""
    Generate a short professional follow-up message for a sales lead.
    Lead name: {first_name}
    Status: {status}
    Source: {source}
    Notes: {notes}
    Write a polite message  in English, 3-5 sentences, friendly but professional
    """
    response = client.responses.create(
        model = "gpt-5-mini",
        input=prompt,
    )
    return(response.output_text)
 