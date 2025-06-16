# app/crud.py
import uuid, json
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException
from . import schemas

def create_device_model(db_conn, model: schemas.DeviceModelCreate):
    cur = db_conn.cursor(cursor_factory=RealDictCursor)
    new_id = str(uuid.uuid4())
    cur.execute(
        """
        INSERT INTO device_models(id, name, description, configuration)
        VALUES (%s, %s, %s, %s::jsonb)
        RETURNING id, name, description, configuration, created_at
        """,
        (
            new_id,
            model.name,
            model.description,
            json.dumps(model.configuration)
        )
    )
    row = cur.fetchone()
    db_conn.commit()
    cur.close()
    return row

def list_device_models(db_conn):
    cur = db_conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM device_models ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    return rows

def get_device_model(db_conn, model_id: str):
    cur = db_conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "SELECT * FROM device_models WHERE id = %s",
        (model_id,)
    )
    row = cur.fetchone()
    cur.close()
    if not row:
        raise HTTPException(status_code=404, detail="Device not found")
    return row

def update_device_model(db_conn, model_id: str, model: schemas.DeviceModelCreate):
    cur = db_conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        UPDATE device_models
           SET name = %s,
               description = %s,
               configuration = %s::jsonb
         WHERE id = %s
      RETURNING id, name, description, configuration, created_at
        """,
        (
            model.name,
            model.description,
            json.dumps(model.configuration),
            model_id
        )
    )
    row = cur.fetchone()
    db_conn.commit()
    cur.close()
    if not row:
        raise HTTPException(status_code=404, detail="Device not found")
    return row

def delete_device_model(db_conn, model_id: str):
    cur = db_conn.cursor()
    cur.execute("DELETE FROM device_models WHERE id = %s", (model_id,))
    db_conn.commit()
    cur.close()
