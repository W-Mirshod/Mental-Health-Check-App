import os
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from . import database, models, schemas, crud, utils

# Determine base directory
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

app = FastAPI(
    title="Mental Health Check",
    description="Track your mood, journal your thoughts, and monitor your wellness journey",
    version="1.0.0"
)

# CORS configuration for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Mount static files
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main page."""
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading page: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Mental Health Check"}

# Dashboard endpoints
@app.get("/api/dashboard/stats")
async def get_dashboard_stats(db: Session = Depends(database.get_db)):
    """Get dashboard statistics."""
    try:
        return crud.get_wellness_stats(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")

@app.get("/api/dashboard/trends")
async def get_mood_trends(db: Session = Depends(database.get_db)):
    """Get mood trends for the last 30 days."""
    try:
        return crud.get_mood_trends(db, 30)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching trends: {str(e)}")

@app.get("/api/dashboard/recent")
async def get_recent_activities(db: Session = Depends(database.get_db)):
    """Get recent wellness activities."""
    try:
        return crud.get_recent_activities(db, 7)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recent activities: {str(e)}")

# Mood endpoints
@app.post("/api/mood", response_model=schemas.MoodEntry)
async def create_mood_entry(mood_entry: schemas.MoodEntryCreate, db: Session = Depends(database.get_db)):
    """Create or update today's mood entry."""
    try:
        return crud.create_mood_entry(db, mood_entry)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating mood entry: {str(e)}")

