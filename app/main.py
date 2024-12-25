from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime
from app.models import TranslatedContent, TranslationPayload
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
    request: Request,
    credentials = Depends(verify_credentials)
):
    try:
        # Get raw body and parse JSON
        raw_body = await request.body()
        body_str = raw_body.decode('utf-8')

        try:
            # Parse the JSON directly
            content_dict = json.loads(body_str)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid JSON format: {str(e)}"
            )

        # Validate the structure using Pydantic
        try:
            translation_payload = TranslationPayload(**content_dict)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid translation payload structure: {str(e)}"
            )

        # Process translations
        arabic_updates = []
        for update in translation_payload.translations.update:
            english_text = update.content  # Changed from headline to content

            arabic_text = await translate_text(
                text=english_text,
                source_language="en",
                target_language="ar"
            )

            arabic_update = {
                "content": arabic_text,  # Changed from headline to content
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
        raw_body = await request.body()
        body_str = raw_body.decode('utf-8')

        try:
            parsed_json = json.loads(body_str)

            # Try to validate with Pydantic
            try:
                translation_payload = TranslationPayload(**parsed_json)
                validation_status = "Successfully validated payload structure"
            except Exception as e:
                validation_status = f"Failed to validate payload: {str(e)}"

            return {
                "raw_body": body_str,
                "parsed_json": parsed_json,
                "validation_status": validation_status,
                "content_type": request.headers.get("content-type"),
                "headers": dict(request.headers)
            }

        except json.JSONDecodeError as e:
            return {
                "error": f"Failed to parse JSON: {str(e)}",
                "raw_body": body_str
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