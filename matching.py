"""
Internship Matching Engine
==========================
Calculates a match score between a StudentProfile and an Internship.

Score breakdown:
  40% — Skill match (required skills covered by student)
  30% — Field / education match
  20% — Interests match
  10% — Year-of-study bonus (prefer later years)
"""


def compute_match(student, internship):
    """
    Returns a dict with:
      score          (0-100 float)
      skill_score    (0-100)
      field_score    (0-100)
      interest_score (0-100)
      year_score     (0-100)
      matched_required  [Skill]
      missing_required  [Skill]
      matched_preferred [Skill]
      explanation    str
    """
    # ── 1. Skills (40%) ──────────────────────────────────────────────────────
    student_skill_ids = {s.id for s in student.skills}
    required = internship.required_skills
    preferred = internship.preferred_skills

    matched_required  = [s for s in required  if s.id in student_skill_ids]
    missing_required  = [s for s in required  if s.id not in student_skill_ids]
    matched_preferred = [s for s in preferred if s.id in student_skill_ids]

    if required:
        skill_score = len(matched_required) / len(required) * 100
    else:
        # Bonus if student has preferred skills and no required defined
        skill_score = (len(matched_preferred) / max(len(preferred), 1)) * 100

    # ── 2. Field / Education match (30%) ─────────────────────────────────────
    student_field = (student.field_of_study or '').lower().strip()
    internship_field = (internship.field or '').lower().strip()

    if student_field and internship_field:
        # Exact match
        if student_field == internship_field:
            field_score = 100.0
        # Partial word overlap
        elif any(word in internship_field for word in student_field.split() if len(word) > 3):
            field_score = 70.0
        elif any(word in student_field for word in internship_field.split() if len(word) > 3):
            field_score = 60.0
        else:
            field_score = 10.0
    else:
        field_score = 50.0  # Unknown — neutral

    # ── 3. Interests (20%) ───────────────────────────────────────────────────
    student_interest_ids = {i.id for i in student.interests}
    internship_tag_ids   = {t.id for t in internship.tags}

    if internship_tag_ids:
        overlap = len(student_interest_ids & internship_tag_ids)
        interest_score = overlap / len(internship_tag_ids) * 100
    else:
        interest_score = 50.0  # No tags — neutral

    # ── 4. Year of study (10%) ───────────────────────────────────────────────
    year = student.year_of_study or 0
    if year >= 4:
        year_score = 100.0
    elif year == 3:
        year_score = 80.0
    elif year == 2:
        year_score = 55.0
    elif year == 1:
        year_score = 30.0
    else:
        year_score = 50.0

    # ── Weighted total ────────────────────────────────────────────────────────
    total = (skill_score * 0.40 +
             field_score * 0.30 +
             interest_score * 0.20 +
             year_score * 0.10)

    # ── Explanation ───────────────────────────────────────────────────────────
    explanation_parts = []
    if matched_required:
        names = ', '.join(s.name for s in matched_required[:3])
        explanation_parts.append(
            f"Your skills include {names}, which are required for this internship."
        )
    if missing_required:
        names = ', '.join(s.name for s in missing_required[:2])
        explanation_parts.append(
            f"You are missing {names} — consider learning these to improve your match."
        )
    if field_score >= 70:
        explanation_parts.append(
            f"Your field of study ({student.field_of_study}) closely aligns with this internship."
        )
    if interest_score >= 60:
        explanation_parts.append("Your interests align well with this internship's focus area.")
    if not explanation_parts:
        explanation_parts.append("This internship has some potential alignment with your profile.")

    explanation = ' '.join(explanation_parts)

    return {
        'score':              round(total, 1),
        'skill_score':        round(skill_score, 1),
        'field_score':        round(field_score, 1),
        'interest_score':     round(interest_score, 1),
        'year_score':         round(year_score, 1),
        'matched_required':   matched_required,
        'missing_required':   missing_required,
        'matched_preferred':  matched_preferred,
        'explanation':        explanation,
    }


def get_recommendations(student, internships, limit=20):
    """
    Returns list of (internship, match_dict) sorted by match score descending.
    Only returns active internships.
    """
    results = []
    for internship in internships:
        if not internship.is_active:
            continue
        match = compute_match(student, internship)
        results.append((internship, match))
    results.sort(key=lambda x: x[1]['score'], reverse=True)
    return results[:limit]
