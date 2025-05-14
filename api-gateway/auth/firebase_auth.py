# auth/firebase_auth.py
from fastapi import Request, HTTPException
from firebase_admin import auth, credentials, initialize_app, get_app

try:
    get_app()
except ValueError:
    cred = credentials.Certificate("firebase-service-account.json")
    initialize_app(cred)

async def verify_token(request: Request):
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    id_token = auth_header.split(" ")[1]

    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token  # This contains uid, email, etc.
    except Exception as e:
        raise HTTPException(status_code=403, detail="Invalid Firebase ID token")