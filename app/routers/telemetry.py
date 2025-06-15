from fastapi import APIRouter, Depends
from psycopg2.extensions import connection as _Connection
from .. import schemas, crud, database

router = APIRouter(prefix="/telemetry", tags=["telemetry"])

@router.post("/", response_model=schemas.TelemetryRead)
def submit_telemetry(payload: schemas.TelemetryPayload, db: _Connection = Depends(database.get_db)):
    return crud.save_telemetry(db, payload)

@router.get("/{device_id}", response_model=list[schemas.TelemetryRead])
def get_telemetry(device_id: str, db: _Connection = Depends(database.get_db)):
    return crud.get_telemetry_by_device(db, device_id)
