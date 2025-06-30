from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.routes.auth import get_current_user
from datetime import datetime
import json
from collections import Counter

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def require_auth(request: Request):
    """Require authentication for dashboard access"""
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, user: str = Depends(require_auth)):
    """Admin dashboard page"""
    # Get analytics data
    feedback_data = request.app.state.feedback_data
    concerns = request.app.state.concerns
    chat_history = request.app.state.chat_history
    
    # Calculate sentiment statistics
    sentiment_counts = Counter([f["sentiment"] for f in feedback_data])
    
    # Calculate concern statistics
    concern_categories = Counter([c["category"] for c in concerns])
    concern_priorities = Counter([c["priority"] for c in concerns])
    concern_statuses = Counter([c["status"] for c in concerns])
    
    # Recent activity
    recent_feedback = feedback_data[-5:] if feedback_data else []
    recent_concerns = concerns[-5:] if concerns else []
    recent_chats = chat_history[-5:] if chat_history else []
    
    dashboard_data = {
        "total_feedback": len(feedback_data),
        "total_concerns": len(concerns),
        "total_chats": len(chat_history),
        "sentiment_stats": dict(sentiment_counts),
        "concern_categories": dict(concern_categories),
        "concern_priorities": dict(concern_priorities),
        "concern_statuses": dict(concern_statuses),
        "recent_feedback": recent_feedback,
        "recent_concerns": recent_concerns,
        "recent_chats": recent_chats
    }
    
    return templates.TemplateResponse(
        "dashboard.html", 
        {"request": request, "user": user, "data": dashboard_data}
    )

@router.get("/analytics")
async def get_analytics(request: Request, user: str = Depends(require_auth)):
    """API endpoint for dashboard analytics"""
    feedback_data = request.app.state.feedback_data
    concerns = request.app.state.concerns
    chat_history = request.app.state.chat_history
    
    # Sentiment analysis
    sentiment_counts = Counter([f["sentiment"] for f in feedback_data])
    
    # Concern analysis
    concern_categories = Counter([c["category"] for c in concerns])
    concern_priorities = Counter([c["priority"] for c in concerns])
    
    # Time-based analysis (last 7 days)
    from datetime import datetime, timedelta
    week_ago = datetime.now() - timedelta(days=7)
    
    recent_feedback = [
        f for f in feedback_data 
        if datetime.fromisoformat(f["timestamp"]) > week_ago
    ]
    
    return JSONResponse({
        "sentiment_distribution": dict(sentiment_counts),
        "concern_categories": dict(concern_categories),
        "concern_priorities": dict(concern_priorities),
        "weekly_feedback_count": len(recent_feedback),
        "total_interactions": len(chat_history) + len(feedback_data) + len(concerns)
    })