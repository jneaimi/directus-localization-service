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
        if not request.translations:
            raise HTTPException(
                status_code=400,
                detail="No valid translation data found"
            )

        # Process translations
        arabic_updates = []
        for update in request.translations.update:
            english_text = update.content

            arabic_text = await translate_text(
                text=english_text,
                source_language="en",
                target_language="ar"
            )

            arabic_update = {
                "content": arabic_text,
                "languages_code": {"code": "ar-SA"},
                "id": update.id
            }
            arabic_updates.append(arabic_update)

        arabic_content = {
            "translations": {
                "create": [],
                "update": arabic_updates,
                "delete": []
            }
        }

        return TranslatedContent(arabicContent=json.dumps(
            arabic_content,
            ensure_ascii=False,
            separators=(',', ':')
        ))

    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # For debugging
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/debug")
async def debug_request(request: Request):
    try:
        body = await request.json()
        return {
            "received_data": body,
            "content_type": request.headers.get("content-type"),
            "headers": dict(request.headers)
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)