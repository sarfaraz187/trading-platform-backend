from fastapi import FastAPI
from routers import users

app = FastAPI(redirect_slashes=True)
app.include_router(users.router, prefix="/api/v1")

@app.get("/api/")
async def root():
    return {"message": "Home page"}

@app.get("/api/health")
def health():
    return { "status": "healthy" }
