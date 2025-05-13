from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import api

app = FastAPI()
app.include_router(api.router)

origins = [
    "http://localhost:5173",  # local dev
    "https://fruitstoroots.vercel.app",  # your Vercel frontend (if deployed)
    "https://fruitstoroots.com",  # future root domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # precise matching
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)