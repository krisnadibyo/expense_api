from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query
from typing import Optional

from app.api.dependencies import get_wa_service
from app.services.wa_service import WaService


router = APIRouter(
  prefix="",
  tags=["whatsapp"]
)

@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(default=None, alias="hub.mode"),
    hub_challenge: str = Query(default=None, alias="hub.challenge"),
    hub_verify_token: str = Query(default=None, alias="hub.verify_token"),
    wa_service: WaService = Depends(get_wa_service)
):
    return await wa_service.verify_webhook(
        mode=hub_mode,
        challenge=hub_challenge,
        verify_token=hub_verify_token
    )

@router.post("/webhook")
async def receive_webhooks(request: Request, wa_service: WaService = Depends(get_wa_service)):
  try:
    data = await request.json()
    return wa_service.handle_message(data)
  except HTTPException as e:
    raise HTTPException(status_code=500, detail=str(e))
