from fastapi import APIRouter, Depends
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/models", tags=["models"])

@router.post("/", response_model=schemas.DeviceModelRead)
def create_model(model: schemas.DeviceModelCreate, conn = Depends(get_db)):
    return crud.create_device_model(conn, model)

@router.get("/", response_model=list[schemas.DeviceModelRead])
def list_models(conn = Depends(get_db)):
    return crud.list_device_models(conn)
