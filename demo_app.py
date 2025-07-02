"""
Citizen AI Demo Application
A simplified version that works without GPU dependencies
"""

from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import uvicorn
import uuid
import json
from typing import Optional

# Initialize FastAPI app
app = FastAPI(title="Citizen AI - Demo Version")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="app/templates")

# Simple in-memory storage
app.state.users = {"admin": {"password": "admin123", "role": "admin"}}
app.state.sessions = {}
app.state.feedback_data = [
    {"id": 1, "text": "The online tax portal is excellent!", "sentiment": "Positive", "timestamp": datetime.now().isoformat()},
    {"id": 2, "text": "Service could be improved", "sentiment": "Neutral", "timestamp": datetime.now().isoformat()},
    {"id": 3, "text": "Very disappointed with the response time", "sentiment": "Negative", "timestamp": datetime.now().isoformat()}
]
app.state.concerns = [
    {"id": 1, "title": "Road Repair Needed", "description": "Main street has potholes", "category": "Infrastructure", "priority": "High", "sentiment": "Negative", "status": "Open", "timestamp": datetime.now().isoformat()},
    {"id": 2, "title": "Library Hours", "description": "Please extend library hours", "category": "Public Services", "priority": "Medium", "sentiment": "Neutral", "status": "Open", "timestamp": datetime.now().isoformat()}
]
app.state.chat_history = [
    {"id": 1, "user_question": "How to apply for ration card?", "ai_response": "Visit your local government office with required documents", "timestamp": datetime.now().isoformat()}
]

# Simple AI responses for demo
def get_ai_response(question: str) -> str:
    """Simple keyword-based responses for demo"""
    question_lower = question.lower()
    
    if any(word in question_lower for word in ["ration", "card", "food"]):
        return "To apply for a ration card, visit your local government office with proof of identity, address, and income. The process typically takes 2-3 weeks."
    elif any(word in question_lower for word in ["pension", "retirement", "elderly"]):
        return "Pension schemes are available for senior citizens. You can apply online through the government portal or visit the nearest pension office with required documents."
    elif any(word in question_lower for word in ["license", "driving", "permit"]):
        return "For driving license applications, visit the RTO office with required documents including age proof, address proof, and medical certificate."
    elif any(word in question_lower for word in ["tax", "income", "filing"]):
        return "Income tax filing can be done online through the government tax portal. Ensure you have all necessary documents and file before the deadline."
    else:
        return "Thank you for your query. For specific information about government services, please contact the relevant department or visit the official government website."

def analyze_sentiment(text: str) -> str:
    """Simple sentiment analysis for demo"""
    text_lower = text.lower()
    positive_words = ["good", "great", "excellent", "happy", "satisfied", "thank", "amazing", "wonderful"]
    negative_words = ["bad", "terrible", "awful", "angry", "disappointed", "worst", "horrible", "frustrated"]
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return "Positive"
    elif negative_count > positive_count:
        return "Negative"
    else:
        return "Neutral"

def get_current_user(request: Request) -> Optional[str]:
    """Get current user from session"""
    session_id = request.cookies.get("session_id")
    if session_id and session_id in app.state.sessions:
        return app.state.sessions[session_id]["username"]
    return None

def require_auth(request: Request):
    """Require authentication"""
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Auth routes
@app.get("/auth/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/auth/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    users = app.state.users
    if username in users and users[username]["password"] == password:
        session_id = str(uuid.uuid4())
        app.state.sessions[session_id] = {"username": username, "role": users[username]["role"]}
        response = RedirectResponse(url="/dashboard/admin", status_code=302)
        response.set_cookie(key="session_id", value=session_id, httponly=True)
        return response
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/auth/logout")
async def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id and session_id in app.state.sessions:
        del app.state.sessions[session_id]
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="session_id")
    return response

