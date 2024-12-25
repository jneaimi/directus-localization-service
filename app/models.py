from pydantic import BaseModel, root_validator
from typing import List, Dict, Optional, Any, Union

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

class EnglishContentRequest(BaseModel):
    englishContent: Optional[str] = None
    translations: Optional[TranslationOperations] = None

    @root_validator(pre=True)
    def check_content_format(cls, values):
        # Check if we have direct translations object
        if 'translations' in values and not values.get('englishContent'):
            return values

        # Check if we have wrapped content
        if 'englishContent' in values:
            try:
                content = json.loads(values['englishContent'])
                if 'translations' in content:
                    values['translations'] = content['translations']
            except:
                pass
        return values

class TranslatedContent(BaseModel):
    arabicContent: str