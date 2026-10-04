-- ============================================================
-- Polymer Material Selection and Recommendation System
-- Database Schema + Sample Data
-- ============================================================

-- Use the project database
USE polymer_recommendation_db;

-- ============================================================
-- Table 1: polymers
-- ============================================================
DROP TABLE IF EXISTS polymers;

CREATE TABLE polymers (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    name                VARCHAR(100) NOT NULL UNIQUE,
    category            VARCHAR(50)  NOT NULL,
    description         TEXT,
    strength            DECIMAL(10,2) NOT NULL COMMENT 'Tensile strength in MPa',
    max_temperature     INT NOT NULL COMMENT 'Maximum continuous use temperature in °C',
    density             DECIMAL(6,3) NOT NULL COMMENT 'Density in g/cm³',
    chemical_resistance VARCHAR(50)  NOT NULL,
    cost                VARCHAR(20)  NOT NULL COMMENT 'Low / Medium / High',
    advantages          TEXT,
    limitations         TEXT,
    applications        TEXT,
    image_url           VARCHAR(255) DEFAULT NULL,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_name (name),
    INDEX idx_category (category),
    INDEX idx_strength (strength),
    INDEX idx_max_temperature (max_temperature)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- Table 2: recommendation_history
-- ============================================================
DROP TABLE IF EXISTS recommendation_history;

CREATE TABLE recommendation_history (
    id                      INT AUTO_INCREMENT PRIMARY KEY,
    application             VARCHAR(150) NOT NULL,
    required_strength       VARCHAR(50)  NOT NULL,
    operating_temperature   INT          NOT NULL,
    weight_requirement      VARCHAR(50)  NOT NULL,
    chemical_resistance     VARCHAR(50)  NOT NULL,
    cost_preference         VARCHAR(50)  NOT NULL,
    recommendation_result   TEXT         NOT NULL,
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- Insert the 7 Polymer Materials
-- ============================================================

INSERT INTO polymers 
(name, category, description, strength, max_temperature, density, chemical_resistance, cost, advantages, limitations, applications, image_url)
VALUES

-- 1. HDPE
('HDPE', 'Thermoplastic',
 'High-Density Polyethylene is a strong, durable thermoplastic with excellent chemical resistance and good impact strength. It is widely used in packaging, pipes and containers.',
 25.00, 120, 0.950, 'Excellent', 'Low',
 'Excellent chemical resistance, good impact strength, low cost, moisture resistant, recyclable',
 'Lower stiffness compared to some engineering plastics, limited high-temperature performance, can stress-crack under certain conditions',
 'Bottles, pipes, tanks, cutting boards, geomembranes, toys',
 NULL),

-- 2. PP
('PP', 'Thermoplastic',
 'Polypropylene is a versatile thermoplastic known for its excellent chemical resistance, low density and good fatigue resistance. It is one of the most widely used plastics.',
 30.00, 100, 0.905, 'Excellent', 'Low',
 'Low density, excellent chemical resistance, good fatigue resistance, low cost, living hinge capability',
 'Poor resistance to UV (without additives), becomes brittle at low temperatures, moderate impact strength',
 'Automotive parts, packaging, living hinges, medical devices, textiles, containers',
 NULL),

-- 3. PVC
('PVC', 'Thermoplastic',
 'Polyvinyl Chloride is a widely used thermoplastic available in rigid and flexible forms. It offers good chemical resistance and is commonly used in construction and piping.',
 50.00, 60, 1.400, 'Good', 'Low',
 'Good chemical resistance, high strength, flame retardant (with additives), low cost, versatile (rigid & flexible)',
 'Limited high-temperature resistance, contains chlorine (environmental concerns), can release HCl when burned',
 'Pipes, window frames, flooring, cables, medical tubing, credit cards',
 NULL),

-- 4. PS
('PS', 'Thermoplastic',
 'Polystyrene is a rigid, transparent thermoplastic that is easy to process. It is commonly used in disposable products and packaging.',
 40.00, 70, 1.050, 'Fair', 'Low',
 'Low cost, easy to process, good dimensional stability, transparent grades available, rigid',
 'Brittle, poor chemical resistance to many solvents, limited temperature resistance, environmental concerns (single-use)',
 'Disposable cutlery, CD cases, packaging foam, laboratory ware, insulation',
 NULL),

-- 5. PET
('PET', 'Thermoplastic',
 'Polyethylene Terephthalate is a strong, transparent thermoplastic with excellent barrier properties. It is the most common material for beverage bottles.',
 70.00, 70, 1.380, 'Good', 'Medium',
 'Excellent strength and stiffness, good barrier properties, transparent, recyclable, good chemical resistance',
 'Limited high-temperature performance, can crystallize and become opaque, moisture sensitive during processing',
 'Beverage bottles, food packaging, textile fibers (polyester), films, engineering components',
 NULL),

-- 6. Nylon 6
('Nylon 6', 'Engineering Thermoplastic',
 'Nylon 6 (Polyamide 6) is a strong engineering thermoplastic with excellent wear resistance, toughness and good chemical resistance to many substances.',
 80.00, 150, 1.140, 'Good', 'High',
 'High strength and toughness, excellent wear resistance, good chemical resistance, good fatigue resistance',
 'Absorbs moisture (affects dimensions and properties), higher cost, requires drying before processing',
 'Gears, bearings, automotive parts, textiles, power tool housings, fasteners',
 NULL),

-- 7. ABS
('ABS', 'Engineering Thermoplastic',
 'Acrylonitrile Butadiene Styrene is a tough, impact-resistant engineering thermoplastic with good dimensional stability and surface finish.',
 40.00, 90, 1.050, 'Fair', 'Medium',
 'Excellent impact resistance, good toughness, easy to process, good surface finish, dimensional stability',
 'Poor resistance to solvents and UV (without additives), moderate chemical resistance, not suitable for high temperatures',
 'Automotive interior parts, electronic housings, LEGO bricks, luggage, protective equipment',
 NULL),

 -- 17. LDPE
('LDPE', 'Thermoplastic',
 'Low-Density Polyethylene is a flexible thermoplastic with excellent moisture resistance, chemical resistance and good impact strength.',
 28.00, 80, 0.920, 'Excellent', 'Low',
 'Flexible, excellent moisture resistance, good chemical resistance, low cost, good impact strength',
 'Low stiffness, limited temperature resistance, relatively low tensile strength',
 'Plastic bags, films, squeeze bottles, liners, tubing, flexible packaging',
 NULL);


-- ============================================================
-- Verification Queries (optional – you can run these later)
-- ============================================================
-- SELECT * FROM polymers;
-- SELECT COUNT(*) AS total_polymers FROM polymers;
-- DESCRIBE polymers;
-- DESCRIBE recommendation_history;