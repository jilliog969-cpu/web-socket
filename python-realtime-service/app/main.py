from fastapi import FastAPI

from .auth import router as auth_router
from .ws_bridge import router as ws_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(ws_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