# Chat routes
@app.get("/chat/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat/ask")
async def ask_question(request: Request, question: str = Form(...)):
    ai_response = get_ai_response(question)
    chat_entry = {
        "id": len(app.state.chat_history) + 1,
        "user_question": question,
        "ai_response": ai_response,
        "timestamp": datetime.now().isoformat()
    }
    app.state.chat_history.append(chat_entry)
    
    return JSONResponse({
        "success": True,
        "response": ai_response,
        "timestamp": chat_entry["timestamp"]
    })

# Feedback routes
@app.get("/feedback/", response_class=HTMLResponse)
async def feedback_page(request: Request):
    return templates.TemplateResponse("feedback.html", {"request": request})

@app.post("/feedback/submit")
async def submit_feedback(request: Request, feedback_text: str = Form(...)):
    sentiment = analyze_sentiment(feedback_text)
    feedback_entry = {
        "id": len(app.state.feedback_data) + 1,
        "text": feedback_text,
        "sentiment": sentiment,
        "timestamp": datetime.now().isoformat()
    }
    app.state.feedback_data.append(feedback_entry)
    
    return JSONResponse({
        "success": True,
        "sentiment": sentiment,
        "message": "Thank you for your feedback!"
    })

# Concern routes
@app.get("/concern/", response_class=HTMLResponse)
async def concern_page(request: Request):
    return templates.TemplateResponse("concern.html", {"request": request})

@app.post("/concern/submit")
async def submit_concern(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    priority: str = Form(...)
):
    sentiment = analyze_sentiment(description)
    concern_entry = {
        "id": len(app.state.concerns) + 1,
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
        "sentiment": sentiment,
        "status": "Open",
        "timestamp": datetime.now().isoformat()
    }
    app.state.concerns.append(concern_entry)
    
    return JSONResponse({
        "success": True,
        "concern_id": concern_entry["id"],
        "message": "Your concern has been submitted successfully!"
    })

@app.get("/concern/list")
async def list_concerns(request: Request):
    return JSONResponse({"concerns": app.state.concerns})

# Dashboard routes
@app.get("/dashboard/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, user: str = Depends(require_auth)):
    from collections import Counter
    
    feedback_data = app.state.feedback_data
    concerns = app.state.concerns
    chat_history = app.state.chat_history
    
    sentiment_counts = Counter([f["sentiment"] for f in feedback_data])
    concern_categories = Counter([c["category"] for c in concerns])
    
    dashboard_data = {
        "total_feedback": len(feedback_data),
        "total_concerns": len(concerns),
        "total_chats": len(chat_history),
        "sentiment_stats": dict(sentiment_counts),
        "concern_categories": dict(concern_categories),
        "recent_feedback": feedback_data[-5:],
        "recent_concerns": concerns[-5:],
        "recent_chats": chat_history[-5:]
    }
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "user": user, 
        "data": dashboard_data
    })

@app.get("/dashboard/analytics")
async def get_analytics(request: Request, user: str = Depends(require_auth)):
    from collections import Counter
    
    feedback_data = app.state.feedback_data
    concerns = app.state.concerns
    chat_history = app.state.chat_history
    
    sentiment_counts = Counter([f["sentiment"] for f in feedback_data])
    concern_categories = Counter([c["category"] for c in concerns])
    
    return JSONResponse({
        "sentiment_distribution": dict(sentiment_counts),
        "concern_categories": dict(concern_categories),
        "total_interactions": len(chat_history) + len(feedback_data) + len(concerns),
        "weekly_feedback_count": len(feedback_data)
    })

if __name__ == "__main__":
    print("🤖 Starting Citizen AI Demo Platform...")
    print("📊 Features: Chat Assistant, Sentiment Analysis, Concern Management, Admin Dashboard")
    print("🔑 Admin Login: username=admin, password=admin123")
    print("🌐 Access at: http://localhost:8000")
    uvicorn.run("demo_app:app", host="0.0.0.0", port=8000, reload=True)