@app.get("/api/mood", response_model=schemas.MoodEntryList)
async def get_mood_entries(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Get all mood entries."""
    try:
        entries = crud.get_mood_entries(db, skip=skip, limit=limit)
        return {"entries": entries, "total": len(entries)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching mood entries: {str(e)}")

@app.get("/api/mood/today")
async def get_today_mood(db: Session = Depends(database.get_db)):
    """Get today's mood entry."""
    try:
        from datetime import datetime
        entry = crud.get_mood_entry_by_date(db, datetime.now())
        return entry or {"message": "No mood entry for today"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching today's mood: {str(e)}")

@app.put("/api/mood/{entry_id}", response_model=schemas.MoodEntry)
async def update_mood_entry(entry_id: int, mood_entry: schemas.MoodEntryCreate, db: Session = Depends(database.get_db)):
    """Update a mood entry."""
    try:
        db_entry = crud.update_mood_entry(db, entry_id, mood_entry)
        if db_entry is None:
            raise HTTPException(status_code=404, detail="Mood entry not found")
        return db_entry
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating mood entry: {str(e)}")

@app.delete("/api/mood/{entry_id}")
async def delete_mood_entry(entry_id: int, db: Session = Depends(database.get_db)):
    """Delete a mood entry."""
    try:
        db_entry = crud.delete_mood_entry(db, entry_id)
        if db_entry is None:
            raise HTTPException(status_code=404, detail="Mood entry not found")
        return {"message": "Mood entry deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting mood entry: {str(e)}")

# Journal endpoints
@app.post("/api/journal", response_model=schemas.JournalEntry)
async def create_journal_entry(journal_entry: schemas.JournalEntryCreate, db: Session = Depends(database.get_db)):
    """Create a new journal entry."""
    try:
        return crud.create_journal_entry(db, journal_entry)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating journal entry: {str(e)}")

@app.get("/api/journal", response_model=schemas.JournalEntryList)
async def get_journal_entries(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Get all journal entries."""
    try:
        entries = crud.get_journal_entries(db, skip=skip, limit=limit)
        return {"entries": entries, "total": len(entries)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching journal entries: {str(e)}")

@app.get("/api/journal/{entry_id}", response_model=schemas.JournalEntry)
async def get_journal_entry(entry_id: int, db: Session = Depends(database.get_db)):
    """Get a specific journal entry."""
    try:
        entry = crud.get_journal_entry_by_id(db, entry_id)
        if entry is None:
            raise HTTPException(status_code=404, detail="Journal entry not found")
        return entry
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching journal entry: {str(e)}")

@app.put("/api/journal/{entry_id}", response_model=schemas.JournalEntry)
async def update_journal_entry(entry_id: int, journal_entry: schemas.JournalEntryCreate, db: Session = Depends(database.get_db)):
    """Update a journal entry."""
    try:
        db_entry = crud.update_journal_entry(db, entry_id, journal_entry)
        if db_entry is None:
            raise HTTPException(status_code=404, detail="Journal entry not found")
        return db_entry
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating journal entry: {str(e)}")

@app.delete("/api/journal/{entry_id}")
async def delete_journal_entry(entry_id: int, db: Session = Depends(database.get_db)):
    """Delete a journal entry."""
    try:
        db_entry = crud.delete_journal_entry(db, entry_id)
        if db_entry is None:
            raise HTTPException(status_code=404, detail="Journal entry not found")
        return {"message": "Journal entry deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting journal entry: {str(e)}")

# Wellness Activity endpoints
@app.post("/api/activities", response_model=schemas.WellnessActivity)
async def create_wellness_activity(activity: schemas.WellnessActivityCreate, db: Session = Depends(database.get_db)):
    """Create a new wellness activity."""
    try:
        return crud.create_wellness_activity(db, activity)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating wellness activity: {str(e)}")

@app.get("/api/activities", response_model=schemas.WellnessActivityList)
async def get_wellness_activities(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Get all wellness activities."""
    try:
        activities = crud.get_wellness_activities(db, skip=skip, limit=limit)
        return {"activities": activities, "total": len(activities)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching wellness activities: {str(e)}")

@app.put("/api/activities/{activity_id}", response_model=schemas.WellnessActivity)
async def update_wellness_activity(activity_id: int, activity: schemas.WellnessActivityCreate, db: Session = Depends(database.get_db)):
    """Update a wellness activity."""
    try:
        db_activity = crud.update_wellness_activity(db, activity_id, activity)
        if db_activity is None:
            raise HTTPException(status_code=404, detail="Wellness activity not found")
        return db_activity
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating wellness activity: {str(e)}")

@app.delete("/api/activities/{activity_id}")
async def delete_wellness_activity(activity_id: int, db: Session = Depends(database.get_db)):
    """Delete a wellness activity."""
    try:
        db_activity = crud.delete_wellness_activity(db, activity_id)
        if db_activity is None:
            raise HTTPException(status_code=404, detail="Wellness activity not found")
        return {"message": "Wellness activity deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting wellness activity: {str(e)}")

# Goal endpoints
@app.post("/api/goals", response_model=schemas.Goal)
async def create_goal(goal: schemas.GoalCreate, db: Session = Depends(database.get_db)):
    """Create a new wellness goal."""
    try:
        return crud.create_goal(db, goal)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating goal: {str(e)}")

@app.get("/api/goals", response_model=schemas.GoalList)
async def get_goals(include_completed: bool = True, skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Get all wellness goals."""
    try:
        goals = crud.get_goals(db, skip=skip, limit=limit, include_completed=include_completed)
        return {"goals": goals, "total": len(goals)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching goals: {str(e)}")

@app.get("/api/goals/{goal_id}", response_model=schemas.Goal)
async def get_goal(goal_id: int, db: Session = Depends(database.get_db)):
    """Get a specific goal."""
    try:
        goal = crud.get_goal_by_id(db, goal_id)
        if goal is None:
            raise HTTPException(status_code=404, detail="Goal not found")
        return goal
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching goal: {str(e)}")

@app.put("/api/goals/{goal_id}/progress")
async def update_goal_progress(goal_id: int, current_value: float, db: Session = Depends(database.get_db)):
    """Update goal progress."""
    try:
        goal = crud.update_goal(db, goal_id, {"current_value": current_value})
        if goal is None:
            raise HTTPException(status_code=404, detail="Goal not found")
        return {"message": "Goal progress updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating goal progress: {str(e)}")

@app.post("/api/goals/{goal_id}/complete")
async def complete_goal(goal_id: int, db: Session = Depends(database.get_db)):
    """Mark goal as completed."""
    try:
        goal = crud.complete_goal(db, goal_id)
        if goal is None:
            raise HTTPException(status_code=404, detail="Goal not found")
        return {"message": "Goal completed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error completing goal: {str(e)}")

@app.delete("/api/goals/{goal_id}")
async def delete_goal(goal_id: int, db: Session = Depends(database.get_db)):
    """Delete a goal."""
    try:
        db_goal = crud.delete_goal(db, goal_id)
        if db_goal is None:
            raise HTTPException(status_code=404, detail="Goal not found")
        return {"message": "Goal deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting goal: {str(e)}")
