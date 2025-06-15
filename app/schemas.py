from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class DeviceModelBase(BaseModel):
    name: str
    description: Optional[str]
    configuration: Dict

class DeviceModelCreate(DeviceModelBase):
    pass

class DeviceModelRead(DeviceModelBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True

class TelemetryPayload(BaseModel):
    device_id: str
    payload: Dict

class TelemetryRead(TelemetryPayload):
    timestamp: datetime

    class Config:
        orm_mode = True