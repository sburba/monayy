from typing import Annotated

from fastapi import APIRouter, Form

router = APIRouter()


@router.post("/account")
async def receive_sms():
    pass


@router.post("/email")
async def receive_email(
        from_addr: Annotated[str, Form(alias="from")],
        to_addr: Annotated[str, Form(alias="to")],
        text: Annotated[str, Form()],
        subject: Annotated[str, Form()]
):
    pass