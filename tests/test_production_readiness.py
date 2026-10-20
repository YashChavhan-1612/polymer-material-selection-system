"""
Comprehensive Production Deployment Readiness Test Suite
Verifies all functionality and security requirements for the Polymer Material Selection System.
"""
import os
import sys
import unittest
import json

# Ensure project root is in path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app, db
from config import Config, build_database_uri
from database import Polymer, RecommendationHistory, get_all_polymers, get_polymer_by_id, get_polymer_by_name, seed_database
from recommendation.recommendation_engine import recommend_materials


class TestProductionReadiness(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()

    def test_01_gunicorn_import_target(self):
        """Test that 'app:app' can be imported cleanly by Gunicorn."""
        import importlib
        app_module = importlib.import_module('app')
        self.assertTrue(hasattr(app_module, 'app'), "Module 'app' must expose 'app' WSGI object")
        self.assertEqual(app_module.app.name, 'app')

    def test_02_config_uri_builder(self):
        """Test that database URI handles standard and cloud URL formats."""
        # 1. Plain mysql:// -> converted to mysql+pymysql://
        old_db_url = os.environ.get('DATABASE_URL')
        try:
            os.environ['DATABASE_URL'] = 'mysql://user:pass@host.example.com:3306/testdb'
            uri = build_database_uri()
            self.assertTrue(uri.startswith('mysql+pymysql://'))
            self.assertIn('host.example.com:3306/testdb', uri)

            # 2. mysql2:// -> converted to mysql+pymysql://
            os.environ['DATABASE_URL'] = 'mysql2://user:pass@host.example.com:3306/testdb'
            uri = build_database_uri()
            self.assertTrue(uri.startswith('mysql+pymysql://'))

            # 3. Already mysql+pymysql:// -> unchanged
            os.environ['DATABASE_URL'] = 'mysql+pymysql://user:pass@host.example.com:3306/testdb'
            uri = build_database_uri()
            self.assertEqual(uri, 'mysql+pymysql://user:pass@host.example.com:3306/testdb')
        finally:
            if old_db_url is not None:
                os.environ['DATABASE_URL'] = old_db_url
            else:
                os.environ.pop('DATABASE_URL', None)

    def test_03_home_page_renders_html(self):
        """Test that GET / returns HTTP 200 with HTML content."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.content_type)
        content = response.get_data(as_text=True)
        self.assertIn('PolySelect', content)
        self.assertIn('Material Recommendation', content)

    def test_04_health_endpoint(self):
        """Test that /health returns liveness and database readiness status."""
        response = self.client.get('/health')
        self.assertIn(response.status_code, [200, 503])
        data = response.get_json()
        self.assertIn('status', data)
        self.assertIn('database', data)
        self.assertIn('version', data)

    def test_05_material_details_html_page(self):
        """Test that /material/<id> renders detailed view."""
        with app.app_context():
            polymer = Polymer.query.first()
            if polymer:
                response = self.client.get(f'/material/{polymer.id}')
                self.assertEqual(response.status_code, 200)
                content = response.get_data(as_text=True)
                self.assertIn(polymer.name, content)
                self.assertIn('Key Properties', content)

    def test_06_material_details_404(self):
        """Test that requesting an invalid material ID returns 404."""
        response = self.client.get('/material/999999')
        self.assertEqual(response.status_code, 404)

    def test_07_api_get_all_materials(self):
        """Test GET /api/materials returns JSON list."""
        response = self.client.get('/api/materials')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIsInstance(data['materials'], list)
        self.assertGreaterEqual(data['count'], 7)

    def test_08_api_get_material_by_id(self):
        """Test GET /api/materials/<id> returns single material."""
        response = self.client.get('/api/materials/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['material']['id'], 1)

    def test_09_api_recommend_valid_payload(self):
        """Test POST /api/recommend with valid engineering requirements."""
        payload = {
            'application': 'High pressure water pipe',
            'strength': 'High',
            'temperature': 60,
            'weight': 'Low',
            'chemical_resistance': 'High',
            'cost': 'Low'
        }
        response = self.client.post('/api/recommend', json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(len(data['recommendations']), 3)

        # Verify rank 1, 2, 3
        ranks = [r['rank'] for r in data['recommendations']]
        self.assertEqual(ranks, [1, 2, 3])

        # Verify scores are sorted descending
        scores = [r['compatibility_score'] for r in data['recommendations']]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_10_api_recommend_validation_missing_fields(self):
        """Test recommendation rejection when required fields are missing."""
        payload = {
            'application': 'Pipe',
            # missing strength, temperature, etc.
        }
        response = self.client.post('/api/recommend', json=payload)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'validation_error')

    def test_11_api_recommend_validation_invalid_temperature(self):
        """Test rejection when temperature exceeds 400 or is negative."""
        payload = {
            'application': 'Pipe',
            'strength': 'Medium',
            'temperature': 500,  # Exceeds max 400
            'weight': 'Low',
            'chemical_resistance': 'High',
            'cost': 'Low'
        }
        response = self.client.post('/api/recommend', json=payload)
        self.assertEqual(response.status_code, 400)

        # Negative temperature
        payload['temperature'] = -10
        response = self.client.post('/api/recommend', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_12_api_recommend_validation_invalid_category(self):
        """Test rejection of unauthorized category values."""
        payload = {
            'application': 'Pipe',
            'strength': 'SuperStrong',  # Not in Low/Medium/High
            'temperature': 60,
            'weight': 'Low',
            'chemical_resistance': 'High',
            'cost': 'Low'
        }
        response = self.client.post('/api/recommend', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_13_database_history_persistence(self):
        """Test that recommendation writes history record to MySQL."""
        with app.app_context():
            initial_count = RecommendationHistory.query.count()
            payload = {
                'application': 'Automotive Dashboard Housing',
                'strength': 'Medium',
                'temperature': 85,
                'weight': 'Low',
                'chemical_resistance': 'Medium',
                'cost': 'Medium'
            }
            response = self.client.post('/api/recommend', json=payload)
            self.assertEqual(response.status_code, 200)
            new_count = RecommendationHistory.query.count()
            self.assertEqual(new_count, initial_count + 1)

            latest = RecommendationHistory.query.order_by(RecommendationHistory.id.desc()).first()
            self.assertEqual(latest.application, 'Automotive Dashboard Housing')

    def test_14_seed_idempotency(self):
        """Test that seed_database does not duplicate existing materials."""
        with app.app_context():
            initial_count = Polymer.query.count()
            inserted, total = seed_database()
            self.assertEqual(inserted, 0)
            self.assertEqual(total, initial_count)

    def test_15_no_secrets_in_tracked_files(self):
        """Verify no hardcoded credentials exist in tracked python files."""
        bad_patterns = ['A' + 'KIA', 'BEGIN RSA' + ' PRIVATE KEY', 'SECRET_' + 'KEY = "sk_']
        for root, dirs, files in os.walk(PROJECT_ROOT):
            if any(p in root for p in ['venv', '.git', '__pycache__', 'tests']):
                continue
            for file in files:
                if file.endswith(('.py', '.json', '.yml', '.yaml')):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()
                        for pattern in bad_patterns:
                            self.assertNotIn(pattern, text, f"Potential secret {pattern} found in {file}")


if __name__ == '__main__':
    unittest.main()
