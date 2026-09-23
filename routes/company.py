from flask import (Blueprint, render_template, redirect, url_for,
                   flash, request, jsonify)
from flask_login import current_user
from decorators import company_required
from models import db, Internship, Skill, Interest, Application, StudentProfile

company_bp = Blueprint('company', __name__)


# ─── Dashboard ────────────────────────────────────────────────────────────────

@company_bp.route('/dashboard')
@company_required
def dashboard():
    company = current_user.company_profile
    internships = (Internship.query
                   .filter_by(company_id=company.id)
                   .order_by(Internship.created_at.desc())
                   .all())
    total_apps = sum(len(i.applications) for i in internships)
    pending    = sum(sum(1 for a in i.applications if a.status == 'pending') for i in internships)
    active_count = sum(1 for i in internships if i.is_active)
    return render_template('company/dashboard.html',
                           company=company,
                           internships=internships,
                           total_apps=total_apps,
                           pending=pending,
                           active_count=active_count)


# ─── Company Profile ──────────────────────────────────────────────────────────

@company_bp.route('/profile', methods=['GET', 'POST'])
@company_required
def profile():
    company = current_user.company_profile
    if request.method == 'POST':
        company.company_name  = request.form.get('company_name', '').strip()
        company.phone         = request.form.get('phone', '').strip()
        company.website       = request.form.get('website', '').strip()
        company.location      = request.form.get('location', '').strip()
        company.industry      = request.form.get('industry', '').strip()
        company.description   = request.form.get('description', '').strip()
        company.contact_email = request.form.get('contact_email', '').strip()
        db.session.commit()
        flash('Company profile updated!', 'success')
        return redirect(url_for('company.profile'))
    return render_template('company/profile.html', company=company)


# ─── Post Internship ──────────────────────────────────────────────────────────

@company_bp.route('/post', methods=['GET', 'POST'])
@company_required
def post_internship():
    company = current_user.company_profile
    all_skills    = Skill.query.order_by(Skill.category, Skill.name).all()
    all_interests = Interest.query.order_by(Interest.name).all()

    if request.method == 'POST':
        title       = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        field       = request.form.get('field', '').strip()
        location    = request.form.get('location', '').strip()
        work_type   = request.form.get('work_type', 'on-site')
        num_students= request.form.get('num_students', 1, type=int)
        start_date  = request.form.get('start_date') or None
        end_date    = request.form.get('end_date') or None
        deadline    = request.form.get('deadline') or None
        contact_email = request.form.get('contact_email', company.contact_email or '').strip()

        req_skill_ids  = request.form.getlist('required_skills', type=int)
        pref_skill_ids = request.form.getlist('preferred_skills', type=int)
        tag_ids        = request.form.getlist('tags', type=int)

        if not title:
            flash('Internship title is required.', 'danger')
        else:
            internship = Internship(
                company_id    = company.id,
                title         = title,
                description   = description,
                field         = field,
                location      = location,
                work_type     = work_type,
                num_students  = num_students,
                contact_email = contact_email,
            )
            # Parse dates
            from datetime import date
            try:
                if start_date:
                    internship.start_date = date.fromisoformat(start_date)
                if end_date:
                    internship.end_date = date.fromisoformat(end_date)
                if deadline:
                    internship.deadline = date.fromisoformat(deadline)
            except ValueError:
                pass

            internship.required_skills  = Skill.query.filter(Skill.id.in_(req_skill_ids)).all()
            internship.preferred_skills = Skill.query.filter(Skill.id.in_(pref_skill_ids)).all()
            internship.tags             = Interest.query.filter(Interest.id.in_(tag_ids)).all()

            db.session.add(internship)
            db.session.commit()
            flash(f'Internship "{title}" posted successfully!', 'success')
            return redirect(url_for('company.dashboard'))

    skills_by_cat = {}
    for skill in all_skills:
        skills_by_cat.setdefault(skill.category or 'Other', []).append(skill)

    return render_template('company/post_internship.html',
                           company=company,
                           skills_by_cat=skills_by_cat,
                           all_interests=all_interests)


