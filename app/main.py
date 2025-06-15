from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routers import models, manufacturing, firmware, telemetry

app = FastAPI(title="IoT Platform with UI")

# Статика: CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")
# Шаблоны Jinja2
templates = Jinja2Templates(directory="templates")

# Подключаем API-роутеры
app.include_router(models.router)
app.include_router(manufacturing.router)
app.include_router(firmware.router)
app.include_router(telemetry.router)

# UI-маршруты
@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/create")
async def create_model_page(request: Request):
    return templates.TemplateResponse("create_model.html", {"request": request})

@app.get("/view/{model_id}")
async def view_model_page(request: Request, model_id: str):
    return templates.TemplateResponse("view_model.html", {"request": request, "model_id": model_id})