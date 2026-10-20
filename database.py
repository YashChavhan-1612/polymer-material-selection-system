from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


def utc_now():
    """Return timezone-aware current UTC datetime."""
    return datetime.now(timezone.utc)

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
    created_at = db.Column(db.DateTime, default=utc_now)
    
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
    created_at = db.Column(db.DateTime, default=utc_now)


# ============================================================
# Default Seed Polymer Data
# ============================================================

DEFAULT_POLYMERS = [
    {
        'name': 'HDPE',
        'category': 'Thermoplastic',
        'description': 'High-Density Polyethylene is a strong, durable thermoplastic with excellent chemical resistance and good impact strength. It is widely used in packaging, pipes and containers.',
        'strength': 25.00,
        'max_temperature': 120,
        'density': 0.950,
        'chemical_resistance': 'Excellent',
        'cost': 'Low',
        'advantages': 'Excellent chemical resistance, good impact strength, low cost, moisture resistant, recyclable',
        'limitations': 'Lower stiffness compared to some engineering plastics, limited high-temperature performance, can stress-crack under certain conditions',
        'applications': 'Bottles, pipes, tanks, cutting boards, geomembranes, toys',
        'image_url': None
    },
    {
        'name': 'PP',
        'category': 'Thermoplastic',
        'description': 'Polypropylene is a versatile thermoplastic known for its excellent chemical resistance, low density and good fatigue resistance. It is one of the most widely used plastics.',
        'strength': 30.00,
        'max_temperature': 100,
        'density': 0.905,
        'chemical_resistance': 'Excellent',
        'cost': 'Low',
        'advantages': 'Low density, excellent chemical resistance, good fatigue resistance, low cost, living hinge capability',
        'limitations': 'Poor resistance to UV (without additives), becomes brittle at low temperatures, moderate impact strength',
        'applications': 'Automotive parts, packaging, living hinges, medical devices, textiles, containers',
        'image_url': None
    },
    {
        'name': 'PVC',
        'category': 'Thermoplastic',
        'description': 'Polyvinyl Chloride is a widely used thermoplastic available in rigid and flexible forms. It offers good chemical resistance and is commonly used in construction and piping.',
        'strength': 50.00,
        'max_temperature': 60,
        'density': 1.400,
        'chemical_resistance': 'Good',
        'cost': 'Low',
        'advantages': 'Good chemical resistance, high strength, flame retardant (with additives), low cost, versatile (rigid & flexible)',
        'limitations': 'Limited high-temperature resistance, contains chlorine (environmental concerns), can release HCl when burned',
        'applications': 'Pipes, window frames, flooring, cables, medical tubing, credit cards',
        'image_url': None
    },
    {
        'name': 'PS',
        'category': 'Thermoplastic',
        'description': 'Polystyrene is a rigid, transparent thermoplastic that is easy to process. It is commonly used in disposable products and packaging.',
        'strength': 40.00,
        'max_temperature': 70,
        'density': 1.050,
        'chemical_resistance': 'Fair',
        'cost': 'Low',
        'advantages': 'Low cost, easy to process, good dimensional stability, transparent grades available, rigid',
        'limitations': 'Brittle, poor chemical resistance to many solvents, limited temperature resistance, environmental concerns (single-use)',
        'applications': 'Disposable cutlery, CD cases, packaging foam, laboratory ware, insulation',
        'image_url': None
    },
    {
        'name': 'PET',
        'category': 'Thermoplastic',
        'description': 'Polyethylene Terephthalate is a strong, transparent thermoplastic with excellent barrier properties. It is the most common material for beverage bottles.',
        'strength': 70.00,
        'max_temperature': 70,
        'density': 1.380,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'Excellent strength and stiffness, good barrier properties, transparent, recyclable, good chemical resistance',
        'limitations': 'Limited high-temperature performance, can crystallize and become opaque, moisture sensitive during processing',
        'applications': 'Beverage bottles, food packaging, textile fibers (polyester), films, engineering components',
        'image_url': None
    },
    {
        'name': 'Nylon 6',
        'category': 'Engineering Thermoplastic',
        'description': 'Nylon 6 (Polyamide 6) is a strong engineering thermoplastic with excellent wear resistance, toughness and good chemical resistance to many substances.',
        'strength': 80.00,
        'max_temperature': 150,
        'density': 1.140,
        'chemical_resistance': 'Good',
        'cost': 'High',
        'advantages': 'High strength and toughness, excellent wear resistance, good chemical resistance, good fatigue resistance',
        'limitations': 'Absorbs moisture (affects dimensions and properties), higher cost, requires drying before processing',
        'applications': 'Gears, bearings, automotive parts, textiles, power tool housings, fasteners',
        'image_url': None
    },
    {
        'name': 'ABS',
        'category': 'Engineering Thermoplastic',
        'description': 'Acrylonitrile Butadiene Styrene is a tough, impact-resistant engineering thermoplastic with good dimensional stability and surface finish.',
        'strength': 40.00,
        'max_temperature': 90,
        'density': 1.050,
        'chemical_resistance': 'Fair',
        'cost': 'Medium',
        'advantages': 'Excellent impact resistance, good toughness, easy to process, good surface finish, dimensional stability',
        'limitations': 'Poor resistance to solvents and UV (without additives), moderate chemical resistance, not suitable for high temperatures',
        'applications': 'Automotive interior parts, electronic housings, LEGO bricks, luggage, protective equipment',
        'image_url': None
    },
    {
        'name': 'LDPE',
        'category': 'Thermoplastic',
        'description': 'Low-Density Polyethylene is a flexible thermoplastic with excellent moisture resistance, chemical resistance and good impact strength.',
        'strength': 28.00,
        'max_temperature': 80,
        'density': 0.920,
        'chemical_resistance': 'Excellent',
        'cost': 'Low',
        'advantages': 'Flexible, excellent moisture resistance, good chemical resistance, low cost, good impact strength',
        'limitations': 'Low stiffness, limited temperature resistance, relatively low tensile strength',
        'applications': 'Plastic bags, films, squeeze bottles, liners, tubing, flexible packaging',
        'image_url': None
    }
]


# ============================================================
# Helper functions
# ============================================================

def get_all_polymers():
    """Retrieve all polymer materials from the database."""
    return Polymer.query.order_by(Polymer.id).all()


def get_polymer_by_id(polymer_id):
    """Retrieve a single polymer by its ID using modern SQLAlchemy session get."""
    return db.session.get(Polymer, polymer_id)


def get_polymer_by_name(name):
    """Retrieve a single polymer by its name (case-insensitive)."""
    return Polymer.query.filter(Polymer.name.ilike(name)).first()


def seed_database(force=False):
    """Seed the database with initial polymer data safely if not already seeded."""
    count = Polymer.query.count()
    if count > 0 and not force:
        return 0, count

    inserted = 0
    for p_data in DEFAULT_POLYMERS:
        existing = Polymer.query.filter_by(name=p_data['name']).first()
        if not existing:
            p = Polymer(**p_data)
            db.session.add(p)
            inserted += 1
    db.session.commit()
    return inserted, Polymer.query.count()
