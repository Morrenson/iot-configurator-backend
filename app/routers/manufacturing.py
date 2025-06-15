from fastapi import APIRouter, Depends, HTTPException
from .. import schemas, crud
from ..database import get_db  # psycopg2-подключение

router = APIRouter(prefix="/manufacturing", tags=["manufacturing"])

@router.post("/produce", response_model=schemas.TelemetryRead)
def produce_device(
    payload: schemas.TelemetryPayload,
    conn = Depends(get_db),
):
    """
    Приём телеметрии/регистрация произведённого устройства.
    conn — psycopg2 соединение из пула.
    """
    # В crud.save_telemetry(conn, payload) — raw SQL INSERT
    result = crud.save_telemetry(conn, payload)
    if result is None:
        raise HTTPException(status_code=400, detail="Cannot save telemetry")
    return result
