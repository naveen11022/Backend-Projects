from fastapi import FastAPI
import uvicorn
from Auth import router as Auth_router
from Todo import router as todo_router
app = FastAPI()

app.include_router(Auth_router)
app.include_router(todo_router)

if app=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=8081)
