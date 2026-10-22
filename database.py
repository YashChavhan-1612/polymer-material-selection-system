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
        'description': 'High-Density Polyethylene is a tough, highly crystalline commodity polymer offering superior chemical inertness, high moisture barrier, and excellent impact resistance.',
        'strength': 28.00,
        'max_temperature': 120,
        'density': 0.955,
        'chemical_resistance': 'Excellent',
        'cost': 'Low',
        'advantages': 'Outstanding chemical resistance, zero moisture absorption, high impact resistance, fully recyclable, very low cost.',
        'limitations': 'Subject to environmental stress cracking under surfactants, high thermal expansion, low mechanical stiffness at elevated temperatures.',
        'applications': 'Water pipes, chemical storage tanks, food packaging, milk bottles, gas distribution piping, geomembranes, cutting boards.',
        'image_url': None
    },
    {
        'name': 'LDPE',
        'category': 'Thermoplastic',
        'description': 'Low-Density Polyethylene is a highly branched, ductile thermoplastic known for its exceptional flexibility, high clarity in thin films, and waterproof characteristics.',
        'strength': 18.00,
        'max_temperature': 80,
        'density': 0.920,
        'chemical_resistance': 'Excellent',
        'cost': 'Low',
        'advantages': 'Exceptional flexibility and elongation, low density, high moisture barrier, great electrical insulation, economical.',
        'limitations': 'Low tensile strength, low maximum continuous temperature, vulnerable to oil absorption and outdoor UV degradation.',
        'applications': 'Plastic bags, flexible squeeze bottles, packaging films, wire and cable jacketing, flexible tubing, agricultural mulch.',
        'image_url': None
    },
    {
        'name': 'LLDPE',
        'category': 'Thermoplastic',
        'description': 'Linear Low-Density Polyethylene provides higher tensile strength, puncture resistance, and environmental stress crack resistance than conventional LDPE.',
        'strength': 24.00,
        'max_temperature': 90,
        'density': 0.925,
        'chemical_resistance': 'Excellent',
        'cost': 'Low',
        'advantages': 'High puncture and tear resistance, superior elongation, excellent impact strength down to subzero temperatures.',
        'limitations': 'Narrower heat-sealing temperature window than LDPE, low surface hardness, low heat deflection.',
        'applications': 'Stretch film, pallet wrap, heavy-duty shipping bags, rotational molding containers, geomembranes, flexible tubing.',
        'image_url': None
    },
    {
        'name': 'UHMWPE',
        'category': 'High-Performance Polyethylene',
        'description': 'Ultra-High Molecular Weight Polyethylene features extremely long polymer chains giving it the highest impact strength and lowest sliding friction of any thermoplastic.',
        'strength': 42.00,
        'max_temperature': 90,
        'density': 0.940,
        'chemical_resistance': 'Excellent',
        'cost': 'Medium',
        'advantages': 'Extreme wear and abrasion resistance, near-zero friction coefficient, self-lubricating, virtually unbreakable under impact.',
        'limitations': 'Cannot be processed by conventional injection molding; requires compression molding or ram extrusion; low melt temperature.',
        'applications': 'Chute liners, conveyor wear strips, orthopedic joint implants, ballistic body armor fibers, marine fender pads, mechanical gears.',
        'image_url': None
    },
    {
        'name': 'PP',
        'category': 'Thermoplastic',
        'description': 'Polypropylene is a lightweight semi-crystalline polymer with good chemical resistance, high stiffness, and unparalleled living hinge fatigue resistance.',
        'strength': 34.00,
        'max_temperature': 105,
        'density': 0.905,
        'chemical_resistance': 'Excellent',
        'cost': 'Low',
        'advantages': 'Lowest density among commodity plastics, exceptional fatigue endurance (living hinges), autoclavable, excellent chemical barrier.',
        'limitations': 'Susceptible to UV degradation without carbon black or stabilizers; becomes brittle below 0 deg C; difficult to bond with adhesives.',
        'applications': 'Automotive bumpers, living hinges, food containers, medical syringes, battery casings, labware, chemical piping.',
        'image_url': None
    },
    {
        'name': 'PP-Random Copolymer',
        'category': 'Thermoplastic',
        'description': 'Random Copolymer Polypropylene incorporates ethylene units into the chain to dramatically boost optical clarity and drop impact ductility.',
        'strength': 30.00,
        'max_temperature': 95,
        'density': 0.900,
        'chemical_resistance': 'Good',
        'cost': 'Low',
        'advantages': 'High optical transparency, smooth surface finish, good impact resistance at ambient temperatures, low extraction levels.',
        'limitations': 'Slightly lower stiffness and melting point than PP homopolymer, moderate scratch resistance.',
        'applications': 'Clear food storage containers, medical syringes, pharmaceutical vials, consumer housewares, cosmetic jars.',
        'image_url': None
    },
    {
        'name': 'PVC-Rigid',
        'category': 'Thermoplastic',
        'description': 'Rigid Polyvinyl Chloride (uPVC) is an unplasticized structural polymer with high modulus, inherent flame retardancy, and excellent weatherability.',
        'strength': 55.00,
        'max_temperature': 60,
        'density': 1.420,
        'chemical_resistance': 'Good',
        'cost': 'Low',
        'advantages': 'Inherently self-extinguishing flame resistance, high mechanical stiffness, outstanding outdoor weatherability, economical.',
        'limitations': 'Low heat deflection temperature, releases corrosive hydrogen chloride gas if overheated, brittle under shock at cold temperatures.',
        'applications': 'Municipal water pipes, window profiles, exterior building siding, chemical ducting, drainage conduits, electrical junction boxes.',
        'image_url': None
    },
    {
        'name': 'PVC-Flexible',
        'category': 'Thermoplastic',
        'description': 'Plasticized Polyvinyl Chloride contains plasticizers to deliver rubber-like flexibility, tear strength, and electrical insulation properties.',
        'strength': 20.00,
        'max_temperature': 60,
        'density': 1.300,
        'chemical_resistance': 'Good',
        'cost': 'Low',
        'advantages': 'Highly pliable, excellent dielectric insulation, fire retardant, easily weldable, resistant to moisture and acids.',
        'limitations': 'Plasticizer migration over time can cause embrittlement; poor resistance to aromatic hydrocarbons and chlorinated solvents.',
        'applications': 'Electrical cable jacketing, medical IV tubing, blood bags, vinyl flooring, protective boots, inflatable curtains.',
        'image_url': None
    },
    {
        'name': 'PS',
        'category': 'Thermoplastic',
        'description': 'General Purpose Polystyrene (GPPS) is an amorphous glassy polymer known for high optical clarity, excellent dimensional stability, and easy molding.',
        'strength': 45.00,
        'max_temperature': 70,
        'density': 1.050,
        'chemical_resistance': 'Fair',
        'cost': 'Low',
        'advantages': 'Crystal clear optical transparency, high surface gloss, rigid and dimensionally stable, low mold shrinkage.',
        'limitations': 'Notoriously brittle under impact, poor solvent resistance, low heat resistance, prone to stress cracking.',
        'applications': 'Petri dishes, disposable cutlery, CD jewel cases, cosmetic packaging, retail display stands, diagnostic trays.',
        'image_url': None
    },
    {
        'name': 'HIPS',
        'category': 'Thermoplastic',
        'description': 'High Impact Polystyrene combines polystyrene with polybutadiene rubber grafting to provide good impact resistance while keeping easy thermoformability.',
        'strength': 30.00,
        'max_temperature': 75,
        'density': 1.040,
        'chemical_resistance': 'Fair',
        'cost': 'Low',
        'advantages': 'Substantially improved impact toughness compared to GPPS, excellent thermoforming characteristics, low cost, easy to paint.',
        'limitations': 'Opaque translucent white finish, poor outdoor UV resistance without additives, vulnerable to aromatic solvents.',
        'applications': 'Refrigerator interior door liners, consumer electronic housings, thermoformed food packaging trays, toys, signboards.',
        'image_url': None
    },
    {
        'name': 'EPS',
        'category': 'Cellular Polymer',
        'description': 'Expanded Polystyrene is a closed-cell cellular foam consisting of 98% air, engineered for superior thermal insulation and shock-absorbing cushioning.',
        'strength': 8.00,
        'max_temperature': 75,
        'density': 0.030,
        'chemical_resistance': 'Fair',
        'cost': 'Low',
        'advantages': 'Ultra-lightweight, outstanding shock dampening, superior thermal insulation factor, moisture resistant, low cost.',
        'limitations': 'Very low mechanical shear and tensile strength, dissolved easily by gasoline and organic solvents, bulky disposal footprint.',
        'applications': 'Building foundation insulation panels, protective packaging corners for electronics, bicycle helmets, cooler boxes.',
        'image_url': None
    },
    {
        'name': 'PET',
        'category': 'Thermoplastic',
        'description': 'Polyethylene Terephthalate is a strong, lightweight semi-crystalline polyester offering exceptional carbon dioxide barrier properties and optical clarity.',
        'strength': 75.00,
        'max_temperature': 70,
        'density': 1.380,
        'chemical_resistance': 'Good',
        'cost': 'Low',
        'advantages': 'Superb gas and moisture barrier, high tensile strength, high transparency in biaxially oriented state, universally recyclable.',
        'limitations': 'Subject to hydrolytic degradation during melt processing if not thoroughly dried; moderate continuous temperature resistance.',
        'applications': 'Carbonated beverage bottles, food jars, polyester textile fibers, food blister packs, strapping tape, optical films.',
        'image_url': None
    },
    {
        'name': 'PETG',
        'category': 'Thermoplastic',
        'description': 'Polyethylene Terephthalate Glycol-modified is an amorphous polyester that does not crystallize, offering great clarity, toughness, and 3D printability.',
        'strength': 50.00,
        'max_temperature': 65,
        'density': 1.270,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'Glass-like transparency, high impact strength even at low temperatures, easy thermoforming without pre-drying, excellent 3D print layer bonding.',
        'limitations': 'Lower surface hardness than acrylic, prone to scratching, low glass transition temperature.',
        'applications': 'Medical equipment packaging, point-of-sale display stands, 3D printing filaments, electronic product covers, machine guards.',
        'image_url': None
    },
    {
        'name': 'ABS',
        'category': 'Engineering Thermoplastic',
        'description': 'Acrylonitrile Butadiene Styrene is an opaque engineering terpolymer providing balanced toughness, dimensional stability, and electroplating capability.',
        'strength': 45.00,
        'max_temperature': 85,
        'density': 1.050,
        'chemical_resistance': 'Fair',
        'cost': 'Medium',
        'advantages': 'Exceptional impact resistance, high dimensional stability, easy to injection mold and machine, excellent electroplating and painting receptivity.',
        'limitations': 'Moderate chemical resistance to solvents and esters; poor resistance to direct sunlight (UV) without stabilizers.',
        'applications': 'Automotive instrument panels, power tool housings, computer monitors, consumer electronics, LEGO bricks, protective helmets.',
        'image_url': None
    },
    {
        'name': 'SAN',
        'category': 'Engineering Thermoplastic',
        'description': 'Styrene Acrylonitrile is a transparent copolymer providing higher heat resistance, tensile strength, and chemical resistance than standard polystyrene.',
        'strength': 68.00,
        'max_temperature': 85,
        'density': 1.080,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'High optical transparency, superior surface scratch resistance, higher heat tolerance than PS, good grease resistance.',
        'limitations': 'Moderate impact ductility, yellowing propensity with thermal degradation, sensitive to stress cracking under cyclic loads.',
        'applications': 'Blender jugs, refrigerator crisper drawers, cosmetic containers, water filter housings, automotive tail-lamp lenses.',
        'image_url': None
    },
    {
        'name': 'ASA',
        'category': 'Engineering Thermoplastic',
        'description': 'Acrylonitrile Styrene Acrylate replaces the butadiene rubber in ABS with acrylate rubber to achieve outstanding outdoor UV and weather resistance.',
        'strength': 48.00,
        'max_temperature': 90,
        'density': 1.070,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'Remarkable outdoor UV weather resistance, retains color and gloss without painting, good impact resistance, high thermal stability.',
        'limitations': 'Slightly higher cost than ABS, hygroscopic requiring drying before processing, moderate solvent resistance.',
        'applications': 'Automotive exterior side mirrors, radiator grilles, exterior architectural siding, outdoor electrical enclosures, marine equipment.',
        'image_url': None
    },
    {
        'name': 'Nylon 6',
        'category': 'Engineering Thermoplastic',
        'description': 'Polyamide 6 (Nylon 6) is a semi-crystalline engineering thermoplastic known for high mechanical strength, good dampening, and high wear resistance.',
        'strength': 80.00,
        'max_temperature': 120,
        'density': 1.140,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'High toughness and tensile strength, excellent fatigue endurance, self-lubricating wear properties, good resistance to fuels and oils.',
        'limitations': 'High moisture absorption reduces dimensional stability and tensile modulus while increasing impact flexibility.',
        'applications': 'Gears, sliding bearings, automotive engine covers, power tool housings, textile fibers, cable zip ties, fasteners.',
        'image_url': None
    },
    {
        'name': 'Nylon 66',
        'category': 'Engineering Thermoplastic',
        'description': 'Polyamide 66 provides higher stiffness, higher melting point (265 deg C), and lower creep under high loads than Nylon 6.',
        'strength': 85.00,
        'max_temperature': 130,
        'density': 1.150,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'Higher heat deflection temperature and tensile modulus than PA6, excellent abrasion resistance, great hydrocarbon resistance.',
        'limitations': 'Absorbs ambient moisture leading to dimensional expansion, requires thorough drying before molding, relatively high mold shrinkage.',
        'applications': 'Under-the-hood automotive radiator tanks, mechanical gears, bearing cages, circuit breaker housings, industrial valves, cable clips.',
        'image_url': None
    },
    {
        'name': 'Nylon 11',
        'category': 'Engineering Thermoplastic',
        'description': 'Polyamide 11 is a bio-based engineering polymer derived from castor oil, offering extremely low moisture absorption and superior cold impact toughness.',
        'strength': 55.00,
        'max_temperature': 110,
        'density': 1.040,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Significantly lower moisture absorption than PA6/66, outstanding dimensional stability, exceptional flexibility down to -40 deg C, renewable source.',
        'limitations': 'Lower tensile strength and stiffness than PA66, higher price point due to specialty precursor synthesis.',
        'applications': 'Automotive fuel and air-brake lines, offshore oil and gas flexible umbilicals, 3D printing SLS powder, ski boot shells.',
        'image_url': None
    },
    {
        'name': 'Nylon 12',
        'category': 'Engineering Thermoplastic',
        'description': 'Polyamide 12 has the lowest moisture absorption and lowest density of all standard polyamides, guaranteeing high dimensional precision in humid environments.',
        'strength': 50.00,
        'max_temperature': 105,
        'density': 1.020,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Minimal moisture uptake, superior dimensional precision, high burst pressure resistance, excellent dampening of vibration and noise.',
        'limitations': 'Lower mechanical strength and heat resistance than PA66, relatively high cost.',
        'applications': 'Automotive fuel delivery lines, pneumatic tubing, precision water meter housings, athletic equipment, SLS 3D printed functional prototypes.',
        'image_url': None
    },
    {
        'name': 'Nylon 46',
        'category': 'High-Temp Polyamide',
        'description': 'Polyamide 46 has an exceptionally high symmetrical chain structure, yielding rapid crystallization, high melting point (295 deg C), and high stiffness at high heat.',
        'strength': 100.00,
        'max_temperature': 160,
        'density': 1.180,
        'chemical_resistance': 'Good',
        'cost': 'High',
        'advantages': 'Exceptional mechanical stiffness and strength retention at elevated temperatures up to 160 deg C, outstanding fatigue resistance.',
        'limitations': 'Very high moisture absorption rate requiring careful dry-room handling, premium price tag.',
        'applications': 'Automotive starter motor gears, timing chain tensioner guides, electric motor brush holders, heavy-duty clutch components.',
        'image_url': None
    },
    {
        'name': 'POM-C',
        'category': 'Engineering Thermoplastic',
        'description': 'Polyoxymethylene Copolymer (Acetal Copolymer) is an engineering plastic renowned for high dimensional stability, low friction, and resistance to thermal degradation.',
        'strength': 65.00,
        'max_temperature': 100,
        'density': 1.410,
        'chemical_resistance': 'Excellent',
        'cost': 'Medium',
        'advantages': 'Exceptional dimensional stability, very low moisture uptake, low friction coefficient, excellent resistance to hydrolysis and alkaline chemicals.',
        'limitations': 'High mold shrinkage, difficult to bond without chemical etching, susceptible to degradation by strong oxidizing acids.',
        'applications': 'Precision gears, conveyor rollers, fuel sender units, water filtration valves, aerosol valves, zipper fasteners.',
        'image_url': None
    },
    {
        'name': 'POM-H',
        'category': 'Engineering Thermoplastic',
        'description': 'Polyoxymethylene Homopolymer (Delrin) provides higher tensile strength, rigidity, and fatigue endurance than POM copolymer.',
        'strength': 75.00,
        'max_temperature': 105,
        'density': 1.430,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'Higher tensile strength, higher surface hardness, superior fatigue resistance, low sliding wear against metals.',
        'limitations': 'Susceptible to centerline porosity in thick cross-sections, lower resistance to strong hot bases than POM copolymer.',
        'applications': 'High-load gear trains, actuator cams, safety belt lock mechanisms, sliding door rollers, musical instrument components.',
        'image_url': None
    },
    {
        'name': 'Polycarbonate',
        'category': 'Engineering Thermoplastic',
        'description': 'Polycarbonate is an amorphous high-performance thermoplastic offering near-glass transparency, remarkable impact toughness, and high heat resistance.',
        'strength': 65.00,
        'max_temperature': 125,
        'density': 1.200,
        'chemical_resistance': 'Fair',
        'cost': 'Medium',
        'advantages': 'Virtually unbreakable impact resistance, crystal clarity (88% light transmission), high heat deflection temperature, flame retardant grades available.',
        'limitations': 'Susceptible to stress cracking from solvents and alkaline cleaners; low scratch resistance without hardcoatings.',
        'applications': 'Bulletproof security glazing, automotive headlamp lenses, safety goggles, electronic display screens, medical device housings.',
        'image_url': None
    },
    {
        'name': 'PMMA',
        'category': 'Engineering Thermoplastic',
        'description': 'Polymethyl Methacrylate (Acrylic) is an amorphous optical plastic known for exceptional light transmission (92%), UV stability, and surface gloss.',
        'strength': 70.00,
        'max_temperature': 85,
        'density': 1.190,
        'chemical_resistance': 'Fair',
        'cost': 'Medium',
        'advantages': 'Highest optical clarity of all plastics, outstanding natural UV resistance without yellowing, high scratch resistance compared to PC.',
        'limitations': 'Brittle under impact compared to polycarbonate, poor chemical resistance to acetone and aromatic hydrocarbons.',
        'applications': 'Automotive tail-light clusters, commercial signage, aircraft window glazing, optical lenses, aquarium display panels, daylight fixtures.',
        'image_url': None
    },
    {
        'name': 'PBT',
        'category': 'Engineering Thermoplastic',
        'description': 'Polybutylene Terephthalate is a semi-crystalline polyester characterized by fast crystallization cycles, high electrical resistance, and low moisture absorption.',
        'strength': 60.00,
        'max_temperature': 120,
        'density': 1.310,
        'chemical_resistance': 'Excellent',
        'cost': 'Medium',
        'advantages': 'Rapid molding cycle times, excellent dielectric breakdown resistance, low moisture absorption, high dimensional stability.',
        'limitations': 'Susceptible to hot water hydrolysis above 60 deg C, notch-sensitive under impact without glass fiber reinforcement.',
        'applications': 'Automotive ignition coil bobbins, electrical plug connectors, keyboard keycaps, fiber optic buffer tubes, distributor caps.',
        'image_url': None
    },
    {
        'name': 'PPE/PPO',
        'category': 'Engineering Thermoplastic',
        'description': 'Polyphenylene Ether is an amorphous high-heat polymer with negligible moisture absorption and very stable electrical properties across frequencies.',
        'strength': 65.00,
        'max_temperature': 110,
        'density': 1.060,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'Extremely low moisture absorption (<0.07%), very high hydrolytic stability, dimensional precision, flame retardant.',
        'limitations': 'High melt viscosity requires blending with polystyrene (Noryl) to achieve good melt processability.',
        'applications': 'Water pump impellers, solar junction boxes, telecommunication relay housings, automotive wheel covers, battery brackets.',
        'image_url': None
    },
    {
        'name': 'PEEK',
        'category': 'High-Performance Polymer',
        'description': 'Polyether Ether Ketone is an elite semi-crystalline polymer providing exceptional strength, continuous service at 250 deg C, and chemical inertness.',
        'strength': 100.00,
        'max_temperature': 250,
        'density': 1.300,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Continuous operation at 250 deg C, outstanding chemical resistance across nearly all acids and bases, gamma radiation resistant, low smoke/flame.',
        'limitations': 'Very high cost, high melt processing temperatures (>370 deg C) requiring specialized mold heating equipment.',
        'applications': 'Aerospace structural brackets, oil and gas downhole drilling tools, spine implant cages, semiconductor wafer carriers, engine bearings.',
        'image_url': None
    },
    {
        'name': 'PEKK',
        'category': 'High-Performance Polymer',
        'description': 'Polyetherketoneketone offers higher glass transition temperature, higher compressive strength, and slower crystallization kinetics than PEEK.',
        'strength': 110.00,
        'max_temperature': 260,
        'density': 1.310,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Higher Tg (160 deg C) than PEEK, superior compressive and wear resistance, flame retardant (UL94 V-0), ideal for 3D printing.',
        'limitations': 'Premium cost, requires specialized high-temperature processing equipment.',
        'applications': 'Aerospace interior panels, carbon fiber composite matrices, oilfield valve seals, high-voltage electrical isolators.',
        'image_url': None
    },
    {
        'name': 'PEI',
        'category': 'High-Performance Polymer',
        'description': 'Polyetherimide (Ultem) is an amorphous amber-transparent polymer providing high heat resistance, inherent flame retardancy, and high dielectric strength.',
        'strength': 105.00,
        'max_temperature': 170,
        'density': 1.270,
        'chemical_resistance': 'Good',
        'cost': 'High',
        'advantages': 'Continuous operating temperature of 170 deg C, high dielectric strength, intrinsically flame retardant with low smoke generation.',
        'limitations': 'High raw material price, sensitive to certain chlorinated and ketone solvents under mechanical stress.',
        'applications': 'Aircraft interior lighting housings, medical sterilizer trays, fiber optic connectors, printed circuit test fixtures.',
        'image_url': None
    },
    {
        'name': 'PPS',
        'category': 'High-Performance Polymer',
        'description': 'Polyphenylene Sulfide is a semi-crystalline polymer noted for supreme chemical inertness, high modulus, and zero known solvents below 200 deg C.',
        'strength': 85.00,
        'max_temperature': 220,
        'density': 1.350,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Continuous temperature capability to 220 deg C, no known solvent below 200 deg C, inherently flame retardant, high dimensional precision.',
        'limitations': 'Brittle in unfilled form (almost always compounded with glass or mineral fillers), abrasive to standard tooling.',
        'applications': 'Automotive engine coolant pumps, exhaust gas recirculation valves, industrial chemical pump casings, electrical motor insulators.',
        'image_url': None
    },
    {
        'name': 'PES',
        'category': 'High-Performance Polymer',
        'description': 'Polyethersulfone is an amorphous transparent amber plastic offering continuous high-temperature endurance, high creep resistance, and sterilizability.',
        'strength': 85.00,
        'max_temperature': 180,
        'density': 1.370,
        'chemical_resistance': 'Good',
        'cost': 'High',
        'advantages': 'High continuous service temperature of 180 deg C, withstands repeated steam sterilization cycles, high electrical insulation.',
        'limitations': 'Vulnerable to stress cracking in the presence of polar organic solvents, relatively expensive.',
        'applications': 'Dialysis membrane filters, medical surgical lamp reflectors, aircraft interior window surrounds, hot water meter housings.',
        'image_url': None
    },
    {
        'name': 'PSU',
        'category': 'High-Performance Polymer',
        'description': 'Polysulfone is an amorphous rigid transparent thermoplastic known for exceptional hydrolytic stability in boiling water and repeated steam cycles.',
        'strength': 70.00,
        'max_temperature': 150,
        'density': 1.240,
        'chemical_resistance': 'Good',
        'cost': 'High',
        'advantages': 'Withstands repeated steam autoclaving, low creep under continuous load, transparent with slight amber hue, FDA food-contact compliant.',
        'limitations': 'Sensitive to aromatic hydrocarbons, esters, and ketones; requires high melt processing temperatures.',
        'applications': 'Medical surgical instrument handles, dairy equipment tubing manifolds, hot beverage dispenser valves, battery cell containers.',
        'image_url': None
    },
    {
        'name': 'PPSU',
        'category': 'High-Performance Polymer',
        'description': 'Polyphenylsulfone (Radel) is a high-performance sulfone polymer offering the highest impact toughness and chemical resistance in the sulfone family.',
        'strength': 75.00,
        'max_temperature': 180,
        'density': 1.290,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Survives over 1,000 steam sterilization cycles without loss of impact toughness, high chemical resistance, high heat deflection.',
        'limitations': 'Premium cost among sulfone polymers, high mold temperatures required.',
        'applications': 'Surgical trial implants, dental tool handles, aircraft galley food service carts, hot water plumbing manifolds.',
        'image_url': None
    },
    {
        'name': 'PAI',
        'category': 'Ultra-High-Performance Polymer',
        'description': 'Polyamide-imide (Torlon) provides the highest mechanical tensile and compressive strength of any unreinforced thermoplastic up to 260 deg C.',
        'strength': 150.00,
        'max_temperature': 260,
        'density': 1.410,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Extreme mechanical strength up to 260 deg C, extraordinary wear and friction performance, unmatched dimensional creep resistance.',
        'limitations': 'Requires a lengthy post-curing thermal cycle (several days) to achieve full molecular weight; very high cost.',
        'applications': 'Transmission thrust washers, aerospace mechanical actuators, labyrinth seals, plasma torch insulators, semiconductor test sockets.',
        'image_url': None
    },
    {
        'name': 'Polyimide-Thermoset',
        'category': 'High-Performance Thermoset',
        'description': 'Thermoset Polyimide (Vespel SP-1) is a non-melting polymeric material capable of continuous operation from cryogenic temperatures up to 300 deg C.',
        'strength': 90.00,
        'max_temperature': 300,
        'density': 1.430,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Continuous operation at 300 deg C (short excursions to 480 deg C), zero melt point, high vacuum outgassing resistance, self-lubricating.',
        'limitations': 'Must be processed via powder metallurgy compaction and sintering; cannot be melt molded; very expensive.',
        'applications': 'Jet engine variable stator vane bushings, high-vacuum semiconductor wafer clamps, cryogenic valve seats, spacecraft thermal isolators.',
        'image_url': None
    },
    {
        'name': 'LCP',
        'category': 'High-Performance Polymer',
        'description': 'Liquid Crystal Polymer possesses rigid rod-like molecular chains that align during flow, providing incredible thin-wall flow and heat resistance.',
        'strength': 140.00,
        'max_temperature': 240,
        'density': 1.400,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Outstanding melt flow enabling ultra-thin walls (<0.2 mm), near-zero mold shrinkage, withstands SMT lead-free solder reflow temperatures.',
        'limitations': 'Weak weld-line strength due to high anisotropic molecular orientation, high directional property variance.',
        'applications': 'Ultra-miniature smartphone SIM card connectors, camera module brackets, fiber optic transceivers, automotive ignition components.',
        'image_url': None
    },
    {
        'name': 'PBI',
        'category': 'Ultra-High-Performance Polymer',
        'description': 'Polybenzimidazole offers the highest temperature resistance and mechanical strength retention of any commercially available polymer up to 340 deg C.',
        'strength': 160.00,
        'max_temperature': 340,
        'density': 1.300,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Highest continuous service temperature (340 deg C), extreme compressive strength, will not burn in normal air, low thermal conductivity.',
        'limitations': 'Extremely difficult to machine, very brittle, highly expensive, processed only via specialized sintered powder techniques.',
        'applications': 'Aerospace rocket motor nozzles, deep-well oil recovery valve seals, extreme-temperature glass handling suction cups.',
        'image_url': None
    },
    {
        'name': 'PAEK',
        'category': 'High-Performance Polymer',
        'description': 'Polyaryletherketone is an engineered ketone variant designed for optimized crystallization rates and high stiffness in continuous carbon fiber tapes.',
        'strength': 105.00,
        'max_temperature': 250,
        'density': 1.300,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Faster cycle times than standard PEEK, high toughness, superior fatigue strength in structural composite laminates.',
        'limitations': 'Requires specialized high-temperature consolidation tools, expensive raw polymer feedstock.',
        'applications': 'Aerospace composite fuselage stiffeners, military helicopter rotor components, primary structural composite brackets.',
        'image_url': None
    },
    {
        'name': 'PTFE',
        'category': 'Fluoropolymer',
        'description': 'Polytetrafluoroethylene (Teflon) is a fully fluorinated polymer offering near-total chemical inertness, extreme non-stick, and continuous service to 260 deg C.',
        'strength': 25.00,
        'max_temperature': 260,
        'density': 2.160,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Almost universal chemical inertness, lowest coefficient of friction among solids, broad temperature window (-200 to +260 deg C), non-stick.',
        'limitations': 'Subject to cold flow (creep) under continuous load, cannot be melt injection molded, low tensile strength, high density.',
        'applications': 'Chemical pipe gaskets, non-stick cooking surfaces, low-friction sleeve bearings, pharmaceutical valve diaphragms, high-frequency coax cable insulation.',
        'image_url': None
    },
    {
        'name': 'PVDF',
        'category': 'Fluoropolymer',
        'description': 'Polyvinylidene Fluoride is a high-purity melt-processable fluoropolymer with superior mechanical stiffness, chemical barrier, and UV resistance.',
        'strength': 50.00,
        'max_temperature': 150,
        'density': 1.780,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Melt processable via injection molding, high mechanical strength for a fluoropolymer, high purity (low extractables), piezoelectric grades.',
        'limitations': 'Attacked by strong fuming acids, ketones, and strong bases at high temperatures; high density.',
        'applications': 'Ultra-pure water piping for semiconductor fabs, chemical tank linings, lithium-ion battery binder membranes, outdoor architectural coatings.',
        'image_url': None
    },
    {
        'name': 'FEP',
        'category': 'Fluoropolymer',
        'description': 'Fluorinated Ethylene Propylene is a melt-processable copolymer of tetrafluoroethylene, retaining PTFE-like chemical resistance with optical clarity.',
        'strength': 22.00,
        'max_temperature': 200,
        'density': 2.150,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Fully melt processable, high optical clarity and UV transmission, continuous 200 deg C resistance, exceptional non-stick release.',
        'limitations': 'Lower continuous temperature than PTFE (200 vs 260 deg C), low tensile modulus, subject to creep under sustained pressure.',
        'applications': 'Plenum cable jacketing, chemical process sight glasses, 3D printing SLA resin vat release films, solar panel protective films.',
        'image_url': None
    },
    {
        'name': 'PFA',
        'category': 'Fluoropolymer',
        'description': 'Perfluoroalkoxy Alkane delivers the full 260 deg C heat and chemical performance of PTFE with the convenience of melt injection processability.',
        'strength': 28.00,
        'max_temperature': 260,
        'density': 2.150,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Continuous 260 deg C performance, melt injection moldable, extraordinary flex-fatigue life, ultra-high chemical purity.',
        'limitations': 'Very high cost, requires corrosion-resistant nickel-alloy tooling during melt processing due to trace fluorinated off-gassing.',
        'applications': 'Semiconductor chemical tubing, high-purity chemical valve bodies, fluid transfer fittings, heat exchanger tubing.',
        'image_url': None
    },
    {
        'name': 'ETFE',
        'category': 'Fluoropolymer',
        'description': 'Ethylene Tetrafluoroethylene combines fluoropolymer chemical resistance with high mechanical toughness, tear strength, and high light transmission.',
        'strength': 45.00,
        'max_temperature': 150,
        'density': 1.700,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'High light transmission (95%), self-cleaning exterior surface, exceptional tear and puncture resistance, 1% the weight of glass.',
        'limitations': 'Lower continuous heat capability than fully fluorinated polymers, specialized welding techniques required for installation.',
        'applications': 'Architectural stadium roofs (Allianz Arena, Eden Project), chemical pump impellers, wire and cable wrap, greenhouse membranes.',
        'image_url': None
    },
    {
        'name': 'ECTFE',
        'category': 'Fluoropolymer',
        'description': 'Ethylene Chlorotrifluoroethylene (Halar) is an engineered fluoropolymer with supreme surface smoothness, chemical resistance, and chlorine barrier.',
        'strength': 50.00,
        'max_temperature': 150,
        'density': 1.680,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Exceptional chemical resistance across broad pH scale (1-14), ultra-smooth surface preventing bacterial adhesion, high abrasion resistance.',
        'limitations': 'Higher price than PVDF, requires high melt processing temperatures.',
        'applications': 'Chemical exhaust ductwork, pulp and paper chlorine bleach piping, powder coating for aggressive chemical tanks, pharmaceutical fluid systems.',
        'image_url': None
    },
    {
        'name': 'PCTFE',
        'category': 'Fluoropolymer',
        'description': 'Polychlorotrifluoroethylene provides the lowest water vapor transmission rate of any polymer and maintains ductility down to cryogenic temperatures (-240 deg C).',
        'strength': 40.00,
        'max_temperature': 150,
        'density': 2.120,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Lowest moisture and gas vapor permeability among all plastics, zero outgassing, retains mechanical seal elasticity at liquid nitrogen temperatures.',
        'limitations': 'Extremely sensitive to thermal degradation during molding; high cost.',
        'applications': 'Cryogenic liquid oxygen and nitrogen valve seats, pharmaceutical moisture-barrier blister packaging (Aclar), aerospace aerospace fuel seals.',
        'image_url': None
    },
    {
        'name': 'PVF',
        'category': 'Fluoropolymer',
        'description': 'Polyvinyl Fluoride (Tedlar) is a specialty fluoropolymer film known for decades-long outdoor weatherability, graffiti resistance, and flame barrier.',
        'strength': 70.00,
        'max_temperature': 110,
        'density': 1.450,
        'chemical_resistance': 'Good',
        'cost': 'High',
        'advantages': 'Decades of proven UV and weather protection without cracking, impervious to harsh cleaning solvents, flame and smoke retardant.',
        'limitations': 'Supplied primarily as oriented film rather than bulk molding resin, requires specialized lamination adhesives.',
        'applications': 'Photovoltaic solar module backsheets, aircraft cabin wall coverings, outdoor architectural graphics, acoustic wall protective facings.',
        'image_url': None
    },
    {
        'name': 'Epoxy-Standard',
        'category': 'Thermoset',
        'description': 'Bisphenol-A based Epoxy Resin cured with amine hardeners forms a crosslinked polymer network with high bond strength and low shrinkage.',
        'strength': 75.00,
        'max_temperature': 120,
        'density': 1.180,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'Exceptional adhesion to metals and fibers, negligible cure shrinkage (<1%), high mechanical stiffness, excellent electrical insulation.',
        'limitations': 'Brittle without toughening modifiers, slow cure cycles compared to thermoplastic molding, skin-sensitizing liquid precursors.',
        'applications': 'Carbon fiber composite structural parts, printed circuit board substrates (FR-4), structural engineering adhesives, marine repairs.',
        'image_url': None
    },
    {
        'name': 'Epoxy-High-Temperature',
        'category': 'Thermoset',
        'description': 'Multifunctional epoxy resin formulated with aromatic amine curing agents to achieve glass transition temperatures exceeding 180 deg C.',
        'strength': 90.00,
        'max_temperature': 180,
        'density': 1.250,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Retains structural modulus up to 180 deg C, excellent hot-wet compression strength, high chemical resistance to aviation fuels.',
        'limitations': 'Requires multi-stage autoclave curing cycles at elevated temperature and pressure, inherently brittle.',
        'applications': 'Aerospace composite primary structures (wing spars, control surfaces), motorsport drive shafts, tooling prepregs.',
        'image_url': None
    },
    {
        'name': 'Phenolic-Resin',
        'category': 'Thermoset',
        'description': 'Phenol-Formaldehyde Resin (Bakelite) is a historic thermoset renowned for supreme fire resistance, high surface hardness, and electrical insulation.',
        'strength': 55.00,
        'max_temperature': 150,
        'density': 1.400,
        'chemical_resistance': 'Good',
        'cost': 'Low',
        'advantages': 'Remarkable flame resistance with low smoke toxicity, high heat deflection, excellent electrical arc resistance, economical.',
        'limitations': 'Dark colors only (brown/black), releases condensation water during curing, brittle under mechanical shock.',
        'applications': 'Automotive brake pads and clutch facings, cookware pot handles, electrical switchboards, billiard balls, circuit breaker cases.',
        'image_url': None
    },
    {
        'name': 'Melamine-Formaldehyde',
        'category': 'Thermoset',
        'description': 'Melamine-Formaldehyde is a hard, scratch-resistant thermosetting resin with exceptional surface gloss, heat resistance, and fire retardancy.',
        'strength': 65.00,
        'max_temperature': 130,
        'density': 1.500,
        'chemical_resistance': 'Good',
        'cost': 'Low',
        'advantages': 'Glass-hard scratch-resistant surface, self-extinguishing flame properties, can be colored in vibrant white and pastel shades.',
        'limitations': 'Brittle, cannot be heated in microwave ovens, releases trace formaldehyde if subjected to high boiling acids.',
        'applications': 'Kitchen dinnerware, Formica decorative laminate countertops, electrical switch plates, acoustic insulation foam.',
        'image_url': None
    },
    {
        'name': 'Urea-Formaldehyde',
        'category': 'Thermoset',
        'description': 'Urea-Formaldehyde is a cost-effective amino resin widely utilized for high-hardness electrical components and wood composite binders.',
        'strength': 50.00,
        'max_temperature': 90,
        'density': 1.450,
        'chemical_resistance': 'Fair',
        'cost': 'Low',
        'advantages': 'High surface hardness, superior anti-tracking electrical resistance, self-extinguishing, highly economical.',
        'limitations': 'Poor water and weather resistance; susceptible to hydrolytic breakdown under warm, damp environments.',
        'applications': 'Wall electrical sockets and light switches, particleboard and MDF binder adhesive, toilet seat covers, buttons.',
        'image_url': None
    },
    {
        'name': 'Unsaturated-Polyester',
        'category': 'Thermoset',
        'description': 'Unsaturated Polyester Resin is the dominant binder matrix for glass-reinforced plastic (fiberglass) boat hulls, tanks, and architectural panels.',
        'strength': 55.00,
        'max_temperature': 110,
        'density': 1.200,
        'chemical_resistance': 'Good',
        'cost': 'Low',
        'advantages': 'Very low cost, easy ambient-temperature curing with MEKP initiator, rapid wetting of glass fibers, good water resistance.',
        'limitations': 'Significant cure volumetric shrinkage (6-8%), styrene vapor emissions during hand layup, lower fatigue strength than epoxy.',
        'applications': 'Fiberglass boat hulls, automotive body repair fillers, architectural cladding panels, corrugated roofing sheets, shower trays.',
        'image_url': None
    },
    {
        'name': 'Vinyl-Ester',
        'category': 'Thermoset',
        'description': 'Vinyl Ester Resin bridges the gap between polyester and epoxy, offering exceptional chemical corrosion resistance and dynamic fatigue life.',
        'strength': 70.00,
        'max_temperature': 135,
        'density': 1.150,
        'chemical_resistance': 'Excellent',
        'cost': 'Medium',
        'advantages': 'Superior chemical corrosion resistance to aggressive acids and alkalis, higher elongation than polyester, prevents fiberglass osmotic blistering.',
        'limitations': 'Higher cost than unsaturated polyester, contains styrene monomer requiring positive shop ventilation.',
        'applications': 'Chemical plant storage tanks, wastewater piping, flue gas desulfurization scrubbers, marine luxury yacht hulls, swimming pools.',
        'image_url': None
    },
    {
        'name': 'Cyanate-Ester',
        'category': 'High-Performance Thermoset',
        'description': 'Cyanate Ester resins offer exceptionally low dielectric loss (Dk/Df), minimal moisture uptake, and high radiation resistance for satellite applications.',
        'strength': 95.00,
        'max_temperature': 230,
        'density': 1.200,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Extremely low dielectric constant and dissipation factor across GHz microwave frequencies, outgassing compliant for space vacuum.',
        'limitations': 'Expensive raw materials, sensitive to moisture contamination prior to complete thermal curing.',
        'applications': 'Satellite radar antennas, stealth aircraft radomes, high-frequency printed microwave circuit substrates, space telescope mirror structures.',
        'image_url': None
    },
    {
        'name': 'Bismaleimide',
        'category': 'High-Performance Thermoset',
        'description': 'Bismaleimide (BMI) resins are thermosetting polymers designed for continuous aerodynamic surface service temperatures between 200 and 230 deg C.',
        'strength': 105.00,
        'max_temperature': 230,
        'density': 1.280,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Retains high mechanical stiffness and compression after impact at 200 deg C, excellent hot-wet performance, epoxy-like handling.',
        'limitations': 'High raw material cost, brittle without core-shell rubber or reactive thermoplastic toughening modifiers.',
        'applications': 'Supersonic fighter jet fuselage skins, jet engine nacelle cowlings, high-temperature missile fairings, F1 exhaust surrounds.',
        'image_url': None
    },
    {
        'name': 'Polyurethane-Rigid',
        'category': 'Thermoset Cellular',
        'description': 'Rigid Polyurethane Foam is the highest efficiency commercial thermal insulation material available, created by reacting polyols with isocyanates.',
        'strength': 15.00,
        'max_temperature': 110,
        'density': 0.045,
        'chemical_resistance': 'Good',
        'cost': 'Low',
        'advantages': 'Lowest thermal conductivity (highest R-value) of commercial insulation materials, closed-cell structure prevents moisture ingress.',
        'limitations': 'Flammable without halogen or phosphorus flame retardants, degrades rapidly under direct UV sun exposure.',
        'applications': 'Commercial refrigerator insulation, architectural insulated metal sandwich panels, pipe insulation, spray foam roofing.',
        'image_url': None
    },
    {
        'name': 'TPU',
        'category': 'Thermoplastic Elastomer',
        'description': 'Thermoplastic Polyurethane bridges the gap between rubber and plastics, offering extreme abrasion resistance, elasticity, and oil barrier.',
        'strength': 40.00,
        'max_temperature': 90,
        'density': 1.200,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'Outstanding abrasion and tear resistance, high elastic recovery, remains flexible at -40 deg C, good grease and fuel resistance.',
        'limitations': 'Prone to hydrolytic degradation in prolonged hot humid environments, narrow melt processing temperature window.',
        'applications': 'Athletic shoe soles, protective smartphone cases, hydraulic cylinder seals, pneumatic hoses, automotive suspension bushings, caster wheels.',
        'image_url': None
    },
    {
        'name': 'TPO',
        'category': 'Thermoplastic Elastomer',
        'description': 'Thermoplastic Polyolefin is a blend of polypropylene and uncrosslinked EPDM rubber providing lightweight durability and cold-impact toughness.',
        'strength': 22.00,
        'max_temperature': 95,
        'density': 0.950,
        'chemical_resistance': 'Good',
        'cost': 'Low',
        'advantages': 'Low density, excellent cold impact down to -40 deg C, direct paintability with primers, fully recyclable, cost effective.',
        'limitations': 'Moderate tensile strength, lower recovery from high sustained compression stress than vulcanized rubbers.',
        'applications': 'Automotive bumper fascias, single-ply commercial roofing membranes, interior automotive dash skins, weatherstrip seals.',
        'image_url': None
    },
    {
        'name': 'TPV',
        'category': 'Thermoplastic Elastomer',
        'description': 'Thermoplastic Vulcanizate (Santoprene) features dynamically vulcanized EPDM rubber nodules dispersed inside a continuous polypropylene matrix.',
        'strength': 15.00,
        'max_temperature': 125,
        'density': 0.960,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'Rubber-like sealing performance with true thermoplastic injection molding efficiency, excellent ozone and heat aging resistance.',
        'limitations': 'Higher compression set than pure vulcanized rubber at extreme temperatures; higher cost than standard TPO.',
        'applications': 'Automotive glass run channels, under-hood air intake ducts, washing machine pump seals, soft-touch power tool grips.',
        'image_url': None
    },
    {
        'name': 'Silicone-Rubber',
        'category': 'Thermoset Elastomer',
        'description': 'Polydimethylsiloxane (Silicone) has an inorganic silicon-oxygen backbone delivering flexibility from -60 deg C to +200 deg C with biological inertness.',
        'strength': 10.00,
        'max_temperature': 200,
        'density': 1.150,
        'chemical_resistance': 'Good',
        'cost': 'High',
        'advantages': 'Unmatched thermal stability window (-60 to +200 deg C), biocompatible and food safe, outstanding ozone and UV weather resistance, flexible.',
        'limitations': 'Low tensile and tear strength compared to organic rubbers, permeable to gases, poor resistance to concentrated hydrocarbon fuels.',
        'applications': 'Medical respiratory masks, baking molds, automotive spark plug boots, high-voltage insulator coatings, gasket seals.',
        'image_url': None
    },
    {
        'name': 'Fluorosilicone',
        'category': 'High-Performance Elastomer',
        'description': 'Fluorosilicone rubber (FVMQ) adds fluorinated side groups to silicone chains to deliver fuel and solvent resistance while keeping low-temp elasticity.',
        'strength': 9.00,
        'max_temperature': 180,
        'density': 1.450,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Resistant to aggressive aviation fuels and synthetic oils while retaining flexibility down to -60 deg C.',
        'limitations': 'Low abrasion and mechanical tear strength, high cost, specialized processing required.',
        'applications': 'Aircraft fuel tank access door seals, automotive turbocharger bypass diaphragms, defense aerospace O-rings.',
        'image_url': None
    },
    {
        'name': 'Fluoroelastomer',
        'category': 'High-Performance Elastomer',
        'description': 'Fluoroelastomer (FKM / Viton) is the gold standard for sealing applications involving aggressive chemicals, synthetic engine oils, and temperatures up to 200 deg C.',
        'strength': 15.00,
        'max_temperature': 200,
        'density': 1.850,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Exceptional resistance to gasoline, diesel, biodiesel, synthetic engine lubricants, and aggressive industrial solvents at high heat.',
        'limitations': 'Stiffens below -15 deg C without special low-temperature grades, high density, premium cost.',
        'applications': 'Automotive engine crankshaft oil seals, fuel injector O-rings, aircraft fuel system gaskets, chemical refinery pipe seals.',
        'image_url': None
    },
    {
        'name': 'Nitrile-Rubber',
        'category': 'Thermoset Elastomer',
        'description': 'Nitrile Butadiene Rubber (NBR / Buna-N) is a synthetic rubber engineered specifically for resistance to petroleum oils, greases, and hydraulic fluids.',
        'strength': 20.00,
        'max_temperature': 100,
        'density': 1.150,
        'chemical_resistance': 'Good',
        'cost': 'Low',
        'advantages': 'Outstanding resistance to petroleum-based oils and hydraulic fluids, good mechanical resilience, economical.',
        'limitations': 'Poor resistance to atmospheric ozone, sunlight, and weather; becomes brittle at temperatures below -20 deg C.',
        'applications': 'Disposable nitrile examination gloves, automotive fuel and oil hoses, hydraulic cylinder O-rings, oil well packers.',
        'image_url': None
    },
    {
        'name': 'HNBR',
        'category': 'Specialty Elastomer',
        'description': 'Hydrogenated Nitrile Butadiene Rubber saturates the polymer backbone to boost heat resistance to 150 deg C and provide high ozone endurance.',
        'strength': 28.00,
        'max_temperature': 150,
        'density': 1.180,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Significantly higher heat and ozone resistance than standard NBR, superior tensile strength and cut-growth resistance.',
        'limitations': 'Higher price than standard nitrile rubber due to catalytic hydrogenation synthesis.',
        'applications': 'Automotive engine timing belts, air conditioning compressor seals (R134a/R1234yf), oilfield blowout preventer packing.',
        'image_url': None
    },
    {
        'name': 'EPDM',
        'category': 'Thermoset Elastomer',
        'description': 'Ethylene Propylene Diene Monomer is an all-weather elastomer offering unmatched resistance to outdoor ozone, UV radiation, brake fluids, and steam.',
        'strength': 16.00,
        'max_temperature': 140,
        'density': 1.100,
        'chemical_resistance': 'Good',
        'cost': 'Low',
        'advantages': 'Immune to atmospheric ozone cracking, superior outdoor weathering, excellent compatibility with glycol brake fluid and steam.',
        'limitations': 'Severely degraded by petroleum oils, gasoline, kerosene, and mineral hydrocarbon greases.',
        'applications': 'Automotive weatherstrips, radiator cooling hoses, hydraulic brake system cups, commercial roofing membranes, washing machine gaskets.',
        'image_url': None
    },
    {
        'name': 'Neoprene',
        'category': 'Thermoset Elastomer',
        'description': 'Polychloroprene (Neoprene) offers a balanced combination of oil resistance, weatherproofing, flame retardancy, and mechanical tear strength.',
        'strength': 18.00,
        'max_temperature': 100,
        'density': 1.250,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'Good moderate resistance to petroleum oils and outdoor ozone, flame retardant self-extinguishing behavior, high resilience.',
        'limitations': 'Not suitable for prolonged contact with concentrated aromatic fuels; moderate compression set over time.',
        'applications': 'Wetsuits, bridge bearing expansion pads, industrial conveyor belts, HVAC duct vibration dampeners, drive belts.',
        'image_url': None
    },
    {
        'name': 'Natural-Rubber',
        'category': 'Elastomer',
        'description': 'Natural Polyisoprene possesses the highest mechanical resilience, tear propagation resistance, and fatigue life of any known elastomer.',
        'strength': 25.00,
        'max_temperature': 80,
        'density': 0.930,
        'chemical_resistance': 'Fair',
        'cost': 'Medium',
        'advantages': 'Unrivaled mechanical rebound resilience, exceptional tensile and tear strength, low heat buildup under cyclic flexing.',
        'limitations': 'Vulnerable to atmospheric ozone cracking, degraded rapidly by petroleum oils and organic solvents, max temp 80 deg C.',
        'applications': 'Heavy-duty truck and aircraft tires, seismic building isolators, automotive engine vibration mounts, rubber bands.',
        'image_url': None
    },
    {
        'name': 'SBR',
        'category': 'Thermoset Elastomer',
        'description': "Styrene-Butadiene Rubber is the world's most widely consumed synthetic rubber, engineered as a durable, wear-resistant tire tread polymer.",
        'strength': 20.00,
        'max_temperature': 85,
        'density': 0.940,
        'chemical_resistance': 'Fair',
        'cost': 'Low',
        'advantages': 'High abrasion and tread wear resistance, good grip on wet asphalt surfaces, lower cost than natural rubber.',
        'limitations': 'Lower tear resistance and elasticity than natural rubber, poor resistance to ozone, fuels, and sunlight.',
        'applications': 'Passenger car tire treads, conveyor belt covers, shoe soles, molded industrial drive pulleys.',
        'image_url': None
    },
    {
        'name': 'Butyl-Rubber',
        'category': 'Thermoset Elastomer',
        'description': 'Isobutylene-isoprene copolymer (Butyl) provides the lowest gas permeability of all commercial rubbers, making it standard for airtight tire inner liners.',
        'strength': 16.00,
        'max_temperature': 110,
        'density': 0.920,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'Extremely low gas and air permeability (70% lower than natural rubber), high vibration dampening factor, excellent chemical barrier.',
        'limitations': 'Slow vulcanization cure speed, poor resilience and bounce back, incompatible with petroleum lubricants.',
        'applications': 'Tubeless tire airtight inner liners, pharmaceutical vial stoppers, chemical protective hazard gloves, vacuum seals.',
        'image_url': None
    },
    {
        'name': 'Polybutadiene-Rubber',
        'category': 'Thermoset Elastomer',
        'description': 'Polybutadiene Rubber (BR) provides outstanding wear resistance and dynamic rebound resilience down to temperatures as low as -70 deg C.',
        'strength': 18.00,
        'max_temperature': 85,
        'density': 0.910,
        'chemical_resistance': 'Fair',
        'cost': 'Low',
        'advantages': 'Exceptional abrasion resistance, very high elasticity rebound, lowest glass transition temperature (-100 deg C) of common rubbers.',
        'limitations': 'Low cut and tear resistance, slippery on wet ice surfaces when unblended, vulnerable to ozone and oil.',
        'applications': 'Tire tread blends, golf ball resilient cores, impact-modifying graft phase for HIPS and ABS, conveyor rollers.',
        'image_url': None
    },
    {
        'name': 'PLA',
        'category': 'Biopolymer',
        'description': 'Polylactic Acid is a bio-based compostable thermoplastic derived from fermented plant corn starch, celebrated for ease of 3D printing.',
        'strength': 60.00,
        'max_temperature': 55,
        'density': 1.240,
        'chemical_resistance': 'Fair',
        'cost': 'Low',
        'advantages': '100% renewable plant feedstock, biodegradable in industrial composting, high tensile stiffness, odorless ease of 3D printing.',
        'limitations': 'Low heat deflection temperature (softens at 55 deg C), brittle under impact shock, slow ambient environmental degradation.',
        'applications': 'FDM 3D printing filaments, disposable food takeaway cups, clear blister packaging, bioresorbable medical suture anchors.',
        'image_url': None
    },
    {
        'name': 'PHA',
        'category': 'Biopolymer',
        'description': 'Polyhydroxyalkanoates are natural polyesters synthesized intracellularly by bacterial fermentation of sugars or plant oils, fully marine biodegradable.',
        'strength': 35.00,
        'max_temperature': 75,
        'density': 1.250,
        'chemical_resistance': 'Good',
        'cost': 'High',
        'advantages': 'Truly ocean and soil biodegradable leaving zero microplastics, renewable bacterial production, biocompatible.',
        'limitations': 'Narrow thermal processing window, slow crystallization rate causing mold sticking, high production cost.',
        'applications': 'Ocean-safe marine packaging, agricultural mulch film, disposable coffee cup linings, internal medical implants.',
        'image_url': None
    },
    {
        'name': 'PHB',
        'category': 'Biopolymer',
        'description': 'Polyhydroxybutyrate is the most common PHA homopolymer, offering physical mechanical properties closely mimicking polypropylene.',
        'strength': 40.00,
        'max_temperature': 85,
        'density': 1.250,
        'chemical_resistance': 'Good',
        'cost': 'High',
        'advantages': 'High optical purity, moisture barrier similar to PP, compostable in backyard soil and marine environments.',
        'limitations': 'Brittle due to large secondary spherulite crystallization over time, thermally unstable above its melt point.',
        'applications': 'Biodegradable packaging containers, controlled-release drug delivery capsules, orthopedic surgical pins.',
        'image_url': None
    },
    {
        'name': 'PBS',
        'category': 'Biopolymer',
        'description': 'Polybutylene Succinate is an aliphatic biodegradable polyester with ductile flexibility, elongation, and thermal tolerance up to 90 deg C.',
        'strength': 38.00,
        'max_temperature': 90,
        'density': 1.260,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'Higher heat resistance than PLA (up to 90 deg C), ductile elongation, blendable with other biopolymers to improve toughness.',
        'limitations': 'Moderate barrier properties to oxygen, higher price than conventional commodity polyolefins.',
        'applications': 'Compostable agricultural mulch films, food packaging cutlery, coffee capsules, paper hot-cup coatings.',
        'image_url': None
    },
    {
        'name': 'PBAT',
        'category': 'Biopolymer',
        'description': 'Polybutyrate Adipate Terephthalate is a highly flexible, ductile biodegradable co-polyester widely blended with PLA to replace LDPE film.',
        'strength': 22.00,
        'max_temperature': 65,
        'density': 1.220,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'High elongation at break (>500%), soft rubbery touch, fully biodegradable in soil, excellent carrier for starch and PLA.',
        'limitations': 'Low tensile modulus and strength, lower barrier properties to moisture vapor than polyethylene.',
        'applications': 'Compostable organic waste bags, agricultural soil mulch films, flexible mailer pouches, shrink wraps.',
        'image_url': None
    },
    {
        'name': 'PCL',
        'category': 'Biopolymer',
        'description': 'Polycaprolactone is a biodegradable polyester with an ultra-low melting point (60 deg C), allowing hand molding in warm water.',
        'strength': 25.00,
        'max_temperature': 50,
        'density': 1.140,
        'chemical_resistance': 'Fair',
        'cost': 'Medium',
        'advantages': 'Low melting point (60 deg C) enables hand-shapeable prototype modeling, slow controlled biodegrade rate (1-2 years) in vivo.',
        'limitations': 'Cannot be used in structural applications exposed to warm water or sunlight due to low melting temperature.',
        'applications': 'Long-term drug release implants, tissue engineering bone scaffolds, orthopedic splints, hobby molding pellets (InstaMorph).',
        'image_url': None
    },
    {
        'name': 'PGA',
        'category': 'Biopolymer',
        'description': 'Polyglycolic Acid is a high-strength, fast-degrading bioresorbable polymer offering superior gas barrier and fast downhole degradation.',
        'strength': 90.00,
        'max_temperature': 120,
        'density': 1.530,
        'chemical_resistance': 'Good',
        'cost': 'High',
        'advantages': 'Highest tensile strength among biopolymers (90 MPa), predictable hydrolytic bioresorption in human tissue, gas barrier.',
        'limitations': 'Hydrolyzes rapidly in moisture environments unless hermetically sealed, high synthesis cost.',
        'applications': 'Dissolvable surgical sutures (Dexon), degradable downhole oilfield frac plugs, ultra-barrier bottle layers.',
        'image_url': None
    },
    {
        'name': 'Cellulose-Acetate',
        'category': 'Bio-Based Polymer',
        'description': 'Cellulose Acetate is a semi-synthetic polymer derived from refined wood pulp, celebrated for deep luster, warmth to touch, and optical clarity.',
        'strength': 50.00,
        'max_temperature': 75,
        'density': 1.300,
        'chemical_resistance': 'Fair',
        'cost': 'Medium',
        'advantages': 'Deep rich aesthetic luster and hypoallergenic touch, biodegradable under compost conditions, high clarity.',
        'limitations': 'Hygroscopic moisture sensitivity, moderate chemical resistance to organic solvents and acetone.',
        'applications': 'Designer eyewear frames, cigarette filtration tow, tool handle grips, transparent display film, buttons.',
        'image_url': None
    },
    {
        'name': 'Bio-PE',
        'category': 'Bio-Based Polymer',
        'description': 'Bio-Polyethylene is chemically identical to conventional petrochemical HDPE/LDPE but synthesized from sugarcane bio-ethanol with negative carbon footprint.',
        'strength': 28.00,
        'max_temperature': 120,
        'density': 0.955,
        'chemical_resistance': 'Excellent',
        'cost': 'Medium',
        'advantages': 'Direct 100% drop-in replacement for conventional PE, recyclable in existing recycling streams, captures 3 kg CO2 per kg produced.',
        'limitations': 'Not biodegradable (remains in environment just like conventional plastic), slightly higher cost than petro-PE.',
        'applications': 'Sustainable cosmetics packaging bottles, detergent containers, caps and closures, agricultural films, toys.',
        'image_url': None
    },
    {
        'name': 'Bio-PET',
        'category': 'Bio-Based Polymer',
        'description': 'Bio-Polyethylene Terephthalate contains 30% plant-derived bio-monoethylene glycol (Bio-MEG) from biomass, matching all PET properties.',
        'strength': 75.00,
        'max_temperature': 70,
        'density': 1.380,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'Identical barrier and mechanical properties to petroleum PET, 100% recyclable in existing curbside bottle recycling bins.',
        'limitations': 'Only partially bio-based (purified terephthalic acid PTA is still currently petroleum derived).',
        'applications': 'Eco-branded beverage bottles (PlantBottle), consumer food packaging, automotive seat textile upholstery.',
        'image_url': None
    },
    {
        'name': 'Thermoplastic-Starch',
        'category': 'Biopolymer',
        'description': 'Thermoplastic Starch (TPS) is produced by plasticizing native agricultural starch with glycerol, yielding home-compostable film blends.',
        'strength': 12.00,
        'max_temperature': 50,
        'density': 1.350,
        'chemical_resistance': 'Poor',
        'cost': 'Low',
        'advantages': 'Low material cost, 100% renewable farm crops, fast home composting without industrial facilities.',
        'limitations': 'Highly sensitive to water and humidity; low tensile strength when unblended with synthetic polyesters.',
        'applications': 'Biodegradable grocery shopping bags, loose-fill packaging packing peanuts, temporary agricultural seedling pots.',
        'image_url': None
    },
    {
        'name': 'PC-ABS',
        'category': 'Polymer Blend',
        'description': 'Polycarbonate/ABS blend combines the high heat and impact resistance of PC with the easy melt flow and cosmetic surface finish of ABS.',
        'strength': 58.00,
        'max_temperature': 105,
        'density': 1.130,
        'chemical_resistance': 'Fair',
        'cost': 'Medium',
        'advantages': 'Superb low-temperature ductility, high heat distortion temperature (105 deg C), easy injection molding, low residual mold stress.',
        'limitations': 'Moderate chemical resistance to petroleum and solvents; hygroscopic requiring pre-drying.',
        'applications': 'Automotive dashboard instrument panels, laptop computer housings, mobile phone internal frames, medical monitors.',
        'image_url': None
    },
    {
        'name': 'PC-PBT',
        'category': 'Polymer Blend',
        'description': "Polycarbonate/PBT blend pairs PC's impact toughness with PBT's superior resistance to motor fuels, motor oils, and lubricants.",
        'strength': 60.00,
        'max_temperature': 115,
        'density': 1.250,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'Exceptional impact resistance combined with hydrocarbon chemical resistance, excellent dimensional stability.',
        'limitations': 'Moderate surface hardness, requires careful processing temperature control to avoid phase separation.',
        'applications': 'Automotive exterior bumper beams, door handles, heavy-duty outdoor power equipment enclosures, industrial plugs.',
        'image_url': None
    },
    {
        'name': 'PPO-PS-Noryl',
        'category': 'Polymer Blend',
        'description': 'Polyphenylene Oxide blended with Polystyrene (Noryl) delivers outstanding hydrolytic stability, low water uptake, and flame retardancy.',
        'strength': 60.00,
        'max_temperature': 110,
        'density': 1.080,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'Almost zero moisture absorption, superb dimensional stability in boiling water, UL94 V-0 flame ratings without halogens.',
        'limitations': 'Vulnerable to petroleum hydrocarbons, aromatic solvents, and cyclic esters under stress.',
        'applications': 'Water filtration pump impellers, solar panel junction boxes, electric vehicle battery pack modules, telecommunication enclosures.',
        'image_url': None
    },
    {
        'name': 'PA6-GF30',
        'category': 'Reinforced Composite',
        'description': 'Polyamide 6 reinforced with 30% short glass fibers dramatically increases tensile strength, stiffness, and heat deflection under load.',
        'strength': 160.00,
        'max_temperature': 150,
        'density': 1.360,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'Very high tensile strength (160 MPa), 3x higher modulus than unfilled PA6, high creep resistance and heat deflection.',
        'limitations': 'Abrasive to injection molding screw and barrel, directional mold shrinkage (warpage risk), reduced surface gloss.',
        'applications': 'Automotive engine intake manifolds, cooling fan blades, power drill motor casings, structural office chair bases.',
        'image_url': None
    },
    {
        'name': 'PA66-GF30',
        'category': 'Reinforced Composite',
        'description': 'Polyamide 66 with 30% glass fiber reinforcement offers the ultimate balance of high strength, rigidity, and continuous high-temperature under-hood service.',
        'strength': 175.00,
        'max_temperature': 160,
        'density': 1.370,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'Outstanding mechanical rigidity and strength up to 160 deg C, excellent fatigue endurance under cyclic automotive vibration.',
        'limitations': 'Anisotropic fiber orientation causes differential shrinkage, brittle under high shock impact without rubber impact modifiers.',
        'applications': 'Automotive radiator end tanks, thermostat valve housings, structural rocker arm covers, industrial pump impellers.',
        'image_url': None
    },
    {
        'name': 'PBT-GF30',
        'category': 'Reinforced Composite',
        'description': 'Polybutylene Terephthalate reinforced with 30% glass fibers provides extreme dimensional precision and electrical insulation in moist environments.',
        'strength': 130.00,
        'max_temperature': 140,
        'density': 1.530,
        'chemical_resistance': 'Excellent',
        'cost': 'Medium',
        'advantages': 'High rigidity and strength, low moisture absorption ensuring constant dielectric insulation, minimal creep under sustained clamping load.',
        'limitations': 'Anisotropic warpage in flat parts, susceptible to steam hydrolysis above 65 deg C.',
        'applications': 'Automotive multi-pin ECU connectors, windshield wiper motor arm frames, circuit breaker bases, ignition coil housings.',
        'image_url': None
    },
    {
        'name': 'PC-GF20',
        'category': 'Reinforced Composite',
        'description': 'Polycarbonate reinforced with 20% glass fibers significantly enhances stiffness, reduces thermal expansion, and improves dimensional tolerances.',
        'strength': 95.00,
        'max_temperature': 135,
        'density': 1.350,
        'chemical_resistance': 'Fair',
        'cost': 'Medium',
        'advantages': 'High stiffness, reduced coefficient of thermal expansion matching aluminum, excellent creep resistance under load.',
        'limitations': 'Loss of optical transparency (becomes opaque gray/white), reduced impact toughness compared to unfilled polycarbonate.',
        'applications': 'Precision drone frames, camera bodies, optical instrument chassis, high-voltage transformer covers.',
        'image_url': None
    },
    {
        'name': 'PEEK-CF30',
        'category': 'Reinforced Composite',
        'description': 'Polyether Ether Ketone reinforced with 30% pitch/PAN carbon fibers yields metal-replacement strength with half the weight of aluminum.',
        'strength': 220.00,
        'max_temperature': 260,
        'density': 1.440,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Ultra-high tensile strength (220 MPa), high flexural modulus, low thermal expansion, static dissipative, self-lubricating wear.',
        'limitations': 'Very high cost, highly abrasive during machining, black opaque finish only.',
        'applications': 'Aerospace structural brackets, racing engine pushrods, semiconductor wafer handling wands, surgical orthopedic external fixation pins.',
        'image_url': None
    },
    {
        'name': 'PEEK-GF30',
        'category': 'Reinforced Composite',
        'description': 'Polyether Ether Ketone reinforced with 30% electrical-grade glass fibers enhances electrical insulation and mechanical modulus at 250 deg C.',
        'strength': 170.00,
        'max_temperature': 250,
        'density': 1.510,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Superb electrical isolation at extreme temperatures, superior compressive creep resistance, broad chemical inertness.',
        'limitations': 'High raw material price, requires specialized barrel heaters for 380 deg C melt processing.',
        'applications': 'Downhole oil well electrical connectors, nuclear reactor instrumentation sensors, high-temperature chemical pump impellers.',
        'image_url': None
    },
    {
        'name': 'PPS-GF40',
        'category': 'Reinforced Composite',
        'description': 'Polyphenylene Sulfide reinforced with 40% glass fibers achieves metal-like stiffness and zero solvent degradation up to 220 deg C.',
        'strength': 160.00,
        'max_temperature': 220,
        'density': 1.650,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'High rigidity and creep resistance, unaffected by all automotive fluids, flame retardant (UL94 V-0), high dimensional accuracy.',
        'limitations': 'Heavy density (1.65 g/cm3), brittle on sudden impact, causes severe wear on standard steel molds.',
        'applications': 'Automotive engine coolant thermostat valves, brake fluid reservoirs, industrial chemical pump volutes, halogen bulb sockets.',
        'image_url': None
    },
    {
        'name': 'POM-GF25',
        'category': 'Reinforced Composite',
        'description': 'Polyoxymethylene reinforced with 25% glass fiber beads/fibers enhances tensile modulus and continuous load capacity while keeping low friction.',
        'strength': 110.00,
        'max_temperature': 110,
        'density': 1.580,
        'chemical_resistance': 'Excellent',
        'cost': 'Medium',
        'advantages': 'Significantly higher modulus and load-bearing strength than unfilled POM, low moisture uptake, good fatigue life.',
        'limitations': 'Abrasive to soft mating plastics; higher friction coefficient than virgin POM against polished metals.',
        'applications': 'Heavy industrial conveyor chain links, high-torque gear wheels, fluid flow meter pistons, automotive seat track mechanisms.',
        'image_url': None
    },
    {
        'name': 'COC',
        'category': 'Specialty Polymer',
        'description': 'Cyclic Olefin Copolymer is an amorphous glass-clear polyolefin providing superior moisture barrier, optical transmission, and chemical purity.',
        'strength': 60.00,
        'max_temperature': 130,
        'density': 1.020,
        'chemical_resistance': 'Excellent',
        'cost': 'High',
        'advantages': 'Glass-like transparency with low birefringence, highest moisture barrier of any clear resin, low protein adsorption in pharmaceutical vials.',
        'limitations': 'Poor resistance to non-polar solvents and oils, relatively brittle, high material cost.',
        'applications': 'Prefilled insulin syringes, microfluidic diagnostic chips, optical camera lenses, high-barrier pharmaceutical blister packaging.',
        'image_url': None
    },
    {
        'name': 'EVOH',
        'category': 'Specialty Barrier Polymer',
        'description': "Ethylene Vinyl Alcohol is the world's preeminent gas-barrier polymer, preventing oxygen permeation in multi-layer food packaging and fuel tanks.",
        'strength': 70.00,
        'max_temperature': 100,
        'density': 1.170,
        'chemical_resistance': 'Good',
        'cost': 'High',
        'advantages': 'Unmatched oxygen and carbon dioxide barrier in dry state (10,000x better than LDPE), high oil and flavor barrier.',
        'limitations': 'Hydrophilic; loses oxygen barrier properties if exposed to high relative humidity unless sandwiched between PE or PP outer layers.',
        'applications': 'Multi-layer barrier food packaging bottles, automotive plastic fuel tanks, underfloor heating oxygen-barrier pipes.',
        'image_url': None
    },
    {
        'name': 'PVOH',
        'category': 'Specialty Polymer',
        'description': 'Polyvinyl Alcohol is a water-soluble synthetic polymer with remarkable tensile strength, oxygen barrier, and biodegradable dissolution.',
        'strength': 55.00,
        'max_temperature': 80,
        'density': 1.250,
        'chemical_resistance': 'Good',
        'cost': 'Medium',
        'advantages': 'Dissolves completely in water without toxic residue, exceptional oxygen barrier in low humidity, oil and grease barrier.',
        'limitations': 'Completely dissolved or swollen by water; cannot be used in humid outdoor or wet environments.',
        'applications': 'Laundry detergent pods (Tide Pods), water-soluble 3D printing dual-extrusion support filament, agricultural chemical single-dose packets.',
        'image_url': None
    },
    {
        'name': 'EVA',
        'category': 'Specialty Copolymer',
        'description': 'Ethylene Vinyl Acetate is an elastomeric copolymer providing rubber-like softness, high transparency, and low-temperature crack resistance.',
        'strength': 18.00,
        'max_temperature': 65,
        'density': 0.940,
        'chemical_resistance': 'Good',
        'cost': 'Low',
        'advantages': 'Rubber-like flexibility, high impact toughness at -50 deg C, high clarity, superior adhesive bonding as hot-melt glue.',
        'limitations': 'Low continuous service temperature, low tensile strength, vulnerable to oil absorption.',
        'applications': 'Solar photovoltaic panel encapsulant film, running shoe midsoles (cushioning foam), hot-melt adhesive sticks, flexible tubing.',
        'image_url': None
    },
    {
        'name': 'PVB',
        'category': 'Specialty Polymer',
        'description': 'Polyvinyl Butyral is a tough, adhesive resin used as the energy-absorbing interlayer film in laminated automotive and architectural safety glass.',
        'strength': 30.00,
        'max_temperature': 70,
        'density': 1.080,
        'chemical_resistance': 'Fair',
        'cost': 'Medium',
        'advantages': 'Incredible adhesion to glass surfaces, outstanding optical clarity, absorbs blunt impact energy preventing glass shattering.',
        'limitations': 'Hygroscopic moisture sensitivity, sensitive to plasticizer balance, low surface hardness.',
        'applications': 'Automotive windshield safety glass interlayers, hurricane-resistant architectural windows, sound-dampening acoustic glazing.',
        'image_url': None
    },
    {
        'name': 'Polyketone-Aliphatic',
        'category': 'Engineering Thermoplastic',
        'description': 'Aliphatic Polyketone (POK / Carilon) is an engineered terpolymer providing balanced wear resistance, fuel barrier, and resilience.',
        'strength': 60.00,
        'max_temperature': 110,
        'density': 1.240,
        'chemical_resistance': 'Excellent',
        'cost': 'Medium',
        'advantages': 'Exceptional resistance to chemical fuels and aggressive coolants, superior wear resistance against POM and nylon, low noise gears.',
        'limitations': 'Requires UV stabilization for outdoor applications; thermal stability requires precise molding temperature window.',
        'applications': 'Automotive fuel pump housings, low-noise gear trains, conveyor components, oil and gas transport piping.',
        'image_url': None
    },
    {
        'name': 'PCT',
        'category': 'Engineering Thermoplastic',
        'description': 'Polycyclohexylene Dimethylene Terephthalate is a high-melting polyester tailored for high-temperature surface-mount LED packaging.',
        'strength': 70.00,
        'max_temperature': 150,
        'density': 1.230,
        'chemical_resistance': 'Good',
        'cost': 'High',
        'advantages': 'Melting point of 290 deg C, high optical reflectivity in LED reflector cups, withstands lead-free solder reflow temperatures.',
        'limitations': 'Higher cost than PBT, requires high mold temperatures for crystallization.',
        'applications': 'LED reflector cups for automotive headlamps, TV backlighting frames, high-temperature electrical sockets.',
        'image_url': None
    }
]
# ============================================================
# Fallback In-Memory Polymer Data Handler
# ============================================================

