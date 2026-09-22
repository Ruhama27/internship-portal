import os
from flask import (Blueprint, render_template, redirect, url_for,
                   flash, request, current_app, jsonify)
from flask_login import current_user
from decorators import student_required
from models import db, Internship, Skill, Interest, Application
from matching import get_recommendations, compute_match

student_bp = Blueprint('student', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def secure_name(filename):
    """Simple secure filename without werkzeug dependency."""
    return filename.replace(' ', '_').replace('/', '_').replace('\\', '_')


# ─── Dashboard ────────────────────────────────────────────────────────────────

@student_bp.route('/dashboard')
@student_required
def dashboard():
    student = current_user.student_profile
    internships = Internship.query.filter_by(is_active=True).all()
    recommendations = get_recommendations(student, internships, limit=6)

    app_counts = {
        'total':     Application.query.filter_by(student_id=student.id).count(),
        'pending':   Application.query.filter_by(student_id=student.id, status='pending').count(),
        'interview': Application.query.filter_by(student_id=student.id, status='interview').count(),
        'accepted':  Application.query.filter_by(student_id=student.id, status='accepted').count(),
        'rejected':  Application.query.filter_by(student_id=student.id, status='rejected').count(),
    }
    return render_template('student/dashboard.html',
                           student=student,
                           recommendations=recommendations,
                           app_counts=app_counts)


# ─── Profile ──────────────────────────────────────────────────────────────────

@student_bp.route('/profile', methods=['GET', 'POST'])
@student_required
def profile():
    student = current_user.student_profile
    skills_by_cat = _group_skills()
    all_interests = Interest.query.order_by(Interest.name).all()

    if request.method == 'POST':
        # Basic info
        student.full_name          = request.form.get('full_name', '').strip()
        student.student_id         = request.form.get('student_id', '').strip()
        student.phone              = request.form.get('phone', '').strip()
        student.university         = request.form.get('university', '').strip()
        student.department         = request.form.get('department', '').strip()
        student.field_of_study     = request.form.get('field_of_study', '').strip()
        student.year_of_study      = request.form.get('year_of_study', type=int)
        student.expected_graduation= request.form.get('expected_graduation', '').strip()
        student.gpa                = request.form.get('gpa', type=float)
        student.location           = request.form.get('location', '').strip()
        student.bio                = request.form.get('bio', '').strip()

        # Skills
        selected_skill_ids = request.form.getlist('skills', type=int)
        student.skills = Skill.query.filter(Skill.id.in_(selected_skill_ids)).all()

        # Interests
        selected_interest_ids = request.form.getlist('interests', type=int)
        student.interests = Interest.query.filter(Interest.id.in_(selected_interest_ids)).all()

        # CV upload
        if 'cv' in request.files:
            cv_file = request.files['cv']
            if cv_file and cv_file.filename and allowed_file(cv_file.filename):
                filename = f"cv_{current_user.id}_{secure_name(cv_file.filename)}"
                cv_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                student.cv_filename = filename

        # Essay upload
        if 'essay' in request.files:
            essay_file = request.files['essay']
            if essay_file and essay_file.filename and allowed_file(essay_file.filename):
                filename = f"essay_{current_user.id}_{secure_name(essay_file.filename)}"
                essay_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                student.essay_filename = filename

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('student.profile'))

    return render_template('student/profile.html',
                           student=student,
                           skills_by_cat=skills_by_cat,
                           all_interests=all_interests)


# ─── Applications ─────────────────────────────────────────────────────────────

@student_bp.route('/applications')
@student_required
def applications():
    student = current_user.student_profile
    apps = (Application.query
            .filter_by(student_id=student.id)
            .order_by(Application.applied_at.desc())
            .all())
    return render_template('student/applications.html', student=student, apps=apps)


# ─── Saved ────────────────────────────────────────────────────────────────────

@student_bp.route('/saved')
@student_required
def saved():
    student = current_user.student_profile
    saved_list = student.saved
    results = []
    for internship in saved_list:
        match = compute_match(student, internship)
        results.append((internship, match))
    results.sort(key=lambda x: x[1]['score'], reverse=True)
    return render_template('student/saved.html', student=student, results=results)


@student_bp.route('/save/<int:internship_id>', methods=['POST'])
@student_required
def toggle_save(internship_id):
    student = current_user.student_profile
    internship = Internship.query.get_or_404(internship_id)
    if internship in student.saved:
        student.saved.remove(internship)
        saved = False
    else:
        student.saved.append(internship)
        saved = True
    db.session.commit()
    return jsonify({'saved': saved})


# ─── Apply ────────────────────────────────────────────────────────────────────

@student_bp.route('/apply/<int:internship_id>', methods=['POST'])
@student_required
def apply(internship_id):
    student = current_user.student_profile
    internship = Internship.query.get_or_404(internship_id)

    existing = Application.query.filter_by(
        student_id=student.id, internship_id=internship_id).first()
    if existing:
        flash('You have already applied to this internship.', 'info')
        return redirect(url_for('internship.detail', internship_id=internship_id))

    match = compute_match(student, internship)
    cover_letter = request.form.get('cover_letter', '')

    app = Application(
        student_id    = student.id,
        internship_id = internship_id,
        cover_letter  = cover_letter,
        match_score   = match['score'],
    )
    db.session.add(app)
    db.session.commit()
    flash(f'Application submitted! Your match score: {match["score"]}%', 'success')
    return redirect(url_for('student.applications'))


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _group_skills():
    """Returns dict of {category: [Skill]} ordered by category."""
    skills = Skill.query.order_by(Skill.category, Skill.name).all()
    groups = {}
    for skill in skills:
        cat = skill.category or 'Other'
        groups.setdefault(cat, []).append(skill)
    return groups
