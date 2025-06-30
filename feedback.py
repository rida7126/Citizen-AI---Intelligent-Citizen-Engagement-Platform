from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import json

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def feedback_page(request: Request):
    """Feedback submission page"""
    return templates.TemplateResponse("feedback.html", {"request": request})

@router.post("/submit")
async def submit_feedback(request: Request, feedback_text: str = Form(...)):
    """Submit and analyze feedback sentiment"""
    try:
        granite_model = request.app.state.granite_model
        
        # Analyze sentiment using Granite model
        # Use fallback if model is not loaded
        if granite_model.model is None:
            sentiment = granite_model._enhanced_keyword_sentiment(feedback_text)
        else:
            sentiment = await granite_model.analyze_sentiment(feedback_text)

        
        # Store feedback
        feedback_entry = {
            "id": len(request.app.state.feedback_data) + 1,
            "text": feedback_text,
            "sentiment": sentiment,
            "timestamp": datetime.now().isoformat()
        }
        request.app.state.feedback_data.append(feedback_entry)
        
        return JSONResponse({
            "success": True,
            "sentiment": sentiment,
            "message": "Thank you for your feedback!"
        })
        
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@router.get("/analyze")
async def analyze_feedback_sentiment(request: Request, text: str):
    """API endpoint for sentiment analysis"""
    try:
        granite_model = request.app.state.granite_model
        if granite_model.model is None:
            sentiment = granite_model._enhanced_keyword_sentiment(text)  # direct fallback
        else:
            sentiment = await granite_model.analyze_sentiment(text)

        
        return JSONResponse({
            "text": text,
            "sentiment": sentiment
        })
        
    except Exception as e:
        return JSONResponse({
            "error": str(e)
        }, status_code=500)