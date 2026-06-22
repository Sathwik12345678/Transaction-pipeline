import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_summary(prompt):

    try:

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.3,
            max_tokens=300
        )

        return chat_completion.choices[0].message.content

    except Exception as e:

        print("Groq Error:", str(e))

        return (
            "Unable to generate AI summary. "
            f"Error: {str(e)}"
        )