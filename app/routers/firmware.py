from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, database

router = APIRouter(prefix="/firmware", tags=["firmware"])

@router.get("/generate/{serial}", response_model=str)
def generate(serial: str, db: Session = Depends(database.get_db)):
    # пример генерации: возвращаем строку с кодом прошивки
    return crud.generate_firmware_source(db, serial)