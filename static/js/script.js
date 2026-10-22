// ================== API CONFIGURATION ==================
// In single-origin deployments (Flask serving HTML), API_BASE_URL is empty ('').
// In decoupled architectures (e.g. Vercel frontend calling Render backend),
// window.API_BASE_URL can be set to the backend's public URL.
const API_BASE_URL = window.API_BASE_URL || '';

/* ============================================================
   PolySelect – Navigation & Mobile Menu with Backdrop & Scroll Lock
   ============================================================ */

function setupNavigation() {
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('nav-links');
    const backdrop = document.getElementById('nav-backdrop');
    const closeBtn = document.getElementById('nav-close-btn');

    function openMenu() {
        if (navLinks) navLinks.classList.add('active');
        if (backdrop) backdrop.classList.add('active');
        if (hamburger) hamburger.classList.add('open');
        document.body.classList.add('menu-open');
    }

    function closeMenu() {
        if (navLinks) navLinks.classList.remove('active');
        if (backdrop) backdrop.classList.remove('active');
        if (hamburger) hamburger.classList.remove('open');
        document.body.classList.remove('menu-open');
    }

    if (hamburger) {
        hamburger.addEventListener('click', (e) => {
            e.stopPropagation();
            if (navLinks && navLinks.classList.contains('active')) {
                closeMenu();
            } else {
                openMenu();
            }
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', closeMenu);
    }

    if (backdrop) {
        backdrop.addEventListener('click', closeMenu);
    }

    // Close menu when clicking any nav link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', closeMenu);
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeMenu();
    });
}

/* ============================================================
   Material Cards & Rendering Helpers
   ============================================================ */

let allMaterialsCache = [];
let currentSelectedCategory = 'ALL';

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
        <span class="category-badge">
            ${escapeHtml(mat.category)}
        </span>
        <h3 style="margin-bottom:0.4rem;font-size:1.15rem;">${escapeHtml(mat.name)}</h3>
        <p class="material-meta" style="font-size:0.85rem;color:var(--text-muted);">
            ${escapeHtml(String(mat.strength))} MPa · ${escapeHtml(String(mat.max_temperature))}°C · ${escapeHtml(mat.cost)} Cost
        </p>
    `;
    return card;
}

function renderCatalogCard(mat) {
    const card = document.createElement('a');
    card.className = 'catalog-card';
    card.href = `/material/${encodeURIComponent(mat.id)}`;
    card.innerHTML = `
        <div>
            <span class="card-category-tag">${escapeHtml(mat.category)}</span>
            <h3>${escapeHtml(mat.name)}</h3>
            <p class="catalog-card-desc">${escapeHtml(mat.description || '')}</p>
        </div>
        <div>
            <div class="card-props-chips">
                <span class="prop-chip" title="Tensile Strength"><i class="fas fa-dumbbell"></i> ${escapeHtml(String(mat.strength))} MPa</span>
                <span class="prop-chip" title="Max Temperature"><i class="fas fa-thermometer-half"></i> ${escapeHtml(String(mat.max_temperature))}°C</span>
                <span class="prop-chip" title="Density"><i class="fas fa-weight-hanging"></i> ${escapeHtml(String(mat.density))} g/cm³</span>
                <span class="prop-chip" title="Cost Level"><i class="fas fa-tag"></i> ${escapeHtml(mat.cost)}</span>
            </div>
            <span class="card-view-btn">View Specifications <i class="fas fa-arrow-right"></i></span>
        </div>
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

        if (data.success && Array.isArray(data.materials) && data.materials.length > 0) {
            grid.innerHTML = '';
            // Display 5 featured polymers on the home page
            const limit = grid.dataset.limit ? parseInt(grid.dataset.limit, 10) : 5;
            const featured = data.materials.slice(0, limit);
            featured.forEach(mat => {
                grid.appendChild(renderMaterialCard(mat));
            });
        }
    } catch (err) {
        console.warn('Featured materials live update deferred; keeping pre-rendered cards', err);
    }
}

