import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")  # fallback if not set

# Load NGSS standards into memory (once at startup)
NGSS_PATH = Path(__file__).resolve().parent.parent / "data/ngss.json"
with open(NGSS_PATH, "r") as f:
    NGSS_STANDARDS = {s["id"]: s for s in json.load(f)}

# Function to generate AI explanation
async def generate_root_explanation(fruit: str, root: dict) -> str:
    prompt = (
        f"Your goal is to help a student develop mastery of the NGSS standard: {root['id']}.\n"
        f"This standard states: \"{root['description']}\"\n"
        f"This student is curious about \"{fruit}\".\n"
        f"Can you generate a short explanation of this NGSS standard using \"{fruit}\" as an example?"
    )

    print(prompt)

    response = await client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a friendly, engaging science teacher connecting real-life interests to NGSS science standards."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=350,
    )

    return response.choices[0].message.content.strip()
