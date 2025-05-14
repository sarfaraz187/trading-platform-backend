from fastapi import FastAPI, Request, Depends, APIRouter
import httpx
import os
from lib.firebase_auth import verify_token

app = FastAPI()

router = APIRouter(prefix="/api/v1/users", tags=["users"])
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8000")

# Proxy all user-related requests to the user service
@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_user_requests(path: str, request: Request, user=Depends(verify_token)):

    print(f"Proxying request to user service: {request.method} {USER_SERVICE_URL}/{path}")
    print(f"User info: {user}")
    print(f"Request headers: {request.headers}")
    async with httpx.AsyncClient() as client:
        req_method = getattr(client, request.method.lower())
        url = f"{USER_SERVICE_URL}/{path}"

        body = await request.body()
        headers = dict(request.headers)
        
        # Inject Firebase UID or email into downstream request
        headers["X-User-Id"] = user["uid"]
        headers["X-User-Email"] = user.get("email", "")

        response = await req_method(url, content=body, headers=headers)
        return response.json()
    
@app.get("/health")
async def health(request: Request):
    user_info = await verify_token(request)
    return {"api-gateway": "running"}

# @app.post("/user/register")
# async def proxy_register(request: Request):
#     user_info = await verify_token(request)
#     payload = await request.json()

#     async with httpx.AsyncClient() as client:
#         response = await client.post(f"{USER_SERVICE_URL}/user/register", json=payload)

#     return JSONResponse(status_code=response.status_code, content=response.json())
