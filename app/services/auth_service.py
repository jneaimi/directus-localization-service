import secrets
from fastapi import HTTPException, Security
from fastapi.security import HTTPBasicCredentials

USERNAME = "admin"
PASSWORD = "password"

def verify_credentials(credentials: HTTPBasicCredentials = Security(HTTPBasic())):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials