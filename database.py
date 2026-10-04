from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create the SQLAlchemy database instance
db = SQLAlchemy()


class Polymer(db.Model):
    """SQLAlchemy model for the polymers table."""
    
    __tablename__ = 'polymers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    strength = db.Column(db.Numeric(10, 2), nullable=False)
    max_temperature = db.Column(db.Integer, nullable=False)
    density = db.Column(db.Numeric(6, 3), nullable=False)
    chemical_resistance = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.String(20), nullable=False)
    advantages = db.Column(db.Text)
    limitations = db.Column(db.Text)
    applications = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert the model instance to a dictionary (for JSON responses)."""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'strength': float(self.strength) if self.strength is not None else None,
            'max_temperature': self.max_temperature,
            'density': float(self.density) if self.density is not None else None,
            'chemical_resistance': self.chemical_resistance,
            'cost': self.cost,
            'advantages': self.advantages,
            'limitations': self.limitations,
            'applications': self.applications,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class RecommendationHistory(db.Model):
    """SQLAlchemy model for the recommendation_history table."""
    
    __tablename__ = 'recommendation_history'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    application = db.Column(db.String(150), nullable=False)
    required_strength = db.Column(db.String(50), nullable=False)
    operating_temperature = db.Column(db.Integer, nullable=False)
    weight_requirement = db.Column(db.String(50), nullable=False)
    chemical_resistance = db.Column(db.String(50), nullable=False)
    cost_preference = db.Column(db.String(50), nullable=False)
    recommendation_result = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ============================================================
# Helper functions
# ============================================================

def get_all_polymers():
    """Retrieve all polymer materials from the database."""
    return Polymer.query.order_by(Polymer.id).all()


def get_polymer_by_id(polymer_id):
    """Retrieve a single polymer by its ID."""
    return Polymer.query.get(polymer_id)


def get_polymer_by_name(name):
    """Retrieve a single polymer by its name (case-insensitive)."""
    return Polymer.query.filter(Polymer.name.ilike(name)).first()