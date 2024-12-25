from pydantic import BaseModel  # Import BaseModel from Pydantic
from typing import List, Any  # Import any other necessary types

# Define your models
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
