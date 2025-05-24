from fastapi import FastAPI
from routers import users
import httpx

app = FastAPI(redirect_slashes=True)
app.include_router(users.router, prefix="/api/v1")

@app.get("/api/")
async def root():
    return {"message": "Home page"}

@app.get("/api/health")
def health():
    return { "status": "healthy" }

@app.get("/combined-openapi.json")
async def combined_openapi():
    async with httpx.AsyncClient() as client:
        user_spec = (await client.get("http://localhost:8001/openapi.json")).json()
        # auth_spec = (await client.get("http://localhost:8002/openapi.json")).json()
    
    # Simplified: just return multiple specs (you can merge them properly)
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Unified API",
            "version": "1.0"
        },
        "paths": {
            **user_spec.get("paths", {}),
            # **auth_spec.get("paths", {}),
        },
        "components": {
            "schemas": {
                **user_spec.get("components", {}).get("schemas", {}),
                # **auth_spec.get("components", {}).get("schemas", {}),
            }
        }
    }