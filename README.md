# Polymer Material Selection and Recommendation System

**Web-Based Polymer Material Selection and Recommendation System Using Rule-Based Decision Making**

A complete final-year engineering project that recommends the most suitable polymer materials based on user requirements using a transparent rule-based scoring algorithm.

---

## 1. Project Title

**Web-Based Polymer Material Selection and Recommendation System Using Rule-Based Decision Making**

---

## 2. Project Description

This project is a full-stack web application that helps engineers and students select the most appropriate polymer material for a given application.  

Users enter requirements such as:
- Application type
- Required strength
- Operating temperature
- Weight preference
- Chemical resistance
- Cost preference

The system evaluates all available polymers stored in a MySQL database using a **100-point rule-based decision algorithm** and returns the **Top 3 recommended materials** together with:
- Compatibility score & percentage
- Detailed matching reasons
- Advantages
- Limitations
- Critical warnings (when a material does not satisfy a key requirement)

The entire system is built with pure HTML, CSS, JavaScript on the frontend and Python (Flask) + MySQL on the backend — making it ideal for a final-year academic project.

---

## 3. Features

- Professional responsive home page
- Sticky navigation bar
- Hero section & project introduction
- “How it works” section
- Material recommendation form with client-side validation
- Rule-based recommendation engine (100-point scoring)
- Top 3 ranked recommendations with progress bars
- Compatibility score, reasons, advantages, limitations & warnings
- Material details page for every polymer
- MySQL-backed polymer database
- Recommendation history logging
- Loading, error, empty and success states
- Fully responsive design (mobile, tablet, laptop, desktop)
- Clean REST API endpoints
- Secure configuration using `.env`

---

## 4. Technology Stack

| Layer            | Technology                          |
|------------------|-------------------------------------|
| Frontend         | HTML5, CSS3, JavaScript (Vanilla)   |
| Backend          | Python 3, Flask                     |
| Production Server| Gunicorn (WSGI)                     |
| Database         | MySQL (InnoDB, UTF-8)               |
| ORM              | Flask-SQLAlchemy + PyMySQL          |
| Configuration    | python-dotenv                       |
| Decision System  | Custom Rule-Based Algorithm         |
| Hosting Target   | Render (Flask) + Hosted MySQL       |

---

## 5. Project Architecture

```
polymer-material-selection-system/
├── app.py                     # Application entry point, web routes & REST API
├── config.py                  # Environment-driven configuration & DB URI resolution
├── database.py                # SQLAlchemy models (Polymer, History) & seed logic
├── init_db.py                 # Idempotent DB schema creation and seed CLI script
├── requirements.txt           # Pinned production Python dependencies (UTF-8)
├── .env.example               # Template for environment variables (no real secrets)
├── .gitignore                 # Excludes .env, virtual environments, caches
├── database/
│   ├── polymer_database.sql   # Initial MySQL script (with DB create/use)
│   └── schema_and_seed.sql    # Safe cloud-ready schema & idempotent seed SQL
├── recommendation/
│   ├── __init__.py
│   └── recommendation_engine.py  # 100-point multi-attribute scoring engine
├── static/
│   ├── css/
│   │   └── style.css          # Design system & responsive styles
│   └── js/
│       └── script.js          # Client-side validation, API fetch & DOM rendering
└── templates/
    ├── index.html             # Main application UI & recommendation form
    └── material_details.html  # Polymer deep-dive specification view
```

---

## 6. Local Development Setup

### Prerequisites
- Python 3.10+
- MySQL Server 8.0+

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YashChavhan-1612/polymer-material-selection-system.git
   cd polymer-material-selection-system
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   Copy `.env.example` to `.env` and fill in your local MySQL credentials:
   ```bash
   cp .env.example .env
   ```

5. **Initialize Database and Seed Polymers:**
   Run the idempotent database initialization script:
   ```bash
   python init_db.py
   # or via Flask CLI:
   flask init-db
   ```

6. **Start the development server:**
   ```bash
   python app.py
   ```
   Open `http://localhost:5000` in your browser.

---

## 7. Production Deployment (Render)

The application is configured to run as a single unified service on Render that serves both the frontend HTML/CSS/JS and the backend REST API.

### A. Provision Hosted MySQL Database
Provision a managed MySQL database from a provider such as:
- **Aiven for MySQL** (Free tier available)
- **Clever Cloud** (Free MySQL plan)
- **Railway** / **TiDB Cloud**

Obtain your database connection URL (`mysql://...` or discrete host/port/user/password).

### B. Initialize Database Schema and Seed Data
You can initialize the database using either:
- **Option 1 (Automated):** Run `python init_db.py` in the Render Shell after deployment.
- **Option 2 (Web Console / SQL):** Run the idempotent script `database/schema_and_seed.sql` in your MySQL database console or GUI (DBeaver / phpMyAdmin).

### C. Configure Web Service on Render
1. Log in to [Render](https://render.com) and click **New +** -> **Web Service**.
2. Connect your GitHub repository: `polymer-material-selection-system`.
3. Configure the settings:
   - **Environment:** `Python 3`
   - **Region:** Choose the region closest to your MySQL database.
   - **Branch:** `main`
   - **Build Command:**
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     gunicorn app:app
     ```
     *(Render sets the `PORT` environment variable automatically, which Gunicorn binds to by default).*

4. Set the **Environment Variables** in the Render Dashboard:
   | Variable Name | Required | Description / Example |
   |---|---|---|
   | `ENVIRONMENT` | Yes | `production` |
   | `SECRET_KEY` | Yes (Secret) | 32+ character random secret string |
   | `DATABASE_URL` | Yes (Secret) | `mysql+pymysql://db_user:db_password@db_host:port/db_name` |
   | `FLASK_DEBUG` | No | `0` |

5. Deploy the service.

---

## 8. Post-Deployment Verification Checklist

Once deployed to Render:

1. **Application Health & DB Readiness:**
   - Open `https://<your-render-app>.onrender.com/health` in your browser.
   - Expected response: `{"status": "healthy", "database": "connected", "version": "1.0.0"}` with HTTP 200.

2. **Home Page & Frontend:**
   - Visit `https://<your-render-app>.onrender.com/`.
   - Verify the PolySelect UI renders properly with styling, navigation, and features.

3. **Materials Overview:**
   - Scroll to "Available Polymer Materials".
   - Verify all 8 polymers are loaded dynamically from MySQL.

4. **Material Details View:**
   - Click on any polymer card (e.g. HDPE or Nylon 6).
   - Verify `https://<your-render-app>.onrender.com/material/<id>` renders comprehensive technical specifications.

5. **Recommendation Engine Flow:**
   - Fill in the recommendation form with test engineering requirements:
     - Application: `Water Pipe`
     - Strength: `Medium`
     - Temperature: `60`
     - Weight: `Low`
     - Chemical Resistance: `High`
     - Cost: `Low`
   - Click **Get Recommendations**.
   - Verify the top 3 ranked polymer cards appear with compatibility scores, matching reasons, and warnings.
