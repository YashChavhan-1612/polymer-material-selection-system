import json
import os
import logging

from flask import Flask, jsonify, request, render_template, abort
from flask_cors import CORS
from sqlalchemy import text
from werkzeug.exceptions import HTTPException

from config import Config
from database import (
    db,
    Polymer,
    RecommendationHistory,
    get_all_polymers,
    get_polymer_by_id,
    get_polymer_by_name,
    seed_database,
)
from recommendation.recommendation_engine import recommend_materials

app = Flask(__name__)
app.config.from_object(Config)

# Log exceptions to Render runtime logs without exposing credentials.
app.logger.setLevel(logging.INFO)

CORS(app, resources={r"/api/*": {"origins": "*"}})

db.init_app(app)


def auto_init_database():
    """Automatically verify schema and seed materials if database is reachable."""
    with app.app_context():
        try:
            db.create_all()
            inserted, total = seed_database()
            if inserted > 0:
                app.logger.info("Database auto-initialized. Seeded %d materials. Total: %d.", inserted, total)
        except Exception as exc:
            db.session.rollback()
            app.logger.warning("Database auto-init deferred or failed: %s", exc)


# Run auto-initialization on startup
auto_init_database()


# ============================================================
# Frontend routes
# ============================================================

@app.route("/")
def home():
    """Serve the complete interactive frontend UI."""
    return render_template("index.html")


@app.route("/materials")
def materials_catalog():
    """Serve the complete polymer materials catalog page."""
    return render_template("materials.html")


@app.route("/material/<int:id>")
def material_details(id):
    """Serve the detailed property view for a specific polymer."""
    try:
        polymer = get_polymer_by_id(id)

        if polymer is None:
            abort(404)

        related = Polymer.query.filter(
            Polymer.category == polymer.category,
            Polymer.id != polymer.id,
        ).limit(3).all()

        return render_template(
            "material_details.html",
            material=polymer,
            related=related,
        )
    except HTTPException:
        raise
    except Exception:
        app.logger.exception("MATERIAL DETAILS FAILED")
        raise


# ============================================================
# Health endpoints
# ============================================================

@app.route("/health", methods=["GET"])
@app.route("/api/health", methods=["GET"])
def health_check():
    """Check application liveness and database connectivity."""
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "version": "1.0.0",
        }), 200
    except Exception:
        db.session.rollback()
        app.logger.exception("DATABASE HEALTH CHECK FAILED")
        return jsonify({
            "status": "degraded",
            "database": "disconnected",
            "version": "1.0.0",
        }), 503


@app.route("/test-db", methods=["GET"])
def test_db():
    """Diagnostic database connectivity check."""
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({
            "success": True,
            "message": "Database connection successful",
        }), 200
    except Exception:
        db.session.rollback()
        app.logger.exception("DATABASE TEST FAILED")
        return jsonify({
            "success": False,
            "message": "Database connection failed",
        }), 500


# ============================================================
# Materials API
# ============================================================

@app.route("/api/materials", methods=["GET"])
def api_get_all_materials():
    """Retrieve all polymers as JSON."""
    try:
        polymers = get_all_polymers()
        result = [polymer.to_dict() for polymer in polymers]

        return jsonify({
            "success": True,
            "count": len(result),
            "materials": result,
        }), 200

    except Exception:
        db.session.rollback()
        app.logger.exception("GET ALL MATERIALS FAILED")
        return jsonify({
            "success": False,
            "error": "server_error",
            "message": "Unable to retrieve materials at this time. Please try again later.",
        }), 500


@app.route("/api/materials/<int:id>", methods=["GET"])
def api_get_material_by_id(id):
    """Retrieve a single polymer by ID."""
    try:
        polymer = get_polymer_by_id(id)

        if polymer is None:
            return jsonify({
                "success": False,
                "error": "not_found",
                "message": f"No material found with ID {id}.",
            }), 404

        return jsonify({
            "success": True,
            "material": polymer.to_dict(),
        }), 200

    except Exception:
        db.session.rollback()
        app.logger.exception("GET MATERIAL BY ID FAILED")
        return jsonify({
            "success": False,
            "error": "server_error",
            "message": "Unable to retrieve the requested material. Please try again later.",
        }), 500


@app.route("/api/materials/name/<string:name>", methods=["GET"])
def api_get_material_by_name(name):
    """Retrieve a single polymer by name."""
    try:
        if not name or not name.strip():
            return jsonify({
                "success": False,
                "error": "validation_error",
                "message": "Material name cannot be empty.",
            }), 400

        polymer = get_polymer_by_name(name.strip())

        if polymer is None:
            return jsonify({
                "success": False,
                "error": "not_found",
                "message": f'No material found with the name "{name}".',
            }), 404

        return jsonify({
            "success": True,
            "material": polymer.to_dict(),
        }), 200

    except Exception:
        db.session.rollback()
        app.logger.exception("GET MATERIAL BY NAME FAILED")
        return jsonify({
            "success": False,
            "error": "server_error",
            "message": "Unable to retrieve the requested material. Please try again later.",
        }), 500


# ============================================================
# Recommendation API
# ============================================================

