from typing import List
import google.generativeai as genai
import os
from discord import Attachment

max_bytes = 4 * 1024 * 1024  # 4MB

genai.configure(api_key=os.getenv("GEMINI_KEY"))


def create_client() -> genai.ChatSession:
        # Set up the model
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
    ]

    model = genai.GenerativeModel(model_name="gemini-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    return model.start_chat(history=[])

async def reply(message: str, attachments: List[Attachment]) -> str:
    if attachments:
        return await _reply_with_attachments(message, attachments)
    return _reply_only_message(message)


def _reply_only_message(message: str) -> str:
    client = create_client()
    reponse = client.send_message(message)
    return reponse.text


async def _reply_with_attachments(prompt: str, attachments: List[Attachment]) -> str:
    model = genai.GenerativeModel("gemini-pro-vision")
    image = attachments[0]
    image_data = await image.read()

    if image.size > max_bytes:
        return "the image size limitation is 4MB. Please reduce your image size."

    contents = {
        "parts": [
            {"mime_type": "image/jpeg", "data": image_data},
            {
                "text": f"Describe this picture as detailed as possible in order to dalle-3 painting plus this {prompt}"
            },
        ]
    }
    response = model.generate_content(contents=contents)
    return response.text


def rewrite_prompt(prompt: str):
    prompt = f"revise `{prompt}` to a DALL-E prompt, return the content in English only return the scene and detail"
    return _reply_only_message(prompt)


def explain_word(word: str):
    prompt =f"""
        Please provide a comprehensive analysis of the given English word. Your response should include the following elements:

        1. Part of Speech: Identify the word's grammatical category (e.g., noun, verb, adjective, adverb, etc.).

        2. English Definition: Provide a clear and concise explanation of the word's meaning in English. If the word has multiple meanings, list the most common ones.

        3. Example Sentences: Create at least two example sentences that demonstrate the correct usage of the word in context. These sentences should be diverse and showcase different aspects of the word's meaning or usage.

        4. Additional Information (optional): If relevant, include any of the following:
        - Etymology (word origin)
        - Synonyms and antonyms
        - Common collocations or phrases
        - Any notable connotations or idiomatic uses

        Please format your response clearly, using headings for each section to ensure easy readability.

        Example word to analyze: [{word}]
    """
    return _reply_only_message(prompt)