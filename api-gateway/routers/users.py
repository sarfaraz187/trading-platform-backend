from fastapi import  Request, APIRouter, Depends, HTTPException
import httpx
import os
from lib.firebase_auth import verify_token

# User router as a sub-router of the API router
router = APIRouter(prefix="/users", tags=["users"])

# Define the USER_SERVICE_URL environment variable
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8000")

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_user_requests(path: str, request: Request, user=Depends(verify_token)):

    print("----------- User Service Proxy Req -------------")
    print(f"Proxying request to user service: {request.method} {USER_SERVICE_URL}/{path}")

    url = f"{USER_SERVICE_URL}/{path}".rstrip("/")
    headers = dict(request.headers)

    # Inject Firebase user info headers
    headers["X-User-Id"] = user["uid"]
    headers["X-User-Email"] = user.get("email", "")

    try:
         async with httpx.AsyncClient() as client:
            req_method = getattr(client, request.method.lower())

            if request.method.upper() in ["POST", "PUT", "PATCH", "DELETE"]:
                body = await request.body()
                response = await req_method(url, content=body, headers=headers)
            else:  # GET, HEAD, OPTIONS, etc.
                params = dict(request.query_params)
                response = await req_method(url, headers=headers, params=params)

            response.raise_for_status()
            # Forward status code and content back to client
            return response.json()

    except httpx.HTTPStatusError as e:
        # Handle HTTP errors from the user service
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    
    except Exception as e:
        # Handle other errors
        raise HTTPException(status_code=500, detail=f"Error proxying request: {str(e)}")