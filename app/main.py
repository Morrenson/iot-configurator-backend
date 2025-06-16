# app/main.py
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json

from . import database, crud, schemas

app = FastAPI()

# статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    db = next(database.get_db())
    devices = crud.list_device_models(db)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "devices": devices
    })


@app.get("/devices/new", response_class=HTMLResponse)
def add_device_form(request: Request):
    return templates.TemplateResponse("add_device.html", {
        "request":     request,
        "error":       None,
        "name":        "",
        "description": "",
        "config":      "",
        "edit":       False,
        "device_id":  None
    })


@app.post("/devices/new")
def add_device(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    config: str = Form(...)
):
    # проверяем JSON
    try:
        cfg = json.loads(config)
    except json.JSONDecodeError:
        return templates.TemplateResponse("add_device.html", {
            "request":     request,
            "error":       "Invalid JSON in configuration",
            "name":        name,
            "description": description,
            "config":      config,
            "edit":       False,
            "device_id":  None
        })

    db = next(database.get_db())
    model_in = schemas.DeviceModelCreate(
        name=name,
        description=description,
        configuration=cfg
    )
    crud.create_device_model(db, model_in)
    return RedirectResponse("/", status_code=303)


@app.get("/devices/{device_id}", response_class=HTMLResponse)
def view_device(request: Request, device_id: str):
    db = next(database.get_db())
    device = crud.get_device_model(db, device_id)
    return templates.TemplateResponse("device.html", {
        "request":  request,
        "device":   device
    })


@app.get("/devices/{device_id}/edit", response_class=HTMLResponse)
def edit_device_form(request: Request, device_id: str):
    db = next(database.get_db())
    device = crud.get_device_model(db, device_id)
    # конфиг как отформатированная строка
    cfg_text = json.dumps(device["configuration"], indent=2, ensure_ascii=False)
    return templates.TemplateResponse("add_device.html", {
        "request":     request,
        "error":       None,
        "name":        device["name"],
        "description": device["description"],
        "config":      cfg_text,
        "edit":       True,
        "device_id":  device_id
    })


@app.post("/devices/{device_id}/edit")
def edit_device(
    request: Request,
    device_id: str,
    name: str = Form(...),
    description: str = Form(""),
    config: str = Form(...)
):
    try:
        cfg = json.loads(config)
    except json.JSONDecodeError:
        return templates.TemplateResponse("add_device.html", {
            "request":     request,
            "error":       "Invalid JSON in configuration",
            "name":        name,
            "description": description,
            "config":      config,
            "edit":       True,
            "device_id":  device_id
        })

    db = next(database.get_db())
    crud.update_device_model(db, device_id, schemas.DeviceModelCreate(
        name=name,
        description=description,
        configuration=cfg
    ))
    return RedirectResponse(f"/devices/{device_id}", status_code=303)


@app.get("/devices/{device_id}/delete")
def delete_device(device_id: str):
    db = next(database.get_db())
    crud.delete_device_model(db, device_id)
    return RedirectResponse("/", status_code=303)
