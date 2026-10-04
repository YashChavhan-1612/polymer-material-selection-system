/* ============================================================
   PolySelect – Frontend Validation & Error Handling
   ============================================================ */

const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('nav-links');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });
}

document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
    });
});

/* ---------- Load materials overview ---------- */
async function loadMaterials() {
    const grid = document.getElementById('materials-grid');
    if (!grid) return;

    try {
        const response = await fetch('/api/materials');
        const data = await response.json();

        if (data.success && Array.isArray(data.materials)) {
            grid.innerHTML = '';
            data.materials.forEach(mat => {
                const card = document.createElement('a');
                card.className = 'material-card';
                card.href = `/material/${mat.id}`;
                card.innerHTML = `
                    <h3>${escapeHtml(mat.name)}</h3>
                    <p class="category">${escapeHtml(mat.category)}</p>
                    <p class="material-meta">
                        ${mat.strength} MPa · ${mat.max_temperature}°C · ${escapeHtml(mat.cost)}
                    </p>
                `;
                grid.appendChild(card);
            });
        }
    } catch (err) {
        console.error('Materials load failed');
        // Silent fail – overview is not critical
    }
}

/* ---------- Helpers ---------- */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showLoading(show) {
    const loading = document.getElementById('loading');
    const submitBtn = document.getElementById('submit-btn');
    if (loading) loading.classList.toggle('hidden', !show);
    if (submitBtn) submitBtn.disabled = show;
}

/* ---------- Form Validation ---------- */
function validateForm() {
    const application = document.getElementById('application').value.trim();
    const strength = document.getElementById('strength').value;
    const temperatureRaw = document.getElementById('temperature').value;
    const weight = document.getElementById('weight').value;
    const chemical = document.getElementById('chemical_resistance').value;
    const cost = document.getElementById('cost').value;

    const errors = [];

    if (!application) {
        errors.push('Application Type is required.');
    } else if (application.length < 2) {
        errors.push('Application Type must be at least 2 characters.');
    } else if (application.length > 150) {
        errors.push('Application Type is too long (max 150 characters).');
    }

    if (!strength) errors.push('Please select Required Strength.');
    if (!weight) errors.push('Please select Weight Requirement.');
    if (!chemical) errors.push('Please select Chemical Resistance.');
    if (!cost) errors.push('Please select Cost Preference.');

    if (temperatureRaw === '' || temperatureRaw === null) {
        errors.push('Operating Temperature is required.');
    } else {
        const temperature = Number(temperatureRaw);
        if (isNaN(temperature) || !Number.isInteger(temperature)) {
            errors.push('Operating Temperature must be a whole number (e.g. 60).');
        } else if (temperature < 0 || temperature > 400) {
            errors.push('Operating Temperature must be between 0°C and 400°C.');
        }
    }

    return {
        isValid: errors.length === 0,
        errors,
        payload: {
            application,
            strength,
            temperature: parseInt(temperatureRaw, 10),
            weight,
            chemical_resistance: chemical,
            cost
        }
    };
}

/* ---------- Form Submit ---------- */
const form = document.getElementById('recommendation-form');
const resultsDiv = document.getElementById('results');

if (form) {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const validation = validateForm();

        if (!validation.isValid) {
            showErrorState(validation.errors.join(' '));
            return;
        }

        // Clear previous results and show loading
        resultsDiv.classList.add('hidden');
        resultsDiv.innerHTML = '';
        showLoading(true);

        try {
            const response = await fetch('/api/recommend', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(validation.payload)
            });

            let data;
            try {
                data = await response.json();
            } catch {
                showErrorState('Received an invalid response from the server. Please try again.');
                showLoading(false);
                return;
            }

            showLoading(false);

            if (data.success && Array.isArray(data.recommendations) && data.recommendations.length > 0) {
                displayResults(data.recommendations);
            } else if (data.success && data.recommendations && data.recommendations.length === 0) {
                showEmptyState(data.message || 'No suitable materials found. Try adjusting your requirements.');
            } else {
                // Backend validation or other error
                showErrorState(data.message || 'Unable to generate recommendations. Please check your inputs and try again.');
            }
        } catch (err) {
            showLoading(false);
            showErrorState('Could not connect to the server. Please make sure the application is running and try again.');
        }
    });
}

