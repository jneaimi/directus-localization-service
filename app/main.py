from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime
from app.models import TranslationPayload, TranslatedContent
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

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import TranslationPayload, TranslatedContent
from app.services import translate_text, verify_credentials
import json

app = FastAPI(title="Directus Localization Service")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with allowed origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/translate")
async def translate(
    payload: TranslationPayload,
    credentials=Depends(verify_credentials)
):
    import logging
    logger = logging.getLogger("uvicorn.error")
    logger.info(f"Payload received: {payload.json()}")  # Log the received payload
    
    try:
        arabic_updates = []
        for update in payload.translations.update:
            english_text = update.content
            arabic_text = await translate_text(
                text=english_text,
                source_language="en",
                target_language="ar"
            )
            arabic_updates.append({
                "content": arabic_text,
                "languages_code": {"code": "ar-SA"},
                "id": update.id
            })
        return {"translations": {"create": [], "update": arabic_updates, "delete": []}}
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")



@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)