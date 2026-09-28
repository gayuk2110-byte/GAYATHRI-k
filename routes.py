from pathlib import Path

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import get_db
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .gemini_generator import generate_workout_gemini, update_workout_plan
from .models import User
from .schemas import UserInput, FeedbackRequest

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "FitBuddy"},
    )


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        data = UserInput(
            username=username,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )
        plan = generate_workout_gemini(
            data.username, data.age, data.weight, data.goal, data.intensity
        )
        tip = generate_nutrition_tip_with_flash(data.goal)

        existing = db.query(User).filter(User.user_id == data.user_id).first()
        if existing:
            existing.username = data.username
            existing.age = data.age
            existing.weight = data.weight
            existing.goal = data.goal
            existing.intensity = data.intensity
            existing.original_plan = plan
            existing.updated_plan = None
            existing.nutrition_tip = tip
            existing.feedback = None
            user = existing
        else:
            user = User(
                user_id=data.user_id,
                username=data.username,
                age=data.age,
                weight=data.weight,
                goal=data.goal,
                intensity=data.intensity,
                original_plan=plan,
                nutrition_tip=tip,
            )
            db.add(user)

        db.commit()
        db.refresh(user)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={"user": user, "active_plan": user.updated_plan or user.original_plan},
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error": str(exc)},
            status_code=400,
        )


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error": "User not found."},
            status_code=404,
        )

    try:
        request_data = FeedbackRequest(user_id=user_id, feedback=feedback)
        current_plan = user.updated_plan or user.original_plan
        revised = update_workout_plan(
            current_plan, request_data.feedback, user.goal, user.intensity
        )
        user.updated_plan = revised
        user.feedback = request_data.feedback
        db.commit()
        db.refresh(user)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={"user": user, "active_plan": user.updated_plan},
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error": str(exc)},
            status_code=400,
        )


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.created_at.desc()).all()
    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={"users": users},
    )


@router.get("/api/users")
def api_users(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.created_at.desc()).all()
    return [
        {
            "user_id": u.user_id,
            "username": u.username,
            "age": u.age,
            "weight": u.weight,
            "goal": u.goal,
            "intensity": u.intensity,
            "has_updated_plan": bool(u.updated_plan),
            "created_at": u.created_at.isoformat() if u.created_at else None,
        }
        for u in users
    ]


@router.get("/api/users/{user_id}")
def api_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return {"error": "User not found"}
    return {
        "user_id": user.user_id,
        "username": user.username,
        "age": user.age,
        "weight": user.weight,
        "goal": user.goal,
        "intensity": user.intensity,
        "original_plan": user.original_plan,
        "updated_plan": user.updated_plan,
        "nutrition_tip": user.nutrition_tip,
        "feedback": user.feedback,
    }
