from google import genai

# automatically reads GOOGLE_API_KEY env variable
client = genai.Client()

def ask_llm(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=prompt
    )

    # Gemini returns candidates → text
    return response.text if response.text else "No response"
