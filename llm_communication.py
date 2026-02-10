from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not found in .env")
client = OpenAI()

def get_normal_response_openai(prompt, temperature, top_p):
     response = client.responses.create(
        model="gpt-4.1",
        input=[
        {
            "role": "system",
            "content": "You are a the usual Chatbot replying like normal."
        },
        {
            "role": "user",
            "content": f"{prompt}"
        }
    ],
        temperature=temperature,
        top_p=top_p,
        max_output_tokens=200
    )
     return response.output_text

def sanitize_number_openai(text): # Probably overkill, but I wanted to try using the chatbot for various things
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "You extract a single numeric value from user input. The result shall be a float with one decimal place."
                    "Return only the number as plain text. "
                    "The decimal places of the result number are seperated by a dot."
                    "If no number is present, return 'ERROR'."
                )
            },
            {
                "role": "user",
                "content": "" + (text)
            }
        ],
        max_output_tokens=16,
        temperature=0.0
    )
    return response.output_text
