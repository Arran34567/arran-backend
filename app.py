from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
import urllib.request

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

class OrderRequest(BaseModel):
    item: str = ""
    qty: int = 1
    total: int = 0
    ship: int = 0
    grand: int = 0
    address: str = ""

@app.post("/order")
def receive_order(order: OrderRequest):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return {"ok": False, "error": "telegram not configured"}
    text = (
        "🛒 ออเดอร์ใหม่ Arran Shop\n"
        f"• {order.item} {order.qty} = {order.total} บาท\n"
        f"• ค่าส่ง {order.ship} บาท\n"
        f"• ยอดรวม {order.grand} บาท\n"
        f"• จัดส่งที่: {order.address}"
    )
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = json.dumps({"chat_id": chat_id, "text": text}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=10)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}
