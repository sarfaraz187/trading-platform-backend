from fastapi import  Request, Response, APIRouter, Depends, HTTPException
import httpx
import os
from lib.firebase_auth import verify_token

# User router as a sub-router of the API router
router = APIRouter(prefix="/users", tags=["users"])

# Define the USER_SERVICE_URL environment variable
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8000")

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy_user_requests(path: str, request: Request, user=Depends(verify_token)):
    url = f"{USER_SERVICE_URL}/{path}".rstrip("/")
    
    headers = {}
    for key, value in request.headers.items():
        if key.lower() != "content-length":
            headers[key] = value
    
    # Add user authentication headers
    headers["X-User-Id"] = user["uid"]
    headers["X-User-Email"] = user.get("email", "")
    
    try:
        async with httpx.AsyncClient() as client:
            if request.method.upper() in ["POST", "PUT", "PATCH", "DELETE"]:
                # For requests with body
                body = await request.body()
                print(f"body: {body}")
                response = await getattr(client, request.method.lower())(
                    url, 
                    content=body,
                    headers=headers
                )
            else:
                # For GET requests and similar
                params = dict(request.query_params)
                response = await client.get(url, headers=headers, params=params)
            
            # print(f"response: {response.status_code} {response.text}")
            # Return the full response
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error proxying request: {str(e)}")