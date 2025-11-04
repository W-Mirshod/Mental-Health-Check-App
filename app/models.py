from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class MoodEntry(Base):
    __tablename__ = "mood_entries"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=func.now())
    mood_level = Column(Integer)  # 1-10 scale
    energy_level = Column(Integer, nullable=True)  # 1-10 scale
    stress_level = Column(Integer, nullable=True)  # 1-10 scale
    sleep_hours = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=func.now())
    title = Column(String, nullable=True)
    content = Column(Text)
    mood_before = Column(Integer, nullable=True)  # 1-10 scale
    mood_after = Column(Integer, nullable=True)  # 1-10 scale
    tags = Column(String, nullable=True)  # comma-separated tags
    is_private = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class WellnessActivity(Base):
    __tablename__ = "wellness_activities"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=func.now())
    activity_type = Column(String)  # meditation, exercise, reading, social, etc.
    duration_minutes = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    mood_impact = Column(Integer, nullable=True)  # -5 to +5 scale
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text, nullable=True)
    goal_type = Column(String)  # mood, activity, sleep, etc.
    target_value = Column(Float, nullable=True)
    current_value = Column(Float, default=0.0)
    start_date = Column(DateTime, default=func.now())
    target_date = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
