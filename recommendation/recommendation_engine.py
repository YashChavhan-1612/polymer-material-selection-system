from database import get_all_polymers


def _map_strength_level(strength_value):
    """Convert numeric tensile strength (MPa) into Low / Medium / High."""
    if strength_value is None:
        return "Medium"
    value = float(strength_value)
    if value < 35:
        return "Low"
    elif value <= 60:
        return "Medium"
    else:
        return "High"


def _map_chemical_level(chem_text):
    """Convert database chemical resistance text into Low / Medium / High."""
    if not chem_text:
        return "Medium"
    text = chem_text.strip().lower()
    if text in ["excellent", "very good", "high"]:
        return "High"
    elif text in ["good", "medium", "moderate"]:
        return "Medium"
    else:
        return "Low"


def _map_weight_level(density):
    """Convert density (g/cm³) into Low / Medium / High weight."""
    if density is None:
        return "Medium"
    value = float(density)
    if value <= 1.0:
        return "Low"
    elif value <= 1.3:
        return "Medium"
    else:
        return "High"


def _score_application(user_application, material_applications):
    """Score application match (max 25 points) with expanded keywords."""
    if not user_application or not material_applications:
        return 0, "No application information available"

    user_app = user_application.lower().strip()
    mat_app = material_applications.lower()

    keywords = {
        "water pipe": ["pipe", "pipes", "piping", "plumbing", "tube"],
        "food container": ["bottle", "bottles", "packaging", "container", "food", "beverage", "packaging"],
        "automobile": ["automotive", "car", "vehicle", "auto", "automobile"],
        "electrical": ["cable", "cables", "electrical", "electronic", "housing", "insulat", "insulation", "wire"],
        "high temperature": ["high temperature", "heat", "thermal", "engine", "under-hood"],
        "packaging": ["packaging", "bottle", "container", "film"],
        "medical": ["medical", "hospital", "healthcare"],
        "construction": ["pipe", "window", "flooring", "construction", "building"],
        "gear": ["gear", "bearing", "mechanical", "fastener"],
        "insulation": ["insulat", "insulation", "cable", "electrical"]
    }

    score = 0
    reason = "Application does not closely match material's typical uses"

    for key, words in keywords.items():
        if key in user_app or any(w in user_app for w in words):
            if any(w in mat_app for w in words) or key in mat_app:
                score = 25
                reason = f"Strong match for '{user_application}' application"
                break
            else:
                score = max(score, 12)
                reason = f"Partial match for '{user_application}' application"

    if score == 0:
        user_words = set(user_app.replace("-", " ").split())
        mat_words = set(mat_app.replace(",", " ").replace("-", " ").split())
        common = user_words.intersection(mat_words)
        if common:
            score = 15
            reason = f"Some application keywords match ({', '.join(list(common)[:3])})"

    return score, reason


def _score_strength(user_strength, material_strength_value):
    material_level = _map_strength_level(material_strength_value)
    user_level = (user_strength or "Medium").strip().capitalize()

    levels = {"Low": 1, "Medium": 2, "High": 3}
    user_rank = levels.get(user_level, 2)
    mat_rank = levels.get(material_level, 2)

    if mat_rank >= user_rank:
        if mat_rank == user_rank:
            return 20, f"Strength matches requirement ({material_level})"
        return 18, f"Strength exceeds requirement (material is {material_level})"
    return 5, f"Strength is lower than required (material is {material_level})"


def _score_temperature(user_temp, material_max_temp):
    try:
        user_temp = int(user_temp)
        material_max_temp = int(material_max_temp)
    except (TypeError, ValueError):
        return 0, "Invalid temperature data"

    if user_temp <= material_max_temp:
        margin = material_max_temp - user_temp
        if margin >= 30:
            return 20, f"Excellent temperature margin (max {material_max_temp}°C)"
        if margin >= 10:
            return 18, f"Good temperature compatibility (max {material_max_temp}°C)"
        return 15, f"Acceptable temperature compatibility (max {material_max_temp}°C)"
    return 0, f"Exceeds maximum operating temperature ({material_max_temp}°C)"


