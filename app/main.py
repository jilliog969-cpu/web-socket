import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .auth import router as auth_router
from .ws_bridge import router as ws_router

app = FastAPI(title="Realtime Adapter Service (Python)")

# CORS tuỳ nhu cầu
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(ws_router)

@app.get("/healthz")
def healthz():
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
