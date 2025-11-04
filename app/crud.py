from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from . import models, schemas
from typing import List
from datetime import datetime, timedelta

# Mood Entry CRUD
def create_mood_entry(db: Session, mood_entry: schemas.MoodEntryCreate):
    # Check if entry already exists for today
    today = datetime.now().date()
    existing = db.query(models.MoodEntry).filter(
        func.date(models.MoodEntry.date) == today
    ).first()

    if existing:
        # Update existing entry
        for key, value in mood_entry.model_dump().items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return existing

    # Create new entry
    db_entry = models.MoodEntry(**mood_entry.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_mood_entries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MoodEntry).order_by(desc(models.MoodEntry.date)).offset(skip).limit(limit).all()

def get_mood_entry_by_date(db: Session, date: datetime):
    return db.query(models.MoodEntry).filter(
        func.date(models.MoodEntry.date) == date.date()
    ).first()

def update_mood_entry(db: Session, entry_id: int, entry_update: schemas.MoodEntryCreate):
    db_entry = db.query(models.MoodEntry).filter(models.MoodEntry.id == entry_id).first()
    if db_entry:
        for key, value in entry_update.model_dump().items():
            setattr(db_entry, key, value)
        db.commit()
        db.refresh(db_entry)
    return db_entry

def delete_mood_entry(db: Session, entry_id: int):
    db_entry = db.query(models.MoodEntry).filter(models.MoodEntry.id == entry_id).first()
    if db_entry:
        db.delete(db_entry)
        db.commit()
    return db_entry

# Journal Entry CRUD
def create_journal_entry(db: Session, journal_entry: schemas.JournalEntryCreate):
    db_entry = models.JournalEntry(**journal_entry.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_journal_entries(db: Session, skip: int = 0, limit: int = 100, include_private: bool = True):
    query = db.query(models.JournalEntry)
    if not include_private:
        query = query.filter(models.JournalEntry.is_private == False)
    return query.order_by(desc(models.JournalEntry.date)).offset(skip).limit(limit).all()

def get_journal_entry_by_id(db: Session, entry_id: int):
    return db.query(models.JournalEntry).filter(models.JournalEntry.id == entry_id).first()

def update_journal_entry(db: Session, entry_id: int, entry_update: schemas.JournalEntryCreate):
    db_entry = db.query(models.JournalEntry).filter(models.JournalEntry.id == entry_id).first()
    if db_entry:
        for key, value in entry_update.model_dump().items():
            setattr(db_entry, key, value)
        db.commit()
        db.refresh(db_entry)
    return db_entry

def delete_journal_entry(db: Session, entry_id: int):
    db_entry = db.query(models.JournalEntry).filter(models.JournalEntry.id == entry_id).first()
    if db_entry:
        db.delete(db_entry)
        db.commit()
    return db_entry

# Wellness Activity CRUD
def create_wellness_activity(db: Session, activity: schemas.WellnessActivityCreate):
    db_activity = models.WellnessActivity(**activity.model_dump())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def get_wellness_activities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WellnessActivity).order_by(desc(models.WellnessActivity.date)).offset(skip).limit(limit).all()

def get_activities_by_type(db: Session, activity_type: str, skip: int = 0, limit: int = 100):
    return db.query(models.WellnessActivity).filter(
        models.WellnessActivity.activity_type == activity_type
    ).order_by(desc(models.WellnessActivity.date)).offset(skip).limit(limit).all()

def update_wellness_activity(db: Session, activity_id: int, activity_update: schemas.WellnessActivityCreate):
    db_activity = db.query(models.WellnessActivity).filter(models.WellnessActivity.id == activity_id).first()
    if db_activity:
        for key, value in activity_update.model_dump().items():
            setattr(db_activity, key, value)
        db.commit()
        db.refresh(db_activity)
    return db_activity

def delete_wellness_activity(db: Session, activity_id: int):
    db_activity = db.query(models.WellnessActivity).filter(models.WellnessActivity.id == activity_id).first()
    if db_activity:
        db.delete(db_activity)
        db.commit()
    return db_activity

