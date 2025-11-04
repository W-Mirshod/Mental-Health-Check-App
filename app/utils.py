from typing import Optional
from datetime import datetime

def get_mood_emoji(mood_level: int) -> str:
    """Get emoji representation of mood level."""
    if mood_level >= 9:
        return "😊"
    elif mood_level >= 7:
        return "🙂"
    elif mood_level >= 5:
        return "😐"
    elif mood_level >= 3:
        return "😕"
    else:
        return "😢"

def get_energy_emoji(energy_level: int) -> str:
    """Get emoji representation of energy level."""
    if energy_level >= 8:
        return "⚡"
    elif energy_level >= 6:
        return "🔋"
    elif energy_level >= 4:
        return "🪫"
    else:
        return "😴"

def get_stress_emoji(stress_level: int) -> str:
    """Get emoji representation of stress level."""
    if stress_level >= 8:
        return "😰"
    elif stress_level >= 6:
        return "😟"
    elif stress_level >= 4:
        return "😌"
    else:
        return "😊"

def get_activity_emoji(activity_type: str) -> str:
    """Get emoji for wellness activity type."""
    activity_emojis = {
        "meditation": "🧘",
        "exercise": "💪",
        "reading": "📚",
        "social": "👥",
        "music": "🎵",
        "art": "🎨",
        "nature": "🌳",
        "sleep": "😴",
        "gratitude": "🙏",
        "therapy": "💬"
    }
    return activity_emojis.get(activity_type.lower(), "✨")

def format_mood_description(mood_level: int) -> str:
    """Get descriptive text for mood level."""
    if mood_level >= 9:
        return "Excellent"
    elif mood_level >= 7:
        return "Good"
    elif mood_level >= 5:
        return "Okay"
    elif mood_level >= 3:
        return "Low"
    else:
        return "Very Low"

def calculate_mood_change(mood_before: Optional[int], mood_after: Optional[int]) -> Optional[str]:
    """Calculate and describe mood change."""
    if not mood_before or not mood_after:
        return None

    change = mood_after - mood_before
    if change > 1:
        return f"Improved by {change} points"
    elif change == 1:
        return "Slightly improved"
    elif change == 0:
        return "No change"
    elif change == -1:
        return "Slightly decreased"
    else:
        return f"Decreased by {abs(change)} points"

def get_weekly_mood_average(mood_entries) -> Optional[float]:
    """Calculate average mood for the week."""
    if not mood_entries:
        return None

    # Get entries from the last 7 days
    week_ago = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = week_ago.replace(day=week_ago.day - 7)

    weekly_entries = [entry for entry in mood_entries if entry.date >= week_ago]

    if not weekly_entries:
        return None

    moods = [entry.mood_level for entry in weekly_entries if entry.mood_level]
    return sum(moods) / len(moods) if moods else None

def get_mood_streak(mood_entries, target_mood: int = 5) -> int:
    """Calculate current streak of moods at or above target."""
    if not mood_entries:
        return 0

    streak = 0
    for entry in sorted(mood_entries, key=lambda x: x.date, reverse=True):
        if entry.mood_level and entry.mood_level >= target_mood:
            streak += 1
        else:
            break

    return streak

def parse_tags(tags_string: Optional[str]) -> list:
    """Parse comma-separated tags string into list."""
    if not tags_string:
        return []
    return [tag.strip() for tag in tags_string.split(',') if tag.strip()]

def format_tags(tags_list: list) -> str:
    """Format tags list into comma-separated string."""
    return ', '.join(tags_list)

def get_goal_progress_percentage(current: float, target: float) -> float:
    """Calculate goal progress percentage."""
    if target <= 0:
        return 100.0 if current >= target else 0.0
    return min((current / target) * 100, 100.0)

def get_goal_status_emoji(is_completed: bool, progress_percentage: float) -> str:
    """Get emoji for goal status."""
    if is_completed:
        return "✅"
    elif progress_percentage >= 75:
        return "🚀"
    elif progress_percentage >= 50:
        return "📈"
    elif progress_percentage >= 25:
        return "🔄"
    else:
        return "🎯"
