import uvicorn
from fastapi import FastAPI

from source.api.api import router

app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, log_level="debug", reload=True)
