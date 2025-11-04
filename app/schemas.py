from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MoodEntryBase(BaseModel):
    mood_level: int
    energy_level: Optional[int] = None
    stress_level: Optional[int] = None
    sleep_hours: Optional[float] = None
    notes: Optional[str] = None

class MoodEntryCreate(MoodEntryBase):
    pass

class MoodEntry(MoodEntryBase):
    id: int
    date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class MoodEntryList(BaseModel):
    entries: List[MoodEntry]
    total: int

class JournalEntryBase(BaseModel):
    title: Optional[str] = None
    content: str
    mood_before: Optional[int] = None
    mood_after: Optional[int] = None
    tags: Optional[str] = None
    is_private: bool = False

class JournalEntryCreate(JournalEntryBase):
    pass

class JournalEntry(JournalEntryBase):
    id: int
    date: datetime
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class JournalEntryList(BaseModel):
    entries: List[JournalEntry]
    total: int

class WellnessActivityBase(BaseModel):
    activity_type: str
    duration_minutes: Optional[int] = None
    description: Optional[str] = None
    mood_impact: Optional[int] = None
    notes: Optional[str] = None

class WellnessActivityCreate(WellnessActivityBase):
    pass

class WellnessActivity(WellnessActivityBase):
    id: int
    date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class WellnessActivityList(BaseModel):
    activities: List[WellnessActivity]
    total: int

class GoalBase(BaseModel):
    title: str
    description: Optional[str] = None
    goal_type: str
    target_value: Optional[float] = None
    current_value: float = 0.0
    target_date: Optional[datetime] = None

class GoalCreate(GoalBase):
    pass

class Goal(GoalBase):
    id: int
    start_date: datetime
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class GoalList(BaseModel):
    goals: List[Goal]
    total: int

class WellnessStats(BaseModel):
    total_entries: int
    avg_mood: Optional[float]
    avg_energy: Optional[float]
    avg_stress: Optional[float]
    avg_sleep: Optional[float]
    total_journal_entries: int
    total_activities: int
    completed_goals: int
    active_goals: int
