from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import APP_NAME, MAX_UPLOAD_MB
from .gemini_service import generate_recommendations
from .schemas import PlannerRequest

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title=APP_NAME, version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "app_name": APP_NAME},
    )


@app.get("/planner/{planner}", response_class=HTMLResponse)
async def planner_page(request: Request, planner: str):
    labels = {
        "home": "Home Interior Planner",
        "party": "Party Budget Planner",
        "jewelry": "Jewelry Budget Planner",
    }
    if planner not in labels:
        return HTMLResponse("Planner not found", status_code=404)

    return templates.TemplateResponse(
        "planner.html",
        {
            "request": request,
            "app_name": APP_NAME,
            "planner": planner,
            "title": labels[planner],
        },
    )


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": APP_NAME}


@app.post("/api/recommend")
async def recommend(payload: PlannerRequest):
    result = await generate_recommendations(
        payload.planner, payload.budget, payload.details
    )
    return JSONResponse(
        {
            "planner": payload.planner,
            "budget": payload.budget,
            **result,
        }
    )


@app.post("/api/jewelry-image")
async def jewelry_image(file: UploadFile = File(...)):
    allowed = {"image/jpeg", "image/png", "image/webp"}
    if file.content_type not in allowed:
        return JSONResponse({"error": "Only JPG, PNG or WEBP images are allowed."}, status_code=400)

    content = await file.read()
    if len(content) > MAX_UPLOAD_MB * 1024 * 1024:
        return JSONResponse({"error": f"Image must be below {MAX_UPLOAD_MB} MB."}, status_code=400)

    # Store temporarily for the demo UI. The current recommendation engine does not
    # send this image to Gemini. Production image analysis can be added separately.
    safe_name = Path(file.filename or "outfit-image").name
    target = UPLOAD_DIR / safe_name
    target.write_bytes(content)

    return {"filename": safe_name, "message": "Image uploaded successfully for planner use."}
