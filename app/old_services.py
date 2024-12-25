from openai import AsyncOpenAI
from app.config import settings
import json

client = AsyncOpenAI(api_key=settings.openai_api_key)

async def translate_text(text: str, source_language: str, target_language: str) -> str:
    try:
        translation_prompt = f"""You are an expert translator specializing in English to Arabic translations. Your task is to provide an accurate and natural-sounding translation while preserving the original meaning and tone of the text.

Here is the English content to be translated:

<english_content>
{text}
</english_content>

Please follow these instructions carefully:

1. Read and comprehend the entire English content provided above.
2. Translate the content into Modern Standard Arabic (فصحى), ensuring grammatical correctness and appropriate vocabulary usage.
3. Maintain the original formatting, including paragraphs, line breaks, and any special characters or punctuation marks.
4. Keep proper nouns, brand names, and technical terms in their original form.
5. For idiomatic expressions or culturally specific references, find an Arabic equivalent that conveys the same meaning.
6. After completing the translation, review it to ensure accuracy, fluency, and naturalness in Arabic.

Your final output must be in the following JSON format:
{{
  "arabic_translation": "Your Arabic translation here",
  "translation_notes": "Any relevant notes or explanations about the translation, if necessary"
}}"""

        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Arabic translator. Respond only with the requested JSON format."
                },
                {
                    "role": "user",
                    "content": translation_prompt
                }
            ],
            temperature=0.3
        )

        translation_result = json.loads(response.choices[0].message.content.strip())
        return translation_result["arabic_translation"]

    except json.JSONDecodeError:
        raise Exception("Failed to parse translation response")
    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")