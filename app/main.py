from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime
from app.models import EnglishContentRequest, TranslatedContent, TranslationPayload
from app.services import translate_text, verify_credentials
from app.config import settings

app = FastAPI(title="Directus Localization Service")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/translate")
async def translate(
    request: EnglishContentRequest,
    credentials = Depends(verify_credentials)
):
    try:
        content_dict = json.loads(request.englishContent)
        translation_payload = TranslationPayload(**content_dict)

        arabic_updates = []
        for update in translation_payload.translations["update"]:
            english_text = update.headline

            arabic_text = await translate_text(
                text=english_text,
                source_language="en",
                target_language="ar"
            )

            arabic_update = {
                "headline": arabic_text,
                "languages_code": {"code": "ar-SA"},
                "id": update.id
            }
            arabic_updates.append(arabic_update)

        arabic_content = {
            "translations": {
                "update": arabic_updates
            }
        }

        return TranslatedContent(arabicContent=json.dumps(
            arabic_content,
            ensure_ascii=False,
            separators=(',', ':')
        ))

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in englishContent")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)