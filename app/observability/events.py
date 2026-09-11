from typing import Any

from pydantic import BaseModel, ConfigDict


class AgentEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str
    event: str
    status: str
    data: dict[str, Any] = {}