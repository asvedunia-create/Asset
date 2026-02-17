from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ServiceOut(BaseModel):
    name: str
    version: str


class AssetOut(BaseModel):
    hostname: str
    address: str
    protocol: str
    os_name: str
    owner: str
    last_scanned_at: datetime | None
    services: list[ServiceOut]


class RefreshTarget(BaseModel):
    hostname: str = Field(min_length=1)
    address: str = Field(min_length=1)
    protocol: Literal["ssh", "winrm"]


class RefreshRequest(BaseModel):
    targets: list[RefreshTarget]
