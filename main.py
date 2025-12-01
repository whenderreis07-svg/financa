from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import PlainTextResponse
import os

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "financas123")


@app.get("/")
def healthcheck():
    return {"status": "ok", "service": "whatsapp-financas"}


@app.get("/webhook")
async def verify_webhook(
    hub_mode: str | None = Query(None, alias="hub.mode"),
    hub_challenge: str | None = Query(None, alias="hub.challenge"),
    hub_verify_token: str | None = Query(None, alias="hub.verify_token"),
):
    """
    Endpoint chamado pela Meta na hora de validar o webhook.
    Ela envia:
      - hub.mode
      - hub.challenge
      - hub.verify_token
    Aqui usamos alias para mapear certinho esses nomes.
    """
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(hub_challenge or "")
    raise HTTPException(status_code=403, detail="Invalid verify token")


@app.post("/webhook")
async def receive_webhook(request: Request):
    body = await request.json()
    print("WEBHOOK RECEBIDO:", body)
    return {"status": "received"}