class FallbackPolymer:
    """Lightweight Polymer-compatible object used when SQL database is initializing or offline."""

    def __init__(self, id, data):
        self.id = id
        self.name = data.get('name', '')
        self.category = data.get('category', '')
        self.description = data.get('description', '')
        self.strength = data.get('strength', 0.0)
        self.max_temperature = data.get('max_temperature', 0)
        self.density = data.get('density', 1.0)
        self.chemical_resistance = data.get('chemical_resistance', 'Moderate')
        self.cost = data.get('cost', 'Medium')
        self.advantages = data.get('advantages', '')
        self.limitations = data.get('limitations', '')
        self.applications = data.get('applications', '')
        self.image_url = data.get('image_url')
        self.created_at = None

    def to_dict(self):
        """Convert the fallback model instance to a dictionary matching Polymer.to_dict()."""
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
            'created_at': None
        }


def _get_fallback_polymers():
    """Generate in-memory polymer objects from DEFAULT_POLYMERS."""
    return [FallbackPolymer(idx + 1, data) for idx, data in enumerate(DEFAULT_POLYMERS)]


# ============================================================
# Helper functions
# ============================================================

def get_all_polymers():
    """Retrieve all polymer materials from the database, falling back safely to default polymers if DB is offline."""
    try:
        polymers = Polymer.query.order_by(Polymer.id).all()
        if polymers:
            return polymers
    except Exception:
        db.session.rollback()

    return _get_fallback_polymers()


