from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter(prefix="/models", tags=["models"])

@router.post("/", response_model=schemas.DeviceModelRead)
def create_model(model: schemas.DeviceModelCreate, db: Session = Depends(database.get_db)):
    return crud.create_device_model(db, model)

@router.get("/", response_model=list[schemas.DeviceModelRead])
def list_models(db: Session = Depends(database.get_db)):
    return crud.get_device_models(db)

@router.get("/{model_id}", response_model=schemas.DeviceModelRead)
def read_model(model_id: str, db: Session = Depends(database.get_db)):
    db_model = crud.get_device_model(db, model_id)
    if not db_model:
        raise HTTPException(status_code=404, detail="Model not found")
    return db_model