import uuid
import json
from datetime import datetime
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException
from . import database, schemas

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
            json.dumps(model.configuration)  # <-- сериализуем dict в JSON
        )
    )
    row = cur.fetchone()
    db_conn.commit()
    cur.close()
    return row  # dict благодаря RealDictCursor

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
        raise HTTPException(status_code=404, detail="DeviceModel not found")
    return row

def save_telemetry(db_conn, data: schemas.TelemetryPayload):
    cur = db_conn.cursor(cursor_factory=RealDictCursor)
    new_id = str(uuid.uuid4())
    cur.execute(
        """
        INSERT INTO telemetry(id, device_id, payload)
        VALUES (%s, %s, %s::jsonb)
        RETURNING id, device_id, payload, timestamp
        """,
        (
            new_id,
            str(data.device_id),
            json.dumps(data.payload)  # <-- сериализуем dict в JSON
        )
    )
    row = cur.fetchone()
    db_conn.commit()
    cur.close()
    return row

def get_telemetry_by_device(db_conn, device_id: str):
    cur = db_conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "SELECT * FROM telemetry WHERE device_id = %s ORDER BY timestamp DESC",
        (str(device_id),)
    )
    rows = cur.fetchall()
    cur.close()
    return rows

def generate_firmware_source(db_conn, serial: str):
    cur = db_conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "SELECT configuration FROM device_models WHERE id = %s",
        (serial,)
    )
    row = cur.fetchone()
    cur.close()
    if not row:
        raise HTTPException(status_code=404, detail="Model for firmware not found")

    config = row['configuration']

    with open("templates/base_template.c", "r", encoding="utf-8") as f:
        template = f.read()

    firmware_source = (
        template
        .replace("{{SERIAL}}", serial)
        .replace("{{FEATURE_WIFI}}", str(int(config.get("FEATURE_WIFI", False))))
        .replace("{{FEATURE_BLE}}",  str(int(config.get("FEATURE_BLE",  False))))
    )

    return firmware_source
