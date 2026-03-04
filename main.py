from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

TOKEN = os.getenv("TELEGRAM_TOKEN")

@app.get("/")
def home():
    return {"status": "OpenClaw running"}

@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text",
