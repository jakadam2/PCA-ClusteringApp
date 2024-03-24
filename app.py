from urllib.request import Request
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.api import router

app = FastAPI()
app.include_router(router)

origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:8080",
    "https://localhost:8080",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "https://localhost:3001",
    "https://127.0.0.1:3001",
    "http://127.0.0.1:8080",
    "https://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# async def authenticate(request: Request, call_next):
#     print(request.headers)
#     response = await call_next(request)
#     return response

# app.middleware("http")(authenticate)
# app.middleware("https")(authenticate)

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8080, log_level="debug", reload=True)
