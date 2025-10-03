from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import login

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou coloque o endereço do seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)