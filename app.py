from flask import Flask, jsonify, request, render_template, abort
from config import Config
from database import db, Polymer, RecommendationHistory, get_all_polymers, get_polymer_by_id, get_polymer_by_name
from recommendation.recommendation_engine import recommend_materials
import json
import traceback

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/test-db')
def test_db():
    try:
        db.session.execute(db.text('SELECT 1'))
        return """
        <h2 style="color: green;">✅ MySQL Connection Successful!</h2>
        <p>Database: <strong>polymer_recommendation_db</strong></p>
        """
    except Exception:
        return """
        <h2 style="color: red;">❌ MySQL Connection Failed</h2>
        <p>Please check that the MySQL service is running and credentials in .env are correct.</p>
        """


@app.route('/material/<int:id>')
def material_details(id):
    polymer = get_polymer_by_id(id)
    if polymer is None:
        abort(404)

    related = Polymer.query.filter(
        Polymer.category == polymer.category,
        Polymer.id != polymer.id
    ).limit(3).all()

    return render_template(
        'material_details.html',
        material=polymer,
        related=related
    )


# ============================================================
# Material API Endpoints
# ============================================================

@app.route('/api/materials', methods=['GET'])
def api_get_all_materials():
    try:
        polymers = get_all_polymers()
        result = [p.to_dict() for p in polymers]
        return jsonify({
            'success': True,
            'count': len(result),
            'materials': result
        }), 200
    except Exception:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': 'Unable to retrieve materials at this time. Please try again later.'
        }), 500


@app.route('/api/materials/<int:id>', methods=['GET'])
def api_get_material_by_id(id):
    try:
        polymer = get_polymer_by_id(id)
        if polymer is None:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': f'No material found with ID {id}.'
            }), 404

        return jsonify({
            'success': True,
            'material': polymer.to_dict()
        }), 200
    except Exception:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': 'Unable to retrieve the requested material. Please try again later.'
        }), 500


@app.route('/api/materials/name/<string:name>', methods=['GET'])
def api_get_material_by_name(name):
    try:
        if not name or not name.strip():
            return jsonify({
                'success': False,
                'error': 'validation_error',
                'message': 'Material name cannot be empty.'
            }), 400

        polymer = get_polymer_by_name(name.strip())
        if polymer is None:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': f'No material found with the name "{name}".'
            }), 404

        return jsonify({
            'success': True,
            'material': polymer.to_dict()
        }), 200
    except Exception:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': 'Unable to retrieve the requested material. Please try again later.'
        }), 500


# ============================================================
# Recommendation API – Full Validation & Safe Error Handling
# ============================================================

@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    try:
        # 1. Content-Type check
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'validation_error',
                'message': 'Request must be sent as JSON.'
            }), 400

        data = request.get_json(silent=True)
        if data is None:
            return jsonify({
                'success': False,
                'error': 'validation_error',
                'message': 'Invalid or empty JSON body.'
            }), 400

        # 2. Required fields
        required_fields = [
            'application', 'strength', 'temperature',
            'weight', 'chemical_resistance', 'cost'
        ]
        missing = [
            field for field in required_fields
            if field not in data or data[field] is None or str(data[field]).strip() == ''
        ]
        if missing:
            return jsonify({
                'success': False,
                'error': 'validation_error',
                'message': f'Missing required fields: {", ".join(missing)}.'
            }), 400

        # 3. Extract & clean
        application = str(data['application']).strip()
        strength = str(data['strength']).strip().capitalize()
        weight = str(data['weight']).strip().capitalize()
        chemical_resistance = str(data['chemical_resistance']).strip().capitalize()
        cost = str(data['cost']).strip().capitalize()

        # 4. Temperature validation
        try:
            temperature = int(data['temperature'])
        except (TypeError, ValueError):
            return jsonify({
                'success': False,
                'error': 'validation_error',
                'message': 'Operating temperature must be a whole number (e.g. 60).'
            }), 400

        if temperature < 0 or temperature > 400:
            return jsonify({
                'success': False,
                'error': 'validation_error',
                'message': 'Operating temperature must be between 0°C and 400°C.'
            }), 400

        # 5. Allowed categorical values
        allowed = {
            'strength': ['Low', 'Medium', 'High'],
            'weight': ['Low', 'Medium', 'High'],
            'chemical_resistance': ['Low', 'Medium', 'High'],
            'cost': ['Low', 'Medium', 'High']
        }

        if strength not in allowed['strength']:
            return jsonify({
                'success': False,
                'error': 'validation_error',
                'message': 'Strength must be one of: Low, Medium, High.'
            }), 400

        if weight not in allowed['weight']:
            return jsonify({
                'success': False,
                'error': 'validation_error',
                'message': 'Weight requirement must be one of: Low, Medium, High.'
            }), 400

        if chemical_resistance not in allowed['chemical_resistance']:
            return jsonify({
                'success': False,
                'error': 'validation_error',
                'message': 'Chemical resistance must be one of: Low, Medium, High.'
            }), 400

        if cost not in allowed['cost']:
            return jsonify({
                'success': False,
                'error': 'validation_error',
                'message': 'Cost preference must be one of: Low, Medium, High.'
            }), 400

        # 6. Application length sanity check
        if len(application) < 2 or len(application) > 150:
            return jsonify({
                'success': False,
                'error': 'validation_error',
                'message': 'Application type must be between 2 and 150 characters.'
            }), 400

        # 7. Call recommendation engine
        try:
            recommendations = recommend_materials(
                application=application,
                required_strength=strength,
                operating_temperature=temperature,
                weight_requirement=weight,
                chemical_resistance=chemical_resistance,
                cost_preference=cost
            )
        except Exception:
            # Log internally if needed, but never expose details
            return jsonify({
                'success': False,
                'error': 'engine_error',
                'message': 'The recommendation engine encountered a problem. Please try again.'
            }), 500

        if not recommendations:
            return jsonify({
                'success': False,
                'error': 'no_results',
                'message': 'No suitable materials found for the given requirements. Try adjusting your inputs.'
            }), 200

        # 8. Save history (non-blocking for the user)
        try:
            history_entry = RecommendationHistory(
                application=application,
                required_strength=strength,
                operating_temperature=temperature,
                weight_requirement=weight,
                chemical_resistance=chemical_resistance,
                cost_preference=cost,
                recommendation_result=json.dumps(recommendations)
            )
            db.session.add(history_entry)
            db.session.commit()
        except Exception:
            db.session.rollback()
            # History failure must not break the response

        # 9. Success
        return jsonify({
            'success': True,
            'count': len(recommendations),
            'message': 'Recommendations generated successfully.',
            'recommendations': recommendations
        }), 200

    except Exception:
        # Catch-all – never leak stack traces
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': 'An unexpected error occurred. Please try again later.'
        }), 500


# Optional: friendly 404 page for material details
@app.errorhandler(404)
def not_found(e):
    return render_template('index.html'), 404


if __name__ == '__main__':
    app.run(debug=True)