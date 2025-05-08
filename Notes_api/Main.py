from fastapi import FastAPI
from Auth import router as auth_router
from Notes_api import router as notes_api_router
import uvicorn
app = FastAPI()

app.include_router(auth_router)
app.include_router(notes_api_router)

if app == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8081)