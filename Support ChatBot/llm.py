import openai
from config import OPENAI_API_KEY  # Import API key

def generate_response(query, retrieved_text):
    client = openai.OpenAI(api_key=OPENAI_API_KEY)  # Pass API key

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Context: {retrieved_text}\n\nQuestion: {query}"}
        ]
    )

    return response.choices[0].message.content