def get_polymer_by_id(polymer_id):
    """Retrieve a single polymer by its ID using modern SQLAlchemy session get with offline fallback."""
    try:
        poly = db.session.get(Polymer, polymer_id)
        if poly is not None:
            return poly
    except Exception:
        db.session.rollback()

    for p in _get_fallback_polymers():
        if p.id == polymer_id:
            return p
    return None


def get_polymer_by_name(name):
    """Retrieve a single polymer by its name (case-insensitive) with offline fallback."""
    if not name:
        return None

    try:
        poly = Polymer.query.filter(Polymer.name.ilike(name)).first()
        if poly is not None:
            return poly
    except Exception:
        db.session.rollback()

    name_clean = name.strip().lower()
    for p in _get_fallback_polymers():
        if p.name.strip().lower() == name_clean:
            return p
    return None


def seed_database(force=False):
    """Seed the database with default polymer data safely, inserting any missing materials."""
    inserted = 0
    existing_names = {row[0].strip().lower() for row in db.session.query(Polymer.name).all()}

    for p_data in DEFAULT_POLYMERS:
        if p_data['name'].strip().lower() not in existing_names:
            p = Polymer(**p_data)
            db.session.add(p)
            existing_names.add(p_data['name'].strip().lower())
            inserted += 1

    if inserted > 0:
        db.session.commit()

    return inserted, Polymer.query.count()