/* ---------- Display Results ---------- */
function displayResults(recommendations) {
    let html = `
        <div class="results-header">
            <h2><i class="fas fa-trophy"></i> Top Recommendations</h2>
            <button type="button" class="btn btn-outline" onclick="resetForm()">
                <i class="fas fa-redo"></i> Try Again
            </button>
        </div>
        <p style="text-align:center;color:var(--text-muted);margin-bottom:1.5rem;font-size:0.95rem;">
            <i class="fas fa-check-circle" style="color:var(--secondary);"></i>
            Recommendations generated successfully
        </p>
    `;

    recommendations.forEach(rec => {
        const percentage = rec.compatibility_percentage ?? 0;

        const warningsHtml = (rec.warnings && rec.warnings.length > 0)
            ? `<div class="warnings-box">
                   <strong><i class="fas fa-exclamation-triangle"></i> Warnings</strong>
                   <ul>${rec.warnings.map(w => `<li>${escapeHtml(w)}</li>`).join('')}</ul>
               </div>`
            : '';

        const reasonsHtml = (rec.reasons || [])
            .map(r => `<li>${escapeHtml(r)}</li>`)
            .join('');

        html += `
            <div class="result-card rank-${rec.rank}">
                <div class="result-header">
                    <div>
                        <span class="rank-badge">
                            ${rec.rank === 1 ? '<i class="fas fa-crown"></i> ' : ''}Rank #${rec.rank}
                        </span>
                        <h3 class="material-name">${escapeHtml(rec.material_name)}</h3>
                        <p style="color:var(--text-muted);font-size:0.9rem;">
                            ${escapeHtml(rec.category || '')} · Score ${rec.compatibility_score}/100
                        </p>
                    </div>
                    <div class="score-area">
                        <div class="score-value">${percentage}%</div>
                        <div class="score-label">Compatibility</div>
                    </div>
                </div>
                <div class="progress-container">
                    <div class="progress-bar" style="width:${percentage}%"></div>
                </div>
                ${warningsHtml}
                <div class="result-section">
                    <div class="result-section-title"><i class="fas fa-check-circle"></i> Why this material?</div>
                    <ul class="reasons-list">${reasonsHtml}</ul>
                </div>
                <div class="result-section">
                    <div class="result-section-title"><i class="fas fa-thumbs-up"></i> Advantages</div>
                    <p style="color:var(--text-secondary);font-size:0.92rem;">${escapeHtml(rec.advantages || '—')}</p>
                </div>
                <div class="result-section">
                    <div class="result-section-title"><i class="fas fa-info-circle"></i> Limitations</div>
                    <p style="color:var(--text-secondary);font-size:0.92rem;">${escapeHtml(rec.limitations || '—')}</p>
                </div>
            </div>
        `;
    });

    resultsDiv.innerHTML = html;
    resultsDiv.classList.remove('hidden');
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/* ---------- Error / Empty States ---------- */
function showErrorState(message) {
    resultsDiv.innerHTML = `
        <div class="state-message error">
            <i class="fas fa-exclamation-circle"></i>
            <h3>Unable to get recommendations</h3>
            <p>${escapeHtml(message)}</p>
            <br>
            <button type="button" class="btn btn-primary" onclick="resetForm()">
                <i class="fas fa-redo"></i> Try Again
            </button>
        </div>
    `;
    resultsDiv.classList.remove('hidden');
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
}

function showEmptyState(message) {
    resultsDiv.innerHTML = `
        <div class="state-message empty">
            <i class="fas fa-search"></i>
            <h3>No matching materials</h3>
            <p>${escapeHtml(message || 'Try adjusting your requirements and submit again.')}</p>
            <br>
            <button type="button" class="btn btn-primary" onclick="resetForm()">
                <i class="fas fa-redo"></i> Try Again
            </button>
        </div>
    `;
    resultsDiv.classList.remove('hidden');
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
}

/* ---------- Reset ---------- */
function resetForm() {
    resultsDiv.classList.add('hidden');
    resultsDiv.innerHTML = '';
    showLoading(false);
    const formEl = document.getElementById('recommendation-form');
    if (formEl) {
        formEl.scrollIntoView({ behavior: 'smooth' });
    }
}

/* ---------- Init ---------- */
document.addEventListener('DOMContentLoaded', loadMaterials);