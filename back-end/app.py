import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import multiprocessing

from source.api.api import router

app = FastAPI()
app.include_router(router)

origins = [
    "http://localhost:3000", "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    print("backend here")
    multiprocessing.freeze_support()
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug", reload=False, workers=1)
