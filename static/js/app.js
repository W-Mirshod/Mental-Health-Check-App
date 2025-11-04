const API_BASE = window.location.origin;

// Tab management
function showTab(tabName) {
    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

    document.querySelector(`[onclick="showTab('${tabName}')"]`).classList.add('active');
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

// Message display
function showMessage(message, type = 'success') {
    const msgDiv = document.createElement('div');
    msgDiv.className = `${type}-message`;
    msgDiv.textContent = message;

    document.querySelector('.container').insertBefore(msgDiv, document.querySelector('main'));
    setTimeout(() => msgDiv.remove(), 5000);
}

// Dashboard stats
async function loadDashboardStats() {
    try {
        const response = await fetch(`${API_BASE}/api/dashboard/stats`);
        if (response.ok) {
            const stats = await response.json();
            document.getElementById('total-entries').textContent = stats.total_entries;
            document.getElementById('avg-mood').textContent = stats.avg_mood ? stats.avg_mood.toFixed(1) : 'N/A';
            document.getElementById('journal-entries').textContent = stats.total_journal_entries;
            document.getElementById('active-goals').textContent = stats.active_goals;
        }
    } catch (error) {
        console.error('Error loading dashboard stats:', error);
    }
}

// Mood tracking
function showMoodForm() {
    document.getElementById('mood-form').classList.remove('hidden');
    document.getElementById('add-mood-btn').classList.add('hidden');
}

function hideMoodForm() {
    document.getElementById('mood-form').classList.add('hidden');
    document.getElementById('add-mood-btn').classList.remove('hidden');
    document.getElementById('create-mood-form').reset();
}

async function createMoodEntry(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const moodData = {
        mood_level: parseInt(document.getElementById('mood-level').value),
        energy_level: parseInt(document.getElementById('energy-level').value),
        stress_level: parseInt(document.getElementById('stress-level').value),
        sleep_hours: document.getElementById('sleep-hours').value ? parseFloat(document.getElementById('sleep-hours').value) : null,
        notes: document.getElementById('mood-notes').value || null
    };

    try {
        const response = await fetch(`${API_BASE}/api/mood`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(moodData)
        });

        if (!response.ok) throw new Error('Failed to save mood entry');

        showMessage('Mood entry saved successfully!');
        hideMoodForm();
        loadMoodEntries();
        loadDashboardStats();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

async function loadMoodEntries() {
    const container = document.getElementById('mood-entries');
    const loading = document.getElementById('mood-loading');
    const empty = document.getElementById('mood-empty');
    const list = document.getElementById('mood-list');

    try {
        loading.classList.remove('hidden');
        empty.classList.add('hidden');
        list.classList.add('hidden');

        const response = await fetch(`${API_BASE}/api/mood`);
        if (!response.ok) throw new Error('Failed to load mood entries');

        const data = await response.json();
        loading.classList.add('hidden');

        if (data.entries.length === 0) {
            empty.classList.remove('hidden');
            return;
        }

        list.innerHTML = '';
        data.entries.forEach(entry => {
            const entryDiv = document.createElement('div');
            entryDiv.className = 'mood-entry';

            const moodEmoji = entry.mood_level >= 7 ? '😊' : entry.mood_level >= 4 ? '😐' : '😢';
            const energyEmoji = entry.energy_level >= 7 ? '⚡' : entry.energy_level >= 4 ? '🔋' : '😴';
            const stressEmoji = entry.stress_level >= 7 ? '😰' : entry.stress_level >= 4 ? '😟' : '😌';

            entryDiv.innerHTML = `
                <div class="entry-header">
                    <div class="entry-date">${new Date(entry.date).toLocaleDateString()}</div>
                    <div class="mood-levels">
                        <span class="mood-level">${moodEmoji} ${entry.mood_level}/10</span>
                        <span class="mood-level">${energyEmoji} ${entry.energy_level}/10</span>
                        <span class="mood-level">${stressEmoji} ${entry.stress_level}/10</span>
                    </div>
                </div>
                ${entry.sleep_hours ? `<div>Sleep: ${entry.sleep_hours} hours</div>` : ''}
                ${entry.notes ? `<div class="mood-notes">${entry.notes}</div>` : ''}
            `;

            list.appendChild(entryDiv);
        });

        list.classList.remove('hidden');
    } catch (error) {
        loading.classList.add('hidden');
        showMessage('Failed to load mood entries', 'error');
    }
}

// Journal functionality
function showJournalForm() {
    document.getElementById('journal-form').classList.remove('hidden');
    document.getElementById('add-journal-btn').classList.add('hidden');
}

function hideJournalForm() {
    document.getElementById('journal-form').classList.add('hidden');
    document.getElementById('add-journal-btn').classList.remove('hidden');
    document.getElementById('create-journal-form').reset();
}

async function createJournalEntry(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const journalData = {
        title: document.getElementById('journal-title').value || null,
        content: document.getElementById('journal-content').value,
        mood_before: document.getElementById('mood-before').value ? parseInt(document.getElementById('mood-before').value) : null,
        mood_after: document.getElementById('mood-after').value ? parseInt(document.getElementById('mood-after').value) : null,
        tags: document.getElementById('journal-tags').value || null
    };

    try {
        const response = await fetch(`${API_BASE}/api/journal`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(journalData)
        });

        if (!response.ok) throw new Error('Failed to save journal entry');

        showMessage('Journal entry saved successfully!');
        hideJournalForm();
        loadJournalEntries();
        loadDashboardStats();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

async function loadJournalEntries() {
    const container = document.getElementById('journal-entries');
    const loading = document.getElementById('journal-loading');
    const empty = document.getElementById('journal-empty');
    const list = document.getElementById('journal-list');

    try {
        loading.classList.remove('hidden');
        empty.classList.add('hidden');
        list.classList.add('hidden');

        const response = await fetch(`${API_BASE}/api/journal`);
        if (!response.ok) throw new Error('Failed to load journal entries');

        const data = await response.json();
        loading.classList.add('hidden');

        if (data.entries.length === 0) {
            empty.classList.remove('hidden');
            return;
        }

        list.innerHTML = '';
        data.entries.forEach(entry => {
            const entryDiv = document.createElement('div');
            entryDiv.className = 'journal-entry';

            entryDiv.innerHTML = `
                <div class="entry-header">
                    <div class="entry-date">${new Date(entry.date).toLocaleDateString()}</div>
                </div>
                ${entry.title ? `<div class="journal-title">${entry.title}</div>` : ''}
                <div class="journal-content">${entry.content}</div>
                ${entry.mood_before || entry.mood_after ?
                    `<div>Mood: ${entry.mood_before || '?'} → ${entry.mood_after || '?'}</div>` : ''}
                ${entry.tags ? `<div class="journal-tags">Tags: ${entry.tags}</div>` : ''}
            `;

            list.appendChild(entryDiv);
        });

        list.classList.remove('hidden');
    } catch (error) {
        loading.classList.add('hidden');
        showMessage('Failed to load journal entries', 'error');
    }
}

// Activities functionality
function showActivityForm() {
    document.getElementById('activity-form').classList.remove('hidden');
    document.getElementById('add-activity-btn').classList.add('hidden');
}

function hideActivityForm() {
    document.getElementById('activity-form').classList.add('hidden');
    document.getElementById('add-activity-btn').classList.remove('hidden');
    document.getElementById('create-activity-form').reset();
}

async function createActivity(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const activityData = {
        activity_type: document.getElementById('activity-type').value,
        duration_minutes: document.getElementById('activity-duration').value ? parseInt(document.getElementById('activity-duration').value) : null,
        description: document.getElementById('activity-description').value || null,
        mood_impact: document.getElementById('mood-impact').value ? parseInt(document.getElementById('mood-impact').value) : null,
        notes: document.getElementById('activity-notes').value || null
    };

    try {
        const response = await fetch(`${API_BASE}/api/activities`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(activityData)
        });

        if (!response.ok) throw new Error('Failed to log activity');

        showMessage('Activity logged successfully!');
        hideActivityForm();
        loadActivities();
        loadDashboardStats();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

async function loadActivities() {
    const container = document.getElementById('activities-list');
    const loading = document.getElementById('activities-loading');
    const empty = document.getElementById('activities-empty');
    const list = document.getElementById('activities-content');

    try {
        loading.classList.remove('hidden');
        empty.classList.add('hidden');
        list.classList.add('hidden');

        const response = await fetch(`${API_BASE}/api/activities`);
        if (!response.ok) throw new Error('Failed to load activities');

        const data = await response.json();
        loading.classList.add('hidden');

        if (data.activities.length === 0) {
            empty.classList.remove('hidden');
            return;
        }

        list.innerHTML = '';
        data.activities.forEach(activity => {
            const activityDiv = document.createElement('div');
            activityDiv.className = 'activity-item';

            const typeEmoji = activity.activity_type === 'meditation' ? '🧘' :
                            activity.activity_type === 'exercise' ? '💪' :
                            activity.activity_type === 'reading' ? '📚' : '✨';

            activityDiv.innerHTML = `
                <div class="entry-header">
                    <div class="activity-type">${typeEmoji} ${activity.activity_type.replace('_', ' ')}</div>
                    <div class="entry-date">${new Date(activity.date).toLocaleDateString()}</div>
                </div>
                ${activity.duration_minutes ? `<div>Duration: ${activity.duration_minutes} minutes</div>` : ''}
                ${activity.description ? `<div>${activity.description}</div>` : ''}
                ${activity.mood_impact ? `<div>Mood impact: ${activity.mood_impact > 0 ? '+' : ''}${activity.mood_impact}</div>` : ''}
                ${activity.notes ? `<div class="activity-notes">${activity.notes}</div>` : ''}
            `;

            list.appendChild(activityDiv);
        });

        list.classList.remove('hidden');
    } catch (error) {
        loading.classList.add('hidden');
        showMessage('Failed to load activities', 'error');
    }
}

// Goals functionality
function showGoalForm() {
    document.getElementById('goal-form').classList.remove('hidden');
    document.getElementById('add-goal-btn').classList.add('hidden');
}

function hideGoalForm() {
    document.getElementById('goal-form').classList.add('hidden');
    document.getElementById('add-goal-btn').classList.remove('hidden');
    document.getElementById('create-goal-form').reset();
}

async function createGoal(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const goalData = {
        title: document.getElementById('goal-title').value,
        description: document.getElementById('goal-description').value || null,
        goal_type: document.getElementById('goal-type').value,
        target_value: document.getElementById('target-value').value ? parseFloat(document.getElementById('target-value').value) : null,
        target_date: document.getElementById('target-date').value || null
    };

    try {
        const response = await fetch(`${API_BASE}/api/goals`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(goalData)
        });

        if (!response.ok) throw new Error('Failed to create goal');

        showMessage('Goal created successfully!');
        hideGoalForm();
        loadGoals();
        loadDashboardStats();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

async function loadGoals() {
    const container = document.getElementById('goals-list');
    const loading = document.getElementById('goals-loading');
    const empty = document.getElementById('goals-empty');
    const list = document.getElementById('goals-content');

    try {
        loading.classList.remove('hidden');
        empty.classList.add('hidden');
        list.classList.add('hidden');

        const response = await fetch(`${API_BASE}/api/goals`);
        if (!response.ok) throw new Error('Failed to load goals');

        const data = await response.json();
        loading.classList.add('hidden');

        if (data.goals.length === 0) {
            empty.classList.remove('hidden');
            return;
        }

        list.innerHTML = '';
        data.goals.forEach(goal => {
            const goalDiv = document.createElement('div');
            goalDiv.className = 'goal-item';

            const progressPercent = goal.target_value ? Math.min((goal.current_value / goal.target_value) * 100, 100) : 0;
            const statusEmoji = goal.is_completed ? '✅' : progressPercent >= 75 ? '🚀' : '🎯';

            goalDiv.innerHTML = `
                <div class="entry-header">
                    <div class="goal-title">${statusEmoji} ${goal.title}</div>
                    <div class="entry-date">${goal.is_completed ? 'Completed' : 'Active'}</div>
                </div>
                ${goal.description ? `<div>${goal.description}</div>` : ''}
                <div>Progress: ${goal.current_value}${goal.target_value ? ` / ${goal.target_value}` : ''}</div>
                ${goal.target_date ? `<div>Target: ${new Date(goal.target_date).toLocaleDateString()}</div>` : ''}
            `;

            list.appendChild(goalDiv);
        });

        list.classList.remove('hidden');
    } catch (error) {
        loading.classList.add('hidden');
        showMessage('Failed to load goals', 'error');
    }
}

// Range input updates
document.addEventListener('input', function(e) {
    if (e.target.type === 'range') {
        const displayId = e.target.id.replace('-level', '-display');
        const displayEl = document.getElementById(displayId);
        if (displayEl) {
            displayEl.textContent = e.target.value;
        }
    }
});

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Form submissions
    document.getElementById('create-mood-form').addEventListener('submit', createMoodEntry);
    document.getElementById('create-journal-form').addEventListener('submit', createJournalEntry);
    document.getElementById('create-activity-form').addEventListener('submit', createActivity);
    document.getElementById('create-goal-form').addEventListener('submit', createGoal);

    // Button click handlers
    document.getElementById('add-mood-btn').addEventListener('click', showMoodForm);
    document.getElementById('add-journal-btn').addEventListener('click', showJournalForm);
    document.getElementById('add-activity-btn').addEventListener('click', showActivityForm);
    document.getElementById('add-goal-btn').addEventListener('click', showGoalForm);

    // Initialize the app
    init();
});

// Initialize the app
async function init() {
    try {
        await Promise.all([
            loadDashboardStats(),
            loadMoodEntries(),
            loadJournalEntries(),
            loadActivities(),
            loadGoals()
        ]);

        // Set default tab
        showTab('mood');
    } catch (error) {
        console.error('Error initializing app:', error);
        showMessage('Failed to load application. Please refresh the page.', 'error');
    }
}
