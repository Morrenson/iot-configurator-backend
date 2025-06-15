from fastapi import APIRouter, Depends, HTTPException
from psycopg2.extensions import connection as _Connection
from .. import schemas, crud, database

router = APIRouter(prefix="/models", tags=["models"])

@router.post("/", response_model=schemas.DeviceModelRead)
def create_model(
    model: schemas.DeviceModelCreate,
    db: _Connection = Depends(database.get_db),
):
    """
    Создаёт новую модель устройства и возвращает её данные.
    """
    return crud.create_device_model(db, model)

@router.get("/", response_model=list[schemas.DeviceModelRead])
def list_models(
    db: _Connection = Depends(database.get_db),
):
    """
    Возвращает список всех моделей устройств.
    """
    return crud.list_device_models(db)

@router.get("/{model_id}", response_model=schemas.DeviceModelRead)
def read_model(
    model_id: str,
    db: _Connection = Depends(database.get_db),
):
    """
    Возвращает одну модель по её ID или 404, если не найдена.
    """
    rec = crud.get_device_model(db, model_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Model not found")
    return rec