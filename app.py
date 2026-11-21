from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str = ""

@app.get("/")
def home():
    return {"status": "ok", "message": "Arran AI Core - พี่น้องไม่ทิ้งกัน"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(data: ChatRequest):
    return {"reply": f"รับทราบครับพี่: {data.message}"}
