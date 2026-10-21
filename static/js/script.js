// ================== API CONFIGURATION ==================
// In single-origin deployments (Flask serving HTML), API_BASE_URL is empty ('').
// In decoupled architectures (e.g. Vercel frontend calling Render backend),
// window.API_BASE_URL can be set to the backend's public URL.
const API_BASE_URL = window.API_BASE_URL || '';

/* ============================================================
   PolySelect – Navigation & Mobile Menu
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

/* ============================================================
   Material Cards & Rendering Helpers
   ============================================================ */

let allMaterialsCache = [];

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function renderMaterialCard(mat) {
    const card = document.createElement('a');
    card.className = 'material-card';
    card.href = `/material/${encodeURIComponent(mat.id)}`;
    card.innerHTML = `
        <span style="display:inline-block;font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.04em;color:var(--secondary);margin-bottom:0.25rem;">
            ${escapeHtml(mat.category)}
        </span>
        <h3 style="margin-bottom:0.4rem;font-size:1.15rem;">${escapeHtml(mat.name)}</h3>
        <p class="material-meta" style="font-size:0.85rem;color:var(--text-muted);">
            ${escapeHtml(String(mat.strength))} MPa · ${escapeHtml(String(mat.max_temperature))}°C · ${escapeHtml(mat.cost)}
        </p>
    `;
    return card;
}

/* ---------- Load Featured Materials (Home Page: 5 materials) ---------- */
async function loadHomeFeaturedMaterials() {
    const grid = document.getElementById('materials-grid');
    if (!grid) return;

    try {
        const response = await fetch(`${API_BASE_URL}/api/materials`);
        const data = await response.json();

        if (data.success && Array.isArray(data.materials)) {
            grid.innerHTML = '';
            // Display only 5 featured polymers on the home page
            const limit = grid.dataset.limit ? parseInt(grid.dataset.limit, 10) : 5;
            const featured = data.materials.slice(0, limit);
            featured.forEach(mat => {
                grid.appendChild(renderMaterialCard(mat));
            });
        }
    } catch (err) {
        console.error('Featured materials load failed', err);
    }
}

/* ---------- Load Full Catalog (/materials page: 100+ materials) ---------- */
async function loadCatalogMaterials() {
    const allGrid = document.getElementById('all-materials-grid');
    if (!allGrid) return;

    const countText = document.getElementById('catalog-count-text');
    const loadingEl = document.getElementById('catalog-loading');
    const searchInput = document.getElementById('catalog-search');
    const categorySelect = document.getElementById('category-filter');
    const resetBtn = document.getElementById('reset-filters-btn');

    try {
        const response = await fetch(`${API_BASE_URL}/api/materials`);
        const data = await response.json();

        if (loadingEl) loadingEl.classList.add('hidden');

        if (data.success && Array.isArray(data.materials)) {
            allMaterialsCache = data.materials;
            renderFilteredCatalog();

            if (searchInput) {
                searchInput.addEventListener('input', renderFilteredCatalog);
            }
            if (categorySelect) {
                categorySelect.addEventListener('change', renderFilteredCatalog);
            }
            if (resetBtn) {
                resetBtn.addEventListener('click', clearCatalogFilters);
            }
        } else {
            if (countText) countText.textContent = 'Unable to load catalog at this time.';
        }
    } catch (err) {
        if (loadingEl) loadingEl.classList.add('hidden');
        if (countText) countText.textContent = 'Error loading materials catalog.';
        console.error('Catalog load failed', err);
    }
}

function renderFilteredCatalog() {
    const allGrid = document.getElementById('all-materials-grid');
    if (!allGrid) return;

    const countText = document.getElementById('catalog-count-text');
    const searchInput = document.getElementById('catalog-search');
    const categorySelect = document.getElementById('category-filter');
    const emptyState = document.getElementById('catalog-empty-state');

    const query = searchInput ? searchInput.value.trim().toLowerCase() : '';
    const selectedCategory = categorySelect ? categorySelect.value : 'ALL';

    const filtered = allMaterialsCache.filter(mat => {
        // Category filter
        if (selectedCategory !== 'ALL') {
            const matCat = (mat.category || '').toLowerCase();
            const targetCat = selectedCategory.toLowerCase();
            if (!matCat.includes(targetCat)) return false;
        }

        // Text search (name, category, applications, description)
        if (query) {
            const name = (mat.name || '').toLowerCase();
            const category = (mat.category || '').toLowerCase();
            const apps = (mat.applications || '').toLowerCase();
            const desc = (mat.description || '').toLowerCase();
            return name.includes(query) || category.includes(query) || apps.includes(query) || desc.includes(query);
        }

        return true;
    });

    allGrid.innerHTML = '';

    if (filtered.length === 0) {
        if (emptyState) emptyState.classList.remove('hidden');
        if (countText) countText.textContent = `0 of ${allMaterialsCache.length} materials match your filters`;
    } else {
        if (emptyState) emptyState.classList.add('hidden');
        if (countText) {
            if (filtered.length === allMaterialsCache.length) {
                countText.textContent = `Showing all ${allMaterialsCache.length} engineering materials`;
            } else {
                countText.textContent = `Showing ${filtered.length} of ${allMaterialsCache.length} materials`;
            }
        }
        filtered.forEach(mat => {
            allGrid.appendChild(renderMaterialCard(mat));
        });
    }
}

function clearCatalogFilters() {
    const searchInput = document.getElementById('catalog-search');
    const categorySelect = document.getElementById('category-filter');
    if (searchInput) searchInput.value = '';
    if (categorySelect) categorySelect.value = 'ALL';
    renderFilteredCatalog();
}

/* ============================================================
   Form Validation & Recommendation Submission
   ============================================================ */

function showLoading(show) {
    const loading = document.getElementById('loading');
    const submitBtn = document.getElementById('submit-btn');
    if (loading) loading.classList.toggle('hidden', !show);
    if (submitBtn) submitBtn.disabled = show;
}

function validateForm() {
    const applicationEl = document.getElementById('application');
    const strengthEl = document.getElementById('strength');
    const temperatureEl = document.getElementById('temperature');
    const weightEl = document.getElementById('weight');
    const chemicalEl = document.getElementById('chemical_resistance');
    const costEl = document.getElementById('cost');

    const application = applicationEl ? applicationEl.value.trim() : '';
    const strength = strengthEl ? strengthEl.value : '';
    const temperatureRaw = temperatureEl ? temperatureEl.value : '';
    const weight = weightEl ? weightEl.value : '';
    const chemical = chemicalEl ? chemicalEl.value : '';
    const cost = costEl ? costEl.value : '';

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
            const response = await fetch(`${API_BASE_URL}/api/recommend`, {
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

/* ---------- Initialization ---------- */
document.addEventListener('DOMContentLoaded', () => {
    loadHomeFeaturedMaterials();
    loadCatalogMaterials();
});