# Goal CRUD
def create_goal(db: Session, goal: schemas.GoalCreate):
    db_goal = models.Goal(**goal.model_dump())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def get_goals(db: Session, skip: int = 0, limit: int = 100, include_completed: bool = True):
    query = db.query(models.Goal)
    if not include_completed:
        query = query.filter(models.Goal.is_completed == False)
    return query.order_by(desc(models.Goal.created_at)).offset(skip).limit(limit).all()

def get_goal_by_id(db: Session, goal_id: int):
    return db.query(models.Goal).filter(models.Goal.id == goal_id).first()

def update_goal(db: Session, goal_id: int, goal_update: dict):
    db_goal = db.query(models.Goal).filter(models.Goal.id == goal_id).first()
    if db_goal:
        for key, value in goal_update.items():
            setattr(db_goal, key, value)
        db.commit()
        db.refresh(db_goal)
    return db_goal

def complete_goal(db: Session, goal_id: int):
    return update_goal(db, goal_id, {"is_completed": True})

def delete_goal(db: Session, goal_id: int):
    db_goal = db.query(models.Goal).filter(models.Goal.id == goal_id).first()
    if db_goal:
        db.delete(db_goal)
        db.commit()
    return db_goal

# Statistics and analytics
def get_wellness_stats(db: Session) -> schemas.WellnessStats:
    """Get comprehensive wellness statistics."""

    # Mood stats
    mood_entries = db.query(models.MoodEntry).all()
    total_entries = len(mood_entries)

    avg_mood = None
    avg_energy = None
    avg_stress = None
    avg_sleep = None

    if mood_entries:
        moods = [e.mood_level for e in mood_entries if e.mood_level]
        energies = [e.energy_level for e in mood_entries if e.energy_level]
        stresses = [e.stress_level for e in mood_entries if e.stress_level]
        sleeps = [e.sleep_hours for e in mood_entries if e.sleep_hours]

        avg_mood = sum(moods) / len(moods) if moods else None
        avg_energy = sum(energies) / len(energies) if energies else None
        avg_stress = sum(stresses) / len(stresses) if stresses else None
        avg_sleep = sum(sleeps) / len(sleeps) if sleeps else None

    # Journal and activity counts
    total_journal_entries = db.query(func.count(models.JournalEntry.id)).scalar()
    total_activities = db.query(func.count(models.WellnessActivity.id)).scalar()

    # Goals
    completed_goals = db.query(func.count(models.Goal.id)).filter(models.Goal.is_completed == True).scalar()
    active_goals = db.query(func.count(models.Goal.id)).filter(models.Goal.is_completed == False).scalar()

    return schemas.WellnessStats(
        total_entries=total_entries,
        avg_mood=round(avg_mood, 1) if avg_mood else None,
        avg_energy=round(avg_energy, 1) if avg_energy else None,
        avg_stress=round(avg_stress, 1) if avg_stress else None,
        avg_sleep=round(avg_sleep, 1) if avg_sleep else None,
        total_journal_entries=total_journal_entries,
        total_activities=total_activities,
        completed_goals=completed_goals,
        active_goals=active_goals
    )

def get_mood_trends(db: Session, days: int = 30):
    """Get mood trends for the last N days."""
    start_date = datetime.now() - timedelta(days=days)

    entries = db.query(models.MoodEntry).filter(
        models.MoodEntry.date >= start_date
    ).order_by(models.MoodEntry.date).all()

    return [{
        "date": entry.date.strftime("%Y-%m-%d"),
        "mood": entry.mood_level,
        "energy": entry.energy_level,
        "stress": entry.stress_level,
        "sleep": entry.sleep_hours
    } for entry in entries]

def get_recent_activities(db: Session, days: int = 7):
    """Get recent wellness activities."""
    start_date = datetime.now() - timedelta(days=days)

    return db.query(models.WellnessActivity).filter(
        models.WellnessActivity.date >= start_date
    ).order_by(desc(models.WellnessActivity.date)).limit(10).all()
