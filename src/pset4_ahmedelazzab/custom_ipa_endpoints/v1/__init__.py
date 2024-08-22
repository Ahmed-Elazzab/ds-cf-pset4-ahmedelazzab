"""Add scoped endpoints to IPA using FastAPI."""
from typing import Any

from pydantic import BaseModel, Field

from aif.ipa import Request, Response, ipa

scopedapp = ipa.scopedapp()


class HiMessage(BaseModel):
    """Model class for hello message."""

    hi: str = Field(description="Hi message")


@scopedapp.get("/hi", response_model=HiMessage)
@ipa.unauthenticated
async def hi(request: Request, response: Response) -> Any:
    """Get a useless JSON."""
    return HiMessage(hi="world")
