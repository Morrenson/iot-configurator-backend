from fastapi import APIRouter, Depends
from .. import crud
from ..database import get_db  # теперь зависит от psycopg2-pool

router = APIRouter(prefix="/firmware", tags=["firmware"])

@router.get("/generate/{serial}", response_model=str)
def generate_firmware(serial: str, conn = Depends(get_db)):
    """
    Генерация исходного кода прошивки по серийному номеру.
    conn — psycopg2 соединение из пула.
    """
    # В crud.generate_firmware_source(conn, serial) вы теперь
    # используете raw SQL через conn.cursor()
    return crud.generate_firmware_source(conn, serial)
