const API_BASE = window.location.origin;

// Tab management
function showTab(tabName) {
    try {
        document.querySelectorAll('.nav-tab').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-panel').forEach(content => content.classList.remove('active'));

        const tabButton = document.querySelector(`[onclick="showTab('${tabName}')"]`);
        const tabContent = document.getElementById(`${tabName}-tab`);
        
        if (tabButton) tabButton.classList.add('active');
        if (tabContent) tabContent.classList.add('active');
    } catch (error) {
        console.error('Error switching tab:', error);
    }
}

// Message display
function showMessage(message, type = 'success') {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${type}`;
    msgDiv.textContent = message;

    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.insertBefore(msgDiv, mainContent.firstChild);
        setTimeout(() => msgDiv.remove(), 5000);
    }
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
    console.log('showMoodForm called');
    const form = document.getElementById('mood-form');
    const btn = document.getElementById('add-mood-btn');
    if (form) {
        form.classList.remove('hidden');
        console.log('Mood form shown');
    } else {
        console.error('Mood form not found');
    }
    if (btn) {
        btn.classList.add('hidden');
    }
}

function hideMoodForm() {
    console.log('hideMoodForm called');
    const form = document.getElementById('mood-form');
    const btn = document.getElementById('add-mood-btn');
    const formElement = document.getElementById('create-mood-form');
    if (form) form.classList.add('hidden');
    if (btn) btn.classList.remove('hidden');
    if (formElement) formElement.reset();
}

async function createMoodEntry(event) {
    event.preventDefault();

    const moodLevelEl = document.getElementById('mood-level');
    const energyLevelEl = document.getElementById('energy-level');
    const stressLevelEl = document.getElementById('stress-level');
    const sleepHoursEl = document.getElementById('sleep-hours');
    const notesEl = document.getElementById('mood-notes');

    const moodLevel = parseInt(moodLevelEl.value);
    const energyLevel = energyLevelEl.value ? parseInt(energyLevelEl.value) : null;
    const stressLevel = stressLevelEl.value ? parseInt(stressLevelEl.value) : null;
    const sleepHours = sleepHoursEl.value ? parseFloat(sleepHoursEl.value) : null;
    const notes = notesEl.value.trim() || null;

    const moodData = {
        mood_level: moodLevel,
        energy_level: energyLevel,
        stress_level: stressLevel,
        sleep_hours: sleepHours,
        notes: notes
    };

    // Validate required fields
    if (!moodData.mood_level || moodData.mood_level < 1 || moodData.mood_level > 10) {
        showMessage('Mood level must be between 1 and 10', 'error');
        return;
    }

    try {
        console.log('Sending mood data:', moodData);
        
        const response = await fetch(`${API_BASE}/api/mood`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(moodData)
        });

        let data;
        try {
            data = await response.json();
        } catch (jsonError) {
            console.error('Failed to parse response:', jsonError);
            const text = await response.text();
            console.error('Response text:', text);
            throw new Error(`Server error: ${response.status} ${response.statusText}`);
        }

        if (!response.ok) {
            const errorMsg = data.detail || data.message || `Failed to save mood entry (${response.status})`;
            console.error('Error response:', data);
            throw new Error(errorMsg);
        }

        console.log('Mood entry saved successfully:', data);
        showMessage('Mood entry saved successfully!');
        hideMoodForm();
        loadMoodEntries();
        loadDashboardStats();
    } catch (error) {
        console.error('Error creating mood entry:', error);
        showMessage(error.message || 'Failed to save mood entry. Please check the console for details.', 'error');
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
            entryDiv.className = 'list-item';

            const moodEmoji = entry.mood_level >= 7 ? '😊' : entry.mood_level >= 4 ? '😐' : '😢';
            const energyEmoji = entry.energy_level >= 7 ? '⚡' : entry.energy_level >= 4 ? '🔋' : '😴';
            const stressEmoji = entry.stress_level >= 7 ? '😰' : entry.stress_level >= 4 ? '😟' : '😌';

            entryDiv.innerHTML = `
                <div class="item-header">
                    <div class="item-date">${new Date(entry.date).toLocaleDateString()}</div>
                </div>
                <div class="item-meta">
                    <div class="meta-item">
                        <span class="meta-badge primary">${moodEmoji} Mood: ${entry.mood_level}/10</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-badge primary">${energyEmoji} Energy: ${entry.energy_level}/10</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-badge ${entry.stress_level >= 7 ? 'warning' : 'success'}">${stressEmoji} Stress: ${entry.stress_level}/10</span>
                    </div>
                    ${entry.sleep_hours ? `<div class="meta-item"><span class="meta-badge">💤 Sleep: ${entry.sleep_hours}h</span></div>` : ''}
                </div>
                ${entry.notes ? `<div style="margin-top: 1rem; color: var(--text-secondary);">${entry.notes}</div>` : ''}
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
    console.log('showJournalForm called');
    const form = document.getElementById('journal-form');
    const btn = document.getElementById('add-journal-btn');
    if (form) {
        form.classList.remove('hidden');
        console.log('Journal form shown');
    } else {
        console.error('Journal form not found');
    }
    if (btn) btn.classList.add('hidden');
}

