import os
from openai import OpenAI
import re

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o"


def chat(system_prompt:str, use_prompt:str, model_name:str):
    client = OpenAI(
        base_url=endpoint,
        api_key=token,
    )
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": use_prompt,
            }
        ],
        model=model_name,
        temperature=1.0,
        max_tokens=1000,
        top_p=1.0
    )
    return response.choices[0].message.content