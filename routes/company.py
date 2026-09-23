from flask import (Blueprint, render_template, redirect, url_for,
                   flash, request, jsonify)
from flask_login import current_user
from decorators import company_required
from models import db, Internship, Skill, Interest, Application, StudentProfile

company_bp = Blueprint('company', __name__)


# ─── Dashboard ────────────────────────────────────────────────────────────────

# ─── Dashboard ────────────────────────────────────────────────────────────────

@company_bp.route('/dashboard')
@company_required
def dashboard():
    company = current_user.company_profile
    internships = (Internship.query
                   .filter_by(company_id=company.id)
                   .order_by(Internship.created_at.desc())
                   .all())
    
    internship_ids = [i.id for i in internships]
    if internship_ids:
        all_apps = (Application.query
                    .filter(Application.internship_id.in_(internship_ids))
                    .order_by(Application.applied_at.desc())
                    .all())
    else:
        all_apps = []

    pending_apps = [a for a in all_apps if a.status == 'pending']
    accepted_apps = [a for a in all_apps if a.status == 'accepted']
    rejected_apps = [a for a in all_apps if a.status == 'rejected']
    active_count = sum(1 for i in internships if i.is_active)

    return render_template('company/dashboard.html',
                           company=company,
                           internships=internships,
                           all_apps=all_apps,
                           pending_apps=pending_apps,
                           accepted_apps=accepted_apps,
                           rejected_apps=rejected_apps,
                           total_apps=len(all_apps),
                           pending=len(pending_apps),
                           active_count=active_count)


# ─── All Applications (Approve / Decline) ───────────────────────────────────

@company_bp.route('/applications')
@company_required
def all_applications():
    company = current_user.company_profile
    status_filter = request.args.get('status', 'all').lower()
    internship_id = request.args.get('internship_id', type=int)

    internships = Internship.query.filter_by(company_id=company.id).all()
    internship_ids = [i.id for i in internships]

    if not internship_ids:
        return render_template('company/all_applications.html',
                               company=company,
                               applications=[],
                               internships=[],
                               current_status=status_filter,
                               current_internship_id=internship_id,
                               counts={'all': 0, 'pending': 0, 'accepted': 0, 'rejected': 0, 'interview': 0})

    query = Application.query.filter(Application.internship_id.in_(internship_ids))

    if internship_id:
        query = query.filter_by(internship_id=internship_id)

    if status_filter in ('pending', 'accepted', 'rejected', 'interview'):
        query = query.filter_by(status=status_filter)

    applications = query.order_by(Application.applied_at.desc()).all()

    # Get counts for tabs
    base_apps = Application.query.filter(Application.internship_id.in_(internship_ids)).all()
    counts = {
        'all': len(base_apps),
        'pending': sum(1 for a in base_apps if a.status == 'pending'),
        'accepted': sum(1 for a in base_apps if a.status == 'accepted'),
        'rejected': sum(1 for a in base_apps if a.status == 'rejected'),
        'interview': sum(1 for a in base_apps if a.status == 'interview'),
    }

    return render_template('company/all_applications.html',
                           company=company,
                           applications=applications,
                           internships=internships,
                           current_status=status_filter,
                           current_internship_id=internship_id,
                           counts=counts)


# ─── Company Profile & Password ───────────────────────────────────────────────

@company_bp.route('/profile', methods=['GET', 'POST'])
@company_required
def profile():
    company = current_user.company_profile
    if request.method == 'POST':
        action = request.form.get('action', 'profile')

        if action == 'password':
            new_password = request.form.get('new_password', '').strip()
            confirm_password = request.form.get('confirm_password', '').strip()
            if not new_password or len(new_password) < 6:
                flash('New password must be at least 6 characters long.', 'danger')
            elif new_password != confirm_password:
                flash('Passwords do not match.', 'danger')
            else:
                current_user.set_password(new_password)
                db.session.commit()
                flash('Your company admin password has been updated successfully!', 'success')
            return redirect(url_for('company.profile'))

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
        student_name = application.student.full_name or 'Student'
        status_labels = {
            'accepted': 'Approved (Accepted) 🎉',
            'rejected': 'Declined (Rejected)',
            'interview': 'Moved to Interview 💬',
            'pending': 'Moved to Pending ⏳',
        }
        flash(f'Application for {student_name} is now {status_labels.get(new_status, new_status)}.', 'success')

    # Allow custom redirect target
    next_url = request.form.get('next') or request.referrer
    if next_url:
        return redirect(next_url)
    return redirect(url_for('company.applicants', internship_id=application.internship_id))
