from fastapi import FastAPI
import uvicorn
from Auth import router as Auth_router
from blog import router as blog_router
app = FastAPI()

app.include_router(Auth_router)
app.include_router(blog_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
