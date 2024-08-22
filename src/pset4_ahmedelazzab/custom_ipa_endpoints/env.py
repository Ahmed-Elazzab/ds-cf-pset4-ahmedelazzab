"""Output the environment name."""
import os
from typing import Any

from pydantic import BaseModel, Field

from aif.ipa import Request, Response, ipa


class Deployment(BaseModel):
    """Model class for deployment."""

    deployment_name: str = Field(description="Deployment name")


@ipa.app.get("/environment", response_model=Deployment)
@ipa.unauthenticated
async def environment(request: Request, response: Response) -> Any:
    """Output environment name."""
    return Deployment(deployment_name=os.environ.get("IPA_DEPLOYMENT_NAME", "<unknown>"))
