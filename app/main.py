from fastapi import FastAPI, Request, Depends, HTTPException, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime
import secrets
from app.models import EnglishContentRequest, TranslatedContent, TranslationPayload
from app.services import translate_text
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

security = HTTPBasic()

# Basic auth credentials
USERNAME = "admin"
PASSWORD = "password"

def verify_credentials(credentials: HTTPBasicCredentials = Security(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials

@app.post("/translate")
async def translate(
    request: EnglishContentRequest,
    credentials: HTTPBasicCredentials = Depends(verify_credentials)
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

        # Modified this line to handle Arabic characters properly
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