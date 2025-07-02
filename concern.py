from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import json

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def concern_page(request: Request):
    """Concern submission page"""
    return templates.TemplateResponse("concern.html", {"request": request})

@router.post("/submit")
async def submit_concern(
    request: Request, 
    title: str = Form(...), 
    description: str = Form(...),
    category: str = Form(...),
    priority: str = Form(...)
):
    """Submit a new concern/issue"""
    try:
        granite_model = request.app.state.granite_model
        
        # Analyze sentiment of the concern
        sentiment = await granite_model.analyze_sentiment(description)
        
        # Create concern entry
        concern_entry = {
            "id": len(request.app.state.concerns) + 1,
            "title": title,
            "description": description,
            "category": category,
            "priority": priority,
            "sentiment": sentiment,
            "status": "Open",
            "timestamp": datetime.now().isoformat()
        }
        request.app.state.concerns.append(concern_entry)
        
        return JSONResponse({
            "success": True,
            "concern_id": concern_entry["id"],
            "message": "Your concern has been submitted successfully!"
        })
        
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@router.get("/list")
async def list_concerns(request: Request):
    """Get list of all concerns"""
    concerns = request.app.state.concerns
    return JSONResponse({"concerns": concerns})

@router.get("/{concern_id}")
async def get_concern(request: Request, concern_id: int):
    """Get specific concern by ID"""
    concerns = request.app.state.concerns
    concern = next((c for c in concerns if c["id"] == concern_id), None)
    
    if not concern:
        raise HTTPException(status_code=404, detail="Concern not found")
    
    return JSONResponse({"concern": concern})