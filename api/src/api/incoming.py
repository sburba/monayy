import uuid
from dataclasses import dataclass
from typing import Annotated

from fastapi import APIRouter, Form, Depends

from src.incoming.incoming_messages import IncomingMessageService, IncomingMessage

router = APIRouter()


@dataclass
class IncomingSms:
    From: str
    To: str
    Body: str


@router.post("/sms")
async def receive_sms(sms: IncomingSms):
    return sms


@router.post("/email")
async def receive_email(
        from_addr: Annotated[str, Form(alias="from")],
        to_addr: Annotated[str, Form(alias="to")],
        text: Annotated[str, Form()],
        message_service: Annotated[IncomingMessageService, Depends(IncomingMessageService)]
):
    await message_service.queue_incoming_email(from_addr=from_addr, to_addr=to_addr, text=text)
