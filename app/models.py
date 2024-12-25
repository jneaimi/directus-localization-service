from pydantic import BaseModel
from typing import List, Dict, Any

class TranslationUpdate(BaseModel):
    headline: str
    languages_code: Dict[str, str]
    id: int

class TranslationPayload(BaseModel):
    translations: Dict[str, List[TranslationUpdate]]

class EnglishContentRequest(BaseModel):
    englishContent: str

class TranslatedContent(BaseModel):
    arabicContent: str

class TranslatedContent(BaseModel):
    arabicContent: str

    class Config:
        json_encoders = {
            str: lambda v: v
        }