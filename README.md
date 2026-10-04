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
| Database         | MySQL                               |
| ORM              | Flask-SQLAlchemy + PyMySQL          |
| Configuration    | python-dotenv                       |
| Decision System  | Custom Rule-Based Algorithm         |
| Development IDE  | Visual Studio Code                  |

---

## 5. Project Architecture
