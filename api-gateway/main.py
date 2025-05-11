from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import os
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase-service-account.json")
firebase_admin.initialize_app(cred)

app = FastAPI()

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8000")

async def verify_token(request: Request):
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid auth header")

    id_token = auth_header.split(" ")[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print("Token verification failed:", str(e))
        raise HTTPException(status_code=403, detail="Invalid Firebase ID token")

@app.get("/health")
async def health(request: Request):
    user_info = await verify_token(request)
    return {"api-gateway": "running"}

@app.post("/user/register")
async def proxy_register(request: Request):
    user_info = await verify_token(request)
    payload = await request.json()

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{USER_SERVICE_URL}/user/register", json=payload)

    return JSONResponse(status_code=response.status_code, content=response.json())
