"""Add endpoints to IPA using FastAPI."""

from typing import Any

from pydantic import BaseModel, Field

from aif.ipa import Request, Response, ipa


class HelloMessage(BaseModel):
    """Model class for hello message."""

    hello: str = Field(description="Hello message")


@ipa.app.get("/hello", response_model=HelloMessage)
@ipa.unauthenticated
async def hello(request: Request, response: Response) -> Any:
    """Be greeted."""
    return HelloMessage(hello="world")
