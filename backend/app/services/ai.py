from dotenv import load_dotenv
# Load environment variables
load_dotenv()

import os
import json
from pathlib import Path
# from openai import AsyncOpenAI
from langfuse.decorators import observe
from langfuse.openai import openai
from langfuse import Langfuse

from app.services.db import get_dci_description




lf = Langfuse()

# Initialize OpenAI client
# client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")  # fallback if not set
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini-2024-07-18")

# Load NGSS standards into memory (once at startup)
# NGSS_PATH = Path(__file__).resolve().parent.parent / "db/ngss.json"
# with open(NGSS_PATH, "r") as f:
#     NGSS_STANDARDS = {s["id"]: s for s in json.load(f)}
#
# # async def generate_root_explanation(fruit: str, root: dict) -> str: (old)
# # Function to generate AI explanation
# @observe()
# def generate_root_explanation(fruit: str, root: dict) -> str:
# #     prompt = (
# #         f"Your goal is to help a student develop mastery of the NGSS standard: {root['id']}.\n"
# #         f"This standard states: \"{root['description']}\"\n"
# #         f"This student is curious about \"{fruit}\".\n"
# #         f"Can you generate a short explanation of this NGSS standard using \"{fruit}\" as an example?"
# #     )
#
#     prompt_obj = lf.get_prompt('first_prompt')
#     prompt = prompt_obj.compile(input_id=root["id"], input_standard=root['description'], input_interest=fruit)
#
#     print(prompt)
#
# #     response = await client.chat.completions.create(
#     response = openai.chat.completions.create(
#
#         model=OPENAI_MODEL,
#         messages=prompt,
# #         messages=[
# #             {
# #                 "role": "system",
# #                 "content": "You are a friendly, engaging science teacher connecting real-life interests to NGSS science standards."
# #             },
# #             {
# #                 "role": "user",
# #                 "content": prompt
# #             }
# #         ],
#         temperature=0.7, # may be a little high
#         max_tokens=1000,
#         langfuse_prompt=prompt_obj
#     )
#
#     return response.choices[0].message.content.strip()

# Optimize Later
# If performance becomes a concern:
# 	•	Cache results in memory
# 	•	Use SQLAlchemy or a lightweight ORM for better abstraction
# Generate explanation for a Disciplinary Core Idea using student's interest
# @observe()
def generate_dci_explanation(group_name: str, interest: str) -> str:
    dci_description = get_dci_description(group_name)
    print("🏁 Commence request ")
    prompt = [
        {
            "role": "system",
            "content": (
                "You are a friendly, engaging science teacher helping students connect their interests "
                "to real scientific ideas from the NGSS Disciplinary Core Ideas."
            )
        },
        {
            "role": "user",
            "content": (
                f"Explain the Disciplinary Core Idea '{group_name}' to a high school student. "
                f"The student is interested in {interest}. "
                f"The full DCI content is:\n{dci_description}\n\n"
                f"Use their interest as an example to help make the idea relatable and engaging."
            )
        }
    ]
    print("👀 Prompt being sent to OpenAI:", prompt)

    try:
        response = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=prompt,
            temperature=0.7,
            max_tokens=1000,
            timeout=15
        )
    except Exception as e:
        print("Error from OPENAI: ", str(e))
        return "Error: couldnt return explanation."
    print("🧠 OpenAI responded:", response)

    print("🧪 using model: ", OPENAI_MODEL)

    return response.choices[0].message.content.strip()