def _score_chemical(user_chem, material_chem_text):
    material_level = _map_chemical_level(material_chem_text)
    user_level = (user_chem or "Medium").strip().capitalize()

    levels = {"Low": 1, "Medium": 2, "High": 3}
    user_rank = levels.get(user_level, 2)
    mat_rank = levels.get(material_level, 2)

    if mat_rank >= user_rank:
        if mat_rank == user_rank:
            return 15, f"Chemical resistance matches ({material_level})"
        return 14, f"Chemical resistance exceeds requirement ({material_level})"
    return 4, f"Chemical resistance is lower than required ({material_level})"


def _score_weight(user_weight, material_density):
    material_level = _map_weight_level(material_density)
    user_level = (user_weight or "Medium").strip().capitalize()

    if material_level == user_level:
        return 10, f"Weight category matches ({material_level} density)"
    if (user_level == "Low" and material_level == "Medium") or \
       (user_level == "Medium" and material_level in ["Low", "High"]):
        return 6, f"Weight is close (material is {material_level})"
    return 2, f"Weight does not match well (material is {material_level})"


def _score_cost(user_cost, material_cost):
    material_cost = (material_cost or "Medium").strip().capitalize()
    user_cost = (user_cost or "Medium").strip().capitalize()

    levels = {"Low": 1, "Medium": 2, "High": 3}
    user_rank = levels.get(user_cost, 2)
    mat_rank = levels.get(material_cost, 2)

    if mat_rank <= user_rank:
        if mat_rank == user_rank:
            return 10, f"Cost matches preference ({material_cost})"
        return 9, f"Cost is better than preferred ({material_cost})"
    return 3, f"Cost is higher than preferred ({material_cost})"


def recommend_materials(application, required_strength, operating_temperature,
                        weight_requirement, chemical_resistance, cost_preference):
    """
    Main recommendation function.
    Returns the top 3 materials with full explanation.
    """
    polymers = get_all_polymers()
    results = []

    for polymer in polymers:
        warnings = []
        reasons = []

        app_score, app_reason = _score_application(application, polymer.applications)
        str_score, str_reason = _score_strength(required_strength, polymer.strength)
        temp_score, temp_reason = _score_temperature(operating_temperature, polymer.max_temperature)
        chem_score, chem_reason = _score_chemical(chemical_resistance, polymer.chemical_resistance)
        weight_score, weight_reason = _score_weight(weight_requirement, polymer.density)
        cost_score, cost_reason = _score_cost(cost_preference, polymer.cost)

        total_score = (app_score + str_score + temp_score +
                       chem_score + weight_score + cost_score)

        reasons.extend([app_reason, str_reason, temp_reason,
                        chem_reason, weight_reason, cost_reason])

        # Critical warnings
        try:
            user_temp = int(operating_temperature)
            if user_temp > polymer.max_temperature:
                warnings.append(
                    f"Operating temperature ({user_temp}°C) exceeds material maximum ({polymer.max_temperature}°C)"
                )
        except (TypeError, ValueError):
            pass

        material_strength_level = _map_strength_level(polymer.strength)
        user_strength_level = (required_strength or "Medium").capitalize()
        levels = {"Low": 1, "Medium": 2, "High": 3}

        if levels.get(material_strength_level, 2) < levels.get(user_strength_level, 2):
            warnings.append(
                f"Material strength ({material_strength_level}) is lower than required ({user_strength_level})"
            )

        material_chem_level = _map_chemical_level(polymer.chemical_resistance)
        user_chem_level = (chemical_resistance or "Medium").capitalize()
        if levels.get(material_chem_level, 2) < levels.get(user_chem_level, 2):
            warnings.append(
                f"Chemical resistance ({material_chem_level}) is lower than required ({user_chem_level})"
            )

        results.append({
            "rank": 0,
            "material_id": polymer.id,
            "material_name": polymer.name,
            "category": polymer.category,
            "compatibility_score": total_score,
            "compatibility_percentage": round((total_score / 100) * 100, 1),
            "reasons": reasons,
            "advantages": polymer.advantages,
            "limitations": polymer.limitations,
            "warnings": warnings,
            "strength": float(polymer.strength) if polymer.strength is not None else None,
            "max_temperature": polymer.max_temperature,
            "density": float(polymer.density) if polymer.density is not None else None,
            "chemical_resistance": polymer.chemical_resistance,
            "cost": polymer.cost
        })

    results.sort(key=lambda x: x["compatibility_score"], reverse=True)
    top_3 = results[:3]

    for i, item in enumerate(top_3, start=1):
        item["rank"] = i

    return top_3