# ─── Edit Internship ──────────────────────────────────────────────────────────

@company_bp.route('/internship/<int:internship_id>/edit', methods=['GET', 'POST'])
@company_required
def edit_internship(internship_id):
    company = current_user.company_profile
    internship = Internship.query.filter_by(id=internship_id, company_id=company.id).first_or_404()
    all_skills    = Skill.query.order_by(Skill.category, Skill.name).all()
    all_interests = Interest.query.order_by(Interest.name).all()

    if request.method == 'POST':
        internship.title       = request.form.get('title', '').strip()
        internship.description = request.form.get('description', '').strip()
        internship.field       = request.form.get('field', '').strip()
        internship.location    = request.form.get('location', '').strip()
        internship.work_type   = request.form.get('work_type', 'on-site')
        internship.num_students= request.form.get('num_students', 1, type=int)
        internship.contact_email = request.form.get('contact_email', '').strip()
        internship.is_active   = 'is_active' in request.form

        req_skill_ids  = request.form.getlist('required_skills', type=int)
        pref_skill_ids = request.form.getlist('preferred_skills', type=int)
        tag_ids        = request.form.getlist('tags', type=int)

        from datetime import date
        try:
            start = request.form.get('start_date')
            end   = request.form.get('end_date')
            dl    = request.form.get('deadline')
            if start: internship.start_date = date.fromisoformat(start)
            if end:   internship.end_date   = date.fromisoformat(end)
            if dl:    internship.deadline   = date.fromisoformat(dl)
        except ValueError:
            pass

        internship.required_skills  = Skill.query.filter(Skill.id.in_(req_skill_ids)).all()
        internship.preferred_skills = Skill.query.filter(Skill.id.in_(pref_skill_ids)).all()
        internship.tags             = Interest.query.filter(Interest.id.in_(tag_ids)).all()

        db.session.commit()
        flash('Internship updated!', 'success')
        return redirect(url_for('company.dashboard'))

    skills_by_cat = {}
    for skill in all_skills:
        skills_by_cat.setdefault(skill.category or 'Other', []).append(skill)

    return render_template('company/post_internship.html',
                           company=company,
                           internship=internship,
                           skills_by_cat=skills_by_cat,
                           all_interests=all_interests,
                           edit_mode=True)


# ─── Delete Internship ────────────────────────────────────────────────────────

@company_bp.route('/internship/<int:internship_id>/delete', methods=['POST'])
@company_required
def delete_internship(internship_id):
    company = current_user.company_profile
    internship = Internship.query.filter_by(id=internship_id, company_id=company.id).first_or_404()
    db.session.delete(internship)
    db.session.commit()
    flash('Internship deleted.', 'info')
    return redirect(url_for('company.dashboard'))


# ─── View Applicants ──────────────────────────────────────────────────────────

@company_bp.route('/internship/<int:internship_id>/applicants')
@company_required
def applicants(internship_id):
    company = current_user.company_profile
    internship = Internship.query.filter_by(id=internship_id, company_id=company.id).first_or_404()
    apps = (Application.query
            .filter_by(internship_id=internship_id)
            .order_by(Application.applied_at.desc())
            .all())
    return render_template('company/applicants.html',
                           company=company,
                           internship=internship,
                           apps=apps)


# ─── Update Application Status ────────────────────────────────────────────────

@company_bp.route('/application/<int:app_id>/status', methods=['POST'])
@company_required
def update_status(app_id):
    application = Application.query.get_or_404(app_id)
    # Verify this application belongs to one of the company's internships
    company = current_user.company_profile
    if application.internship.company_id != company.id:
        return jsonify({'error': 'Forbidden'}), 403
    new_status = request.form.get('status')
    if new_status in ('pending', 'interview', 'accepted', 'rejected'):
        application.status = new_status
        db.session.commit()
        flash(f'Application status updated to {new_status}.', 'success')
    return redirect(url_for('company.applicants',
                            internship_id=application.internship_id))
