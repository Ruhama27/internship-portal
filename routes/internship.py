from flask import Blueprint, render_template, request
from flask_login import current_user
from models import Internship, Skill, Interest, Application

internship_bp = Blueprint('internship', __name__)


@internship_bp.route('/')
def search():
    """Search & filter internships."""
    q         = request.args.get('q', '').strip()
    field     = request.args.get('field', '').strip()
    location  = request.args.get('location', '').strip()
    work_type = request.args.getlist('work_type')
    skill_ids = request.args.getlist('skills', type=int)

    query = Internship.query.filter_by(is_active=True)

    if q:
        query = query.filter(
            Internship.title.ilike(f'%{q}%') |
            Internship.description.ilike(f'%{q}%')
        )
    if field:
        query = query.filter(Internship.field.ilike(f'%{field}%'))
    if location:
        query = query.filter(Internship.location.ilike(f'%{location}%'))
    if work_type:
        query = query.filter(Internship.work_type.in_(work_type))

    internships = query.order_by(Internship.created_at.desc()).all()

    # Skill filter (post-query since it's a many-to-many)
    if skill_ids:
        internships = [
            i for i in internships
            if any(s.id in skill_ids for s in i.required_skills)
        ]

    all_skills = Skill.query.order_by(Skill.name).all()
    fields = (Internship.query
              .with_entities(Internship.field)
              .filter(Internship.is_active == True, Internship.field != None)
              .distinct().all())
    fields = sorted(set(f[0] for f in fields if f[0]))

    return render_template('internship/search.html',
                           internships=internships,
                           all_skills=all_skills,
                           fields=fields,
                           q=q,
                           selected_field=field,
                           selected_location=location,
                           selected_work_type=work_type,
                           selected_skills=skill_ids)


@internship_bp.route('/<int:internship_id>')
def detail(internship_id):
    internship = Internship.query.get_or_404(internship_id)
    already_applied = False
    is_saved = False

    if current_user.is_authenticated and current_user.role == 'student':
        student = current_user.student_profile
        already_applied = Application.query.filter_by(
            student_id=student.id,
            internship_id=internship_id
        ).first() is not None
        is_saved = internship in student.saved

    return render_template('internship/detail.html',
                           internship=internship,
                           already_applied=already_applied,
                           is_saved=is_saved)
