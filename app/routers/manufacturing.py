from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter(prefix="/manufacturing", tags=["manufacturing"])

@router.post("/produce", response_model=schemas.TelemetryRead)
def produce_device(data: schemas.TelemetryPayload, db: Session = Depends(database.get_db)):
    # здесь должна быть логика проверки серийного номера и создания записи;
    return crud.save_telemetry(db, data)  # пример