@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    """Score requirements against polymers and return Top 3 ranked recommendations."""
    try:
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "validation_error",
                "message": "Request must be sent as JSON.",
            }), 400

        data = request.get_json(silent=True)

        if data is None or not isinstance(data, dict):
            return jsonify({
                "success": False,
                "error": "validation_error",
                "message": "Invalid or empty JSON body.",
            }), 400

        required_fields = [
            "application",
            "strength",
            "temperature",
            "weight",
            "chemical_resistance",
            "cost",
        ]

        missing = [
            field for field in required_fields
            if field not in data
            or data[field] is None
            or str(data[field]).strip() == ""
        ]

        if missing:
            return jsonify({
                "success": False,
                "error": "validation_error",
                "message": f"Missing required fields: {', '.join(missing)}.",
            }), 400

        application = str(data["application"]).strip()
        strength = str(data["strength"]).strip().capitalize()
        weight = str(data["weight"]).strip().capitalize()
        chemical_resistance = (
            str(data["chemical_resistance"]).strip().capitalize()
        )
        cost = str(data["cost"]).strip().capitalize()

        try:
            temperature = int(data["temperature"])
        except (TypeError, ValueError):
            return jsonify({
                "success": False,
                "error": "validation_error",
                "message": "Operating temperature must be a whole number (e.g. 60).",
            }), 400

        if temperature < 0 or temperature > 400:
            return jsonify({
                "success": False,
                "error": "validation_error",
                "message": "Operating temperature must be between 0°C and 400°C.",
            }), 400

        allowed = {
            "strength": ["Low", "Medium", "High"],
            "weight": ["Low", "Medium", "High"],
            "chemical_resistance": ["Low", "Medium", "High"],
            "cost": ["Low", "Medium", "High"],
        }

        for field, value in [
            ("strength", strength),
            ("weight", weight),
            ("chemical_resistance", chemical_resistance),
            ("cost", cost),
        ]:
            if value not in allowed[field]:
                return jsonify({
                    "success": False,
                    "error": "validation_error",
                    "message": (
                        f"{field.replace('_', ' ').title()} must be one of: "
                        f"{', '.join(allowed[field])}."
                    ),
                }), 400

        if len(application) < 2 or len(application) > 150:
            return jsonify({
                "success": False,
                "error": "validation_error",
                "message": "Application type must be between 2 and 150 characters.",
            }), 400

        # Generate recommendations using the rule-based engine.
        try:
            recommendations = recommend_materials(
                application=application,
                required_strength=strength,
                operating_temperature=temperature,
                weight_requirement=weight,
                chemical_resistance=chemical_resistance,
                cost_preference=cost,
            )
        except Exception:
            app.logger.exception("RECOMMENDATION ENGINE FAILED")
            return jsonify({
                "success": False,
                "error": "engine_error",
                "message": "The recommendation engine encountered a problem. Please try again.",
            }), 500

        if not recommendations:
            return jsonify({
                "success": False,
                "error": "no_results",
                "message": "No suitable materials found. Try adjusting your inputs.",
            }), 200

        # History is non-critical: a history write failure must not
        # prevent an otherwise successful recommendation response.
        try:
            history_entry = RecommendationHistory(
                application=application,
                required_strength=strength,
                operating_temperature=temperature,
                weight_requirement=weight,
                chemical_resistance=chemical_resistance,
                cost_preference=cost,
                recommendation_result=json.dumps(recommendations),
            )
            db.session.add(history_entry)
            db.session.commit()

        except Exception:
            db.session.rollback()
            app.logger.exception("SAVING RECOMMENDATION HISTORY FAILED")

        return jsonify({
            "success": True,
            "count": len(recommendations),
            "message": "Recommendations generated successfully.",
            "recommendations": recommendations,
        }), 200

    except Exception:
        db.session.rollback()
        app.logger.exception("RECOMMENDATION API FAILED")
        return jsonify({
            "success": False,
            "error": "server_error",
            "message": "An unexpected error occurred. Please try again later.",
        }), 500


# ============================================================
# Error handlers
# ============================================================

@app.errorhandler(404)
def not_found(error):
    if request.path.startswith("/api/"):
        return jsonify({
            "success": False,
            "error": "not_found",
            "message": "The requested API endpoint was not found.",
        }), 404

    return render_template("index.html"), 404


@app.errorhandler(500)
def server_error(error):
    app.logger.error(
        "UNHANDLED HTTP 500 ERROR on %s",
        request.path,
        exc_info=True,
    )

    if request.path.startswith("/api/"):
        return jsonify({
            "success": False,
            "error": "server_error",
            "message": "Internal server error occurred.",
        }), 500

    return "An internal server error occurred. Please try again later.", 500


# ============================================================
# Database initialization CLI
# ============================================================

@app.cli.command("init-db")
def init_db_command():
    """Create database tables and seed default polymer materials."""
    with app.app_context():
        try:
            db.create_all()
            inserted, total = seed_database()
            print(
                f"Database schema verified. Seeded {inserted} new materials. "
                f"Total materials: {total}."
            )
        except Exception:
            db.session.rollback()
            app.logger.exception("DATABASE INITIALIZATION FAILED")
            raise


# ============================================================
# Application startup
# ============================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=Config.DEBUG,
    )
