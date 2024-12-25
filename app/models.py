from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class LanguageCode(BaseModel):
    code: str

class TranslationItem(BaseModel):
    content: str
    languages_code: LanguageCode
    id: int

class TranslationOperations(BaseModel):
    create: List[Any] = []
    update: List[TranslationItem]
    delete: List[Any] = []

class TranslationPayload(BaseModel):
    translations: TranslationOperations

class TranslatedContent(BaseModel):
    arabicContent: str