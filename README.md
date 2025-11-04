# 🧠 Mental Health Check

A comprehensive web application for tracking daily mood, journaling thoughts, logging wellness activities, and setting personal goals.

## Features

- **Daily Mood Tracking**: Log mood, energy, stress levels, and sleep hours
- **Journal**: Write private journal entries with mood tracking before/after
- **Wellness Activities**: Track meditation, exercise, social activities, and their mood impact
- **Goal Setting**: Set and track wellness goals with progress monitoring
- **Statistics Dashboard**: View mood trends and activity summaries

## Tech Stack

- **Backend**: FastAPI with SQLAlchemy
- **Frontend**: Vanilla JavaScript with modern CSS
- **Database**: SQLite

## Quick Start

1. **Navigate to the app**:
   ```bash
   cd "Mental Health Check App"
   ```

2. **Start the application**:
   ```bash
   docker compose up -d
   ```

3. **Open your browser**:
   Navigate to `http://localhost:8004`

## Production Features

- **Modern UI**: Beautiful gradient design with smooth animations and responsive layout
- **Error Handling**: Comprehensive error handling throughout the application
- **CORS Support**: Configured for cross-origin requests
- **Health Check**: `/health` endpoint for monitoring
- **Security**: Non-root user in Docker container
- **Database**: Auto-initialization with proper directory handling

## Usage

### Mood Tracking
- Daily mood check-in with sliders for mood, energy, and stress levels
- Sleep hours tracking
- Optional notes about the day

### Journaling
- Write private journal entries
- Track mood before and after writing
- Add tags for organization
- Optional titles for entries

### Activity Logging
- Log wellness activities (meditation, exercise, reading, etc.)
- Track duration and mood impact
- Add descriptions and notes

### Goal Setting
- Set personal wellness goals
- Track progress with target values
- Set completion dates

## API Endpoints

### Mood
- `POST /api/mood` - Create/update daily mood entry
- `GET /api/mood` - List mood entries
- `PUT /api/mood/{id}` - Update mood entry
- `DELETE /api/mood/{id}` - Delete mood entry

### Journal
- `POST /api/journal` - Create journal entry
- `GET /api/journal` - List journal entries
- `PUT /api/journal/{id}` - Update journal entry
- `DELETE /api/journal/{id}` - Delete journal entry

### Activities
- `POST /api/activities` - Log wellness activity
- `GET /api/activities` - List activities
- `PUT /api/activities/{id}` - Update activity
- `DELETE /api/activities/{id}` - Delete activity

### Goals
- `POST /api/goals` - Create wellness goal
- `GET /api/goals` - List goals
- `PUT /api/goals/{id}/progress` - Update goal progress
- `POST /api/goals/{id}/complete` - Mark goal complete
- `DELETE /api/goals/{id}` - Delete goal

### Dashboard
- `GET /api/dashboard/stats` - Get wellness statistics
- `GET /api/dashboard/trends` - Get mood trends
- `GET /api/dashboard/recent` - Get recent activities
