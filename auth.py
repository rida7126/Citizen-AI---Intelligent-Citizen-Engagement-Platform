from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import uuid
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_current_user(request: Request) -> Optional[str]:
    """Get current user from session"""
    session_id = request.cookies.get("session_id")
    if session_id and session_id in request.app.state.sessions:
        return request.app.state.sessions[session_id]["username"]
    return None

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    """Process login"""
    users = request.app.state.users
    
    if username in users and users[username]["password"] == password:
        # Create session
        session_id = str(uuid.uuid4())
        request.app.state.sessions[session_id] = {
            "username": username,
            "role": users[username]["role"]
        }
        
        # Redirect to dashboard with session cookie
        response = RedirectResponse(url="/dashboard/admin", status_code=302)
        response.set_cookie(key="session_id", value=session_id, httponly=True)
        return response
    else:
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "error": "Invalid username or password"}
        )

@router.get("/logout")
async def logout(request: Request):
    """Logout user"""
    session_id = request.cookies.get("session_id")
    if session_id and session_id in request.app.state.sessions:
        del request.app.state.sessions[session_id]
    
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="session_id")
    return response