function hideJournalForm() {
    console.log('hideJournalForm called');
    const form = document.getElementById('journal-form');
    const btn = document.getElementById('add-journal-btn');
    const formElement = document.getElementById('create-journal-form');
    if (form) form.classList.add('hidden');
    if (btn) btn.classList.remove('hidden');
    if (formElement) formElement.reset();
}

async function createJournalEntry(event) {
    event.preventDefault();

    const journalData = {
        title: document.getElementById('journal-title').value.trim() || null,
        content: document.getElementById('journal-content').value.trim(),
        mood_before: document.getElementById('mood-before').value ? parseInt(document.getElementById('mood-before').value) : null,
        mood_after: document.getElementById('mood-after').value ? parseInt(document.getElementById('mood-after').value) : null,
        tags: document.getElementById('journal-tags').value.trim() || null
    };

    // Validate required fields
    if (!journalData.content || journalData.content.length === 0) {
        showMessage('Journal content is required', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/journal`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(journalData)
        });

        const data = await response.json();

        if (!response.ok) {
            const errorMsg = data.detail || data.message || 'Failed to save journal entry';
            console.error('Error response:', data);
            throw new Error(errorMsg);
        }

        showMessage('Journal entry saved successfully!');
        hideJournalForm();
        loadJournalEntries();
        loadDashboardStats();
    } catch (error) {
        console.error('Error creating journal entry:', error);
        showMessage(error.message || 'Failed to save journal entry. Please try again.', 'error');
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
            entryDiv.className = 'list-item';

            entryDiv.innerHTML = `
                <div class="item-header">
                    <div class="item-date">${new Date(entry.date).toLocaleDateString()}</div>
                </div>
                ${entry.title ? `<div style="font-size: 1.125rem; font-weight: 600; margin-bottom: 0.75rem; color: var(--text-primary);">${entry.title}</div>` : ''}
                <div style="color: var(--text-secondary); line-height: 1.6; margin-bottom: 1rem;">${entry.content}</div>
                ${entry.mood_before || entry.mood_after ?
                    `<div class="item-meta"><div class="meta-item"><span class="meta-badge primary">Mood: ${entry.mood_before || '?'} → ${entry.mood_after || '?'}</span></div></div>` : ''}
                ${entry.tags ? `<div class="item-meta" style="margin-top: 0.5rem;"><div class="meta-item"><span class="meta-badge">Tags: ${entry.tags}</span></div></div>` : ''}
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
    console.log('showActivityForm called');
    const form = document.getElementById('activity-form');
    const btn = document.getElementById('add-activity-btn');
    if (form) {
        form.classList.remove('hidden');
        console.log('Activity form shown');
    } else {
        console.error('Activity form not found');
    }
    if (btn) btn.classList.add('hidden');
}

function hideActivityForm() {
    console.log('hideActivityForm called');
    const form = document.getElementById('activity-form');
    const btn = document.getElementById('add-activity-btn');
    const formElement = document.getElementById('create-activity-form');
    if (form) form.classList.add('hidden');
    if (btn) btn.classList.remove('hidden');
    if (formElement) formElement.reset();
}

async function createActivity(event) {
    event.preventDefault();

    const activityData = {
        activity_type: document.getElementById('activity-type').value,
        duration_minutes: document.getElementById('activity-duration').value ? parseInt(document.getElementById('activity-duration').value) : null,
        description: document.getElementById('activity-description').value.trim() || null,
        mood_impact: document.getElementById('mood-impact').value ? parseInt(document.getElementById('mood-impact').value) : null,
        notes: document.getElementById('activity-notes').value.trim() || null
    };

    // Validate required fields
    if (!activityData.activity_type) {
        showMessage('Activity type is required', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/activities`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(activityData)
        });

        const data = await response.json();

        if (!response.ok) {
            const errorMsg = data.detail || data.message || 'Failed to log activity';
            console.error('Error response:', data);
            throw new Error(errorMsg);
        }

        showMessage('Activity logged successfully!');
        hideActivityForm();
        loadActivities();
        loadDashboardStats();
    } catch (error) {
        console.error('Error creating activity:', error);
        showMessage(error.message || 'Failed to log activity. Please try again.', 'error');
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
            activityDiv.className = 'list-item';

            const typeEmoji = activity.activity_type === 'meditation' ? '🧘' :
                            activity.activity_type === 'exercise' ? '💪' :
                            activity.activity_type === 'reading' ? '📚' : '✨';

            const moodImpactClass = activity.mood_impact > 0 ? 'success' : activity.mood_impact < 0 ? 'warning' : '';
            
            activityDiv.innerHTML = `
                <div class="item-header">
                    <div style="font-weight: 600; color: var(--text-primary);">${typeEmoji} ${activity.activity_type.charAt(0).toUpperCase() + activity.activity_type.slice(1).replace('_', ' ')}</div>
                    <div class="item-date">${new Date(activity.date).toLocaleDateString()}</div>
                </div>
                <div class="item-meta">
                    ${activity.duration_minutes ? `<div class="meta-item"><span class="meta-badge">⏱ ${activity.duration_minutes} min</span></div>` : ''}
                    ${activity.mood_impact ? `<div class="meta-item"><span class="meta-badge ${moodImpactClass}">${activity.mood_impact > 0 ? '+' : ''}${activity.mood_impact} Impact</span></div>` : ''}
                </div>
                ${activity.description ? `<div style="margin-top: 1rem; color: var(--text-secondary);">${activity.description}</div>` : ''}
                ${activity.notes ? `<div style="margin-top: 0.75rem; color: var(--text-muted); font-size: 0.875rem;">${activity.notes}</div>` : ''}
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
    console.log('showGoalForm called');
    const form = document.getElementById('goal-form');
    const btn = document.getElementById('add-goal-btn');
    if (form) {
        form.classList.remove('hidden');
        console.log('Goal form shown');
    } else {
        console.error('Goal form not found');
    }
    if (btn) btn.classList.add('hidden');
}

function hideGoalForm() {
    console.log('hideGoalForm called');
    const form = document.getElementById('goal-form');
    const btn = document.getElementById('add-goal-btn');
    const formElement = document.getElementById('create-goal-form');
    if (form) form.classList.add('hidden');
    if (btn) btn.classList.remove('hidden');
    if (formElement) formElement.reset();
}

async function createGoal(event) {
    event.preventDefault();

    const goalData = {
        title: document.getElementById('goal-title').value.trim(),
        description: document.getElementById('goal-description').value.trim() || null,
        goal_type: document.getElementById('goal-type').value,
        target_value: document.getElementById('target-value').value ? parseFloat(document.getElementById('target-value').value) : null,
        target_date: document.getElementById('target-date').value || null
    };

    // Validate required fields
    if (!goalData.title || goalData.title.length === 0) {
        showMessage('Goal title is required', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/goals`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(goalData)
        });

        const data = await response.json();

        if (!response.ok) {
            const errorMsg = data.detail || data.message || 'Failed to create goal';
            console.error('Error response:', data);
            throw new Error(errorMsg);
        }

        showMessage('Goal created successfully!');
        hideGoalForm();
        loadGoals();
        loadDashboardStats();
    } catch (error) {
        console.error('Error creating goal:', error);
        showMessage(error.message || 'Failed to create goal. Please try again.', 'error');
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
            goalDiv.className = 'list-item';

            const progressPercent = goal.target_value ? Math.min((goal.current_value / goal.target_value) * 100, 100) : 0;
            const statusEmoji = goal.is_completed ? '✅' : progressPercent >= 75 ? '🚀' : '🎯';

            goalDiv.innerHTML = `
                <div class="item-header">
                    <div style="font-weight: 600; color: var(--text-primary); font-size: 1.125rem;">${statusEmoji} ${goal.title}</div>
                    <div class="meta-badge ${goal.is_completed ? 'success' : 'primary'}">${goal.is_completed ? 'Completed' : 'Active'}</div>
                </div>
                ${goal.description ? `<div style="margin-top: 0.75rem; color: var(--text-secondary);">${goal.description}</div>` : ''}
                <div class="item-meta" style="margin-top: 1rem;">
                    <div class="meta-item"><span class="meta-badge primary">Progress: ${goal.current_value}${goal.target_value ? ` / ${goal.target_value}` : ''}</span></div>
                    ${goal.target_date ? `<div class="meta-item"><span class="meta-badge">Target: ${new Date(goal.target_date).toLocaleDateString()}</span></div>` : ''}
                </div>
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

// Setup event listeners
function setupEventListeners() {
    try {
        // Form submissions
        const moodForm = document.getElementById('create-mood-form');
        const journalForm = document.getElementById('create-journal-form');
        const activityForm = document.getElementById('create-activity-form');
        const goalForm = document.getElementById('create-goal-form');

        if (moodForm) {
            moodForm.addEventListener('submit', createMoodEntry);
        } else {
            console.warn('Mood form not found');
        }
        
        if (journalForm) {
            journalForm.addEventListener('submit', createJournalEntry);
        } else {
            console.warn('Journal form not found');
        }
        
        if (activityForm) {
            activityForm.addEventListener('submit', createActivity);
        } else {
            console.warn('Activity form not found');
        }
        
        if (goalForm) {
            goalForm.addEventListener('submit', createGoal);
        } else {
            console.warn('Goal form not found');
        }

        // Button click handlers
        const addMoodBtn = document.getElementById('add-mood-btn');
        const addJournalBtn = document.getElementById('add-journal-btn');
        const addActivityBtn = document.getElementById('add-activity-btn');
        const addGoalBtn = document.getElementById('add-goal-btn');

        if (addMoodBtn) {
            addMoodBtn.addEventListener('click', showMoodForm);
            console.log('Mood button listener attached');
        } else {
            console.warn('Add mood button not found');
        }
        
        if (addJournalBtn) {
            addJournalBtn.addEventListener('click', showJournalForm);
            console.log('Journal button listener attached');
        } else {
            console.warn('Add journal button not found');
        }
        
        if (addActivityBtn) {
            addActivityBtn.addEventListener('click', showActivityForm);
            console.log('Activity button listener attached');
        } else {
            console.warn('Add activity button not found');
        }
        
        if (addGoalBtn) {
            addGoalBtn.addEventListener('click', showGoalForm);
            console.log('Goal button listener attached');
        } else {
            console.warn('Add goal button not found');
        }
    } catch (error) {
        console.error('Error setting up event listeners:', error);
    }
}

// Wait for DOM to be ready
(function() {
    function ready() {
        console.log('Setting up event listeners...');
        setupEventListeners();
        init();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', ready);
    } else {
        // DOM is already loaded
        ready();
    }
})();