/* ---------- Category Matcher Helper ---------- */
function matchesCategory(materialCategory, selectedCategory) {
    if (selectedCategory === 'ALL') return true;
    const cat = (materialCategory || '').toLowerCase();
    const sel = selectedCategory.toLowerCase();

    if (sel === 'thermoplastic') {
        return (cat.includes('thermoplastic') && !cat.includes('engineering') && !cat.includes('elastomer'))
            || cat.includes('polyethylene') || cat.includes('cellular');
    }
    if (sel === 'engineering thermoplastic') {
        return cat.includes('engineering') || cat.includes('polyamide');
    }
    if (sel === 'high-performance') {
        return cat.includes('high-performance') || cat.includes('ultra-high');
    }
    if (sel === 'fluoropolymer') {
        return cat.includes('fluoropolymer');
    }
    if (sel === 'thermoset') {
        return cat.includes('thermoset');
    }
    if (sel === 'elastomer') {
        return cat.includes('elastomer') || cat.includes('rubber');
    }
    if (sel === 'biopolymer') {
        return cat.includes('bio');
    }
    if (sel === 'reinforced composite') {
        return cat.includes('reinforced') || cat.includes('composite');
    }
    if (sel === 'specialty') {
        return cat.includes('specialty') || cat.includes('blend') || cat.includes('copolymer') || cat.includes('barrier');
    }

    return cat.includes(sel);
}

/* ---------- Category Names for Readable Feedback ---------- */
const CATEGORY_DISPLAY_NAMES = {
    'ALL': 'engineering polymers',
    'Thermoplastic': 'Commodity Thermoplastics',
    'Engineering Thermoplastic': 'Engineering Thermoplastics',
    'High-Performance': 'High-Performance Polymers',
    'Fluoropolymer': 'Fluoropolymers',
    'Thermoset': 'Thermosets & Resins',
    'Elastomer': 'Elastomers & Rubbers',
    'Biopolymer': 'Biopolymers & Bio-Based Polymers',
    'Reinforced Composite': 'Reinforced Composites',
    'Specialty': 'Specialty Polymers & Blends'
};

/* ---------- Load Full Catalog (/materials page: 100+ materials) ---------- */
async function loadCatalogMaterials() {
    const allGrid = document.getElementById('all-materials-grid');
    if (!allGrid) return;

    const countText = document.getElementById('catalog-count-text');
    const loadingEl = document.getElementById('catalog-loading');
    const keywordInput = document.getElementById('catalog-keyword');
    const categorySelect = document.getElementById('category-filter-select');
    const pillsList = document.querySelectorAll('.category-pill');
    const resetBtn = document.getElementById('btn-show-all-categories');

    // 1. Immediately hydrate from embedded JSON if available (zero-delay, 100% offline-safe)
    const initialDataEl = document.getElementById('initial-catalog-data');
    if (initialDataEl) {
        try {
            const raw = initialDataEl.textContent.trim();
            if (raw) {
                const parsed = JSON.parse(raw);
                if (Array.isArray(parsed) && parsed.length > 0) {
                    allMaterialsCache = parsed;
                    renderFilteredCatalog();
                }
            }
        } catch (e) {
            console.warn('Could not parse embedded initial catalog data', e);
        }
    }

    // 2. Setup Category Pills Click Listener
    pillsList.forEach(pill => {
        pill.addEventListener('click', () => {
            const cat = pill.dataset.category || 'ALL';
            setSelectedCategory(cat);
        });
    });

    // 3. Setup Category Dropdown Listener
    if (categorySelect) {
        categorySelect.addEventListener('change', () => {
            setSelectedCategory(categorySelect.value);
        });
    }

    // 4. Setup Optional Keyword Filter
    if (keywordInput) {
        keywordInput.addEventListener('input', () => {
            renderFilteredCatalog();
        });
    }

    // 5. Setup Reset Button
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            if (keywordInput) keywordInput.value = '';
            setSelectedCategory('ALL');
        });
    }

    // 6. Fetch live updates from API in the background
    try {
        const response = await fetch(`${API_BASE_URL}/api/materials`);
        const data = await response.json();
        if (loadingEl) loadingEl.classList.add('hidden');

        if (data.success && Array.isArray(data.materials) && data.materials.length > 0) {
            allMaterialsCache = data.materials;
            renderFilteredCatalog();
        } else if (allMaterialsCache.length === 0) {
            if (countText) countText.textContent = 'Polymer materials catalog available.';
        }
    } catch (err) {
        if (loadingEl) loadingEl.classList.add('hidden');
        console.warn('Live API fetch deferred; using catalog cache', err);
    }
}

