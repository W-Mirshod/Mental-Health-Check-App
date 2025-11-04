from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from . import database, models, schemas, crud, utils

app = FastAPI(title="Mental Health Check")

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main page."""
    return templates.TemplateResponse("index.html", {"request": request})

# Dashboard endpoints
@app.get("/api/dashboard/stats")
async def get_dashboard_stats(db: Session = Depends(database.get_db)):
    """Get dashboard statistics."""
    return crud.get_wellness_stats(db)

@app.get("/api/dashboard/trends")
async def get_mood_trends(db: Session = Depends(database.get_db)):
    """Get mood trends for the last 30 days."""
    return crud.get_mood_trends(db, 30)

@app.get("/api/dashboard/recent")
async def get_recent_activities(db: Session = Depends(database.get_db)):
    """Get recent wellness activities."""
    return crud.get_recent_activities(db, 7)

# Mood endpoints
@app.post("/api/mood", response_model=schemas.MoodEntry)
async def create_mood_entry(mood_entry: schemas.MoodEntryCreate, db: Session = Depends(database.get_db)):
    """Create or update today's mood entry."""
    return crud.create_mood_entry(db, mood_entry)

@app.get("/api/mood", response_model=schemas.MoodEntryList)
async def get_mood_entries(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Get all mood entries."""
    entries = crud.get_mood_entries(db, skip=skip, limit=limit)
    return {"entries": entries, "total": len(entries)}

@app.get("/api/mood/today")
async def get_today_mood(db: Session = Depends(database.get_db)):
    """Get today's mood entry."""
    from datetime import datetime
    entry = crud.get_mood_entry_by_date(db, datetime.now())
    return entry

@app.put("/api/mood/{entry_id}", response_model=schemas.MoodEntry)
async def update_mood_entry(entry_id: int, mood_entry: schemas.MoodEntryCreate, db: Session = Depends(database.get_db)):
    """Update a mood entry."""
    db_entry = crud.update_mood_entry(db, entry_id, mood_entry)
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Mood entry not found")
    return db_entry

@app.delete("/api/mood/{entry_id}")
async def delete_mood_entry(entry_id: int, db: Session = Depends(database.get_db)):
    """Delete a mood entry."""
    db_entry = crud.delete_mood_entry(db, entry_id)
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Mood entry not found")
    return {"message": "Mood entry deleted successfully"}

# Journal endpoints
@app.post("/api/journal", response_model=schemas.JournalEntry)
async def create_journal_entry(journal_entry: schemas.JournalEntryCreate, db: Session = Depends(database.get_db)):
    """Create a new journal entry."""
    return crud.create_journal_entry(db, journal_entry)

@app.get("/api/journal", response_model=schemas.JournalEntryList)
async def get_journal_entries(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Get all journal entries."""
    entries = crud.get_journal_entries(db, skip=skip, limit=limit)
    return {"entries": entries, "total": len(entries)}

@app.get("/api/journal/{entry_id}", response_model=schemas.JournalEntry)
async def get_journal_entry(entry_id: int, db: Session = Depends(database.get_db)):
    """Get a specific journal entry."""
    entry = crud.get_journal_entry_by_id(db, entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    return entry

@app.put("/api/journal/{entry_id}", response_model=schemas.JournalEntry)
async def update_journal_entry(entry_id: int, journal_entry: schemas.JournalEntryCreate, db: Session = Depends(database.get_db)):
    """Update a journal entry."""
    db_entry = crud.update_journal_entry(db, entry_id, journal_entry)
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    return db_entry

@app.delete("/api/journal/{entry_id}")
async def delete_journal_entry(entry_id: int, db: Session = Depends(database.get_db)):
    """Delete a journal entry."""
    db_entry = crud.delete_journal_entry(db, entry_id)
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    return {"message": "Journal entry deleted successfully"}

# Wellness Activity endpoints
@app.post("/api/activities", response_model=schemas.WellnessActivity)
async def create_wellness_activity(activity: schemas.WellnessActivityCreate, db: Session = Depends(database.get_db)):
    """Create a new wellness activity."""
    return crud.create_wellness_activity(db, activity)

@app.get("/api/activities", response_model=schemas.WellnessActivityList)
async def get_wellness_activities(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Get all wellness activities."""
    activities = crud.get_wellness_activities(db, skip=skip, limit=limit)
    return {"activities": activities, "total": len(activities)}

@app.put("/api/activities/{activity_id}", response_model=schemas.WellnessActivity)
async def update_wellness_activity(activity_id: int, activity: schemas.WellnessActivityCreate, db: Session = Depends(database.get_db)):
    """Update a wellness activity."""
    db_activity = crud.update_wellness_activity(db, activity_id, activity)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Wellness activity not found")
    return db_activity

@app.delete("/api/activities/{activity_id}")
async def delete_wellness_activity(activity_id: int, db: Session = Depends(database.get_db)):
    """Delete a wellness activity."""
    db_activity = crud.delete_wellness_activity(db, activity_id)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Wellness activity not found")
    return {"message": "Wellness activity deleted successfully"}

# Goal endpoints
@app.post("/api/goals", response_model=schemas.Goal)
async def create_goal(goal: schemas.GoalCreate, db: Session = Depends(database.get_db)):
    """Create a new wellness goal."""
    return crud.create_goal(db, goal)

@app.get("/api/goals", response_model=schemas.GoalList)
async def get_goals(include_completed: bool = True, skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Get all wellness goals."""
    goals = crud.get_goals(db, skip=skip, limit=limit, include_completed=include_completed)
    return {"goals": goals, "total": len(goals)}

@app.get("/api/goals/{goal_id}", response_model=schemas.Goal)
async def get_goal(goal_id: int, db: Session = Depends(database.get_db)):
    """Get a specific goal."""
    goal = crud.get_goal_by_id(db, goal_id)
    if goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal

@app.put("/api/goals/{goal_id}/progress")
async def update_goal_progress(goal_id: int, current_value: float, db: Session = Depends(database.get_db)):
    """Update goal progress."""
    goal = crud.update_goal(db, goal_id, {"current_value": current_value})
    if goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return {"message": "Goal progress updated successfully"}

@app.post("/api/goals/{goal_id}/complete")
async def complete_goal(goal_id: int, db: Session = Depends(database.get_db)):
    """Mark goal as completed."""
    goal = crud.complete_goal(db, goal_id)
    if goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return {"message": "Goal completed successfully"}

@app.delete("/api/goals/{goal_id}")
async def delete_goal(goal_id: int, db: Session = Depends(database.get_db)):
    """Delete a goal."""
    db_goal = crud.delete_goal(db, goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return {"message": "Goal deleted successfully"}
