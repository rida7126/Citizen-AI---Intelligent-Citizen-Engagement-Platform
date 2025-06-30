from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import json

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    """Chat interface page"""
    return templates.TemplateResponse("chat.html", {"request": request})

@router.post("/ask")
async def ask_question(request: Request, question: str = Form(...)):
    """Process user question and return AI response"""
    try:
        granite_model = request.app.state.granite_model
        
        # Generate AI response
        ai_response = await granite_model.chat_response(question)
        
        # Store chat history
        chat_entry = {
            "id": len(request.app.state.chat_history) + 1,
            "user_question": question,
            "ai_response": ai_response,
            "timestamp": datetime.now().isoformat()
        }
        request.app.state.chat_history.append(chat_entry)
        
        return JSONResponse({
            "success": True,
            "response": ai_response,
            "timestamp": chat_entry["timestamp"]
        })
        
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@router.get("/history")
async def get_chat_history(request: Request):
    """Get recent chat history"""
    history = request.app.state.chat_history[-10:]  # Last 10 conversations
    return JSONResponse({"history": history})