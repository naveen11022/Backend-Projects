from fastapi import FastAPI
from Articles import router as Article_router
from Auth import router as Auth_router
import uvicorn

app = FastAPI()

app.include_router(Article_router, tags=["Articles"])
app.include_router(Auth_router, tags=["Auth"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
