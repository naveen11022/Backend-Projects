from fastapi import FastAPI
from Auth import router as Auth_router
from Api import router as API_router
import uvicorn

app = FastAPI()

app.include_router(Auth_router)
app.include_router(API_router)

if app == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)