function setSelectedCategory(categoryKey) {
    currentSelectedCategory = categoryKey;

    // Update active class on pills
    document.querySelectorAll('.category-pill').forEach(pill => {
        if (pill.dataset.category === categoryKey) {
            pill.classList.add('active');
        } else {
            pill.classList.remove('active');
        }
    });

    // Sync dropdown
    const categorySelect = document.getElementById('category-filter-select');
    if (categorySelect && categorySelect.value !== categoryKey) {
        for (let i = 0; i < categorySelect.options.length; i++) {
            if (categorySelect.options[i].value === categoryKey) {
                categorySelect.selectedIndex = i;
                break;
            }
        }
    }

    renderFilteredCatalog();
}

function renderFilteredCatalog() {
    const allGrid = document.getElementById('all-materials-grid');
    if (!allGrid) return;

    const countText = document.getElementById('catalog-count-text');
    const keywordInput = document.getElementById('catalog-keyword');
    const emptyState = document.getElementById('catalog-empty-state');

    const keyword = keywordInput ? keywordInput.value.trim().toLowerCase() : '';

    const filtered = allMaterialsCache.filter(mat => {
        // Category filter
        if (!matchesCategory(mat.category, currentSelectedCategory)) {
            return false;
        }

        // Optional keyword filter (name, category, applications, description)
        if (keyword) {
            const name = (mat.name || '').toLowerCase();
            const category = (mat.category || '').toLowerCase();
            const apps = (mat.applications || '').toLowerCase();
            const desc = (mat.description || '').toLowerCase();
            return name.includes(keyword) || category.includes(keyword) || apps.includes(keyword) || desc.includes(keyword);
        }

        return true;
    });

    allGrid.innerHTML = '';

    const totalCount = allMaterialsCache.length;
    const catLabel = CATEGORY_DISPLAY_NAMES[currentSelectedCategory] || currentSelectedCategory;

    if (filtered.length === 0) {
        if (emptyState) emptyState.classList.remove('hidden');
        if (countText) countText.textContent = `0 materials found in "${catLabel}"`;
    } else {
        if (emptyState) emptyState.classList.add('hidden');
        if (countText) {
            if (currentSelectedCategory === 'ALL' && !keyword) {
                countText.textContent = `Showing all ${totalCount} engineering polymers · Select a category above to filter`;
            } else if (keyword) {
                countText.textContent = `Showing ${filtered.length} materials matching "${keyword}" in ${catLabel}`;
            } else {
                countText.textContent = `Showing ${filtered.length} ${catLabel} (out of ${totalCount} materials in database)`;
            }
        }
        filtered.forEach(mat => {
            allGrid.appendChild(renderCatalogCard(mat));
        });
    }
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
                <div style="margin-top: 1rem; padding-top: 0.85rem; border-top: 1px solid var(--border);">
                    <a href="/material/${encodeURIComponent(rec.material_id)}" class="btn btn-outline" style="display:inline-flex;align-items:center;gap:0.4rem;font-size:0.85rem;padding:0.45rem 1rem;">
                        <i class="fas fa-file-alt"></i> View Full Specifications &amp; Properties &rarr;
                    </a>
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
    setupNavigation();
    if (document.getElementById('materials-grid')) {
        loadHomeFeaturedMaterials();
    }
    if (document.getElementById('all-materials-grid')) {
        loadCatalogMaterials();
    }
});
