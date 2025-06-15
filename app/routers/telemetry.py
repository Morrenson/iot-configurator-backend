from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter(prefix="/telemetry", tags=["telemetry"])

@router.post("/", response_model=schemas.TelemetryRead)
def submit_telemetry(payload: schemas.TelemetryPayload, db: Session = Depends(database.get_db)):
    return crud.save_telemetry(db, payload)

@router.get("/{device_id}", response_model=list[schemas.TelemetryRead])
def get_telemetry(device_id: str, db: Session = Depends(database.get_db)):
    return crud.get_telemetry_by_device(db, device_id)