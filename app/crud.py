from sqlalchemy.orm import Session
from . import models, schemas
import uuid

# Models CRUD
def create_device_model(db: Session, model: schemas.DeviceModelCreate):
    db_model = models.DeviceModel(
        id=str(uuid.uuid4()),
        name=model.name,
        description=model.description,
        configuration=model.configuration,
    )
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

def get_device_models(db: Session):
    return db.query(models.DeviceModel).all()

def get_device_model(db: Session, model_id: str):
    return db.query(models.DeviceModel).filter(models.DeviceModel.id == model_id).first()

# Telemetry CRUD
def save_telemetry(db: Session, data: schemas.TelemetryPayload):
    telemetry = models.Telemetry(
        id=str(uuid.uuid4()),
        device_id=data.device_id,
        payload=data.payload,
    )
    db.add(telemetry)
    db.commit()
    db.refresh(telemetry)
    return telemetry

def get_telemetry_by_device(db: Session, device_id: str):
    return db.query(models.Telemetry).filter(models.Telemetry.device_id == device_id).order_by(models.Telemetry.timestamp.desc()).all()