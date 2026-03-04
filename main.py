from fastapi import FastAPI, Request
import requests
import os
from openai import OpenAI

app = FastAPI()

TOKEN = os.getenv("TELEGRAM_TOKEN")

# Kết nối tới API server của bạn
client = OpenAI(
    api_key="namnl",
    base_url="https://opencodefreemodelsapi.onrender.com/v1"
)

@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    if not chat_id or not text:
        return {"ok": True}

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": "Bạn là trợ lý AI trả lời ngắn gọn, thông minh."},
            {"role": "user", "content": text}
        ]
    )

    reply = response.choices[0].message.content

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": reply}
    )

    return {"ok": True}
