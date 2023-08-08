from typing import Annotated

from fastapi import APIRouter, Form

from src.incoming_messages import IncomingSms, IncomingEmail

router = APIRouter()


@router.post("/account")
async def receive_sms(sms: IncomingSms):
    return sms


@router.post("/email")
async def receive_email(
        from_addr: Annotated[str, Form(alias="from")],
        to_addr: Annotated[str, Form(alias="to")],
        text: Annotated[str, Form()],
        subject: Annotated[str, Form()]
):
    print(IncomingEmail(subject, text, from_addr, to_addr))
