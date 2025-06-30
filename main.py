from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
from datetime import datetime
from typing import Optional
import json

# Import our modules
from app.ai_model import GraniteModel
from app.routes.auth import router as auth_router
from app.routes.chat import router as chat_router
from app.routes.feedback import router as feedback_router
from app.routes.concern import router as concern_router
from app.routes.dashboard import router as dashboard_router

# Initialize FastAPI app
app = FastAPI(title="Citizen AI - Intelligent Citizen Engagement Platform")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="app/templates")

# Initialize AI model (will be loaded on startup)
granite_model = None

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# In-memory storage for demo purposes
app.state.users = {"admin": {"password": "admin123", "role": "admin"}}
app.state.sessions = {}
app.state.feedback_data = []
app.state.concerns = []
app.state.chat_history = []

@app.on_event("startup")
async def startup_event():
    """Initialize the AI model on startup"""
    global granite_model
    print("Loading IBM Granite model...")
    granite_model = GraniteModel()
    await granite_model.load_model()
    app.state.granite_model = granite_model
    print("Model loaded successfully!")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(feedback_router, prefix="/feedback", tags=["feedback"])
app.include_router(concern_router, prefix="/concern", tags=["concerns"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)