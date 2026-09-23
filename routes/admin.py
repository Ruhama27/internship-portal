from flask import Blueprint, render_template, redirect, url_for, flash, request
from decorators import admin_required
from models import db, User, StudentProfile, CompanyProfile, Internship, Application

admin_bp = Blueprint('admin', __name__)


# ─── Dashboard ────────────────────────────────────────────────────────────────

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    stats = {
        'students':           StudentProfile.query.count(),
        'companies':          CompanyProfile.query.count(),
        'internships':        Internship.query.count(),
        'active_internships': Internship.query.filter_by(is_active=True).count(),
        'applications':       Application.query.count(),
        'pending':            Application.query.filter_by(status='pending').count(),
        'accepted':           Application.query.filter_by(status='accepted').count(),
    }
    recent_apps = (Application.query
                   .order_by(Application.applied_at.desc())
                   .limit(8).all())
    recent_internships = (Internship.query
                          .order_by(Internship.created_at.desc())
                          .limit(8).all())
    return render_template('admin/dashboard.html',
                           stats=stats,
                           recent_apps=recent_apps,
                           recent_internships=recent_internships)


# ─── Company Management ───────────────────────────────────────────────────────

@admin_bp.route('/companies')
@admin_required
def companies():
    """List all companies and the Add Company form."""
    all_companies = (CompanyProfile.query
                     .join(User, User.id == CompanyProfile.user_id)
                     .order_by(CompanyProfile.company_name)
                     .all())
    return render_template('admin/companies.html', companies=all_companies)


@admin_bp.route('/companies/add', methods=['POST'])
@admin_required
def add_company():
    """University admin creates a new company account."""
    company_name  = request.form.get('company_name', '').strip()
    work_email    = request.form.get('work_email', '').strip().lower()
    password      = request.form.get('password', '').strip()
    phone         = request.form.get('phone', '').strip()
    website       = request.form.get('website', '').strip()
    location      = request.form.get('location', '').strip()
    industry      = request.form.get('industry', '').strip()
    description   = request.form.get('description', '').strip()

    if not company_name or not work_email or not password:
        flash('Company name, work email and password are required.', 'danger')
        return redirect(url_for('admin.companies'))

    if User.query.filter_by(email=work_email).first():
        flash(f'Email "{work_email}" is already registered in the system.', 'danger')
        return redirect(url_for('admin.companies'))

    user = User(email=work_email, role='company')
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    profile = CompanyProfile(
        user_id      = user.id,
        company_name = company_name,
        phone        = phone,
        website      = website,
        location     = location,
        industry     = industry,
        description  = description,
        contact_email= work_email,
    )
    db.session.add(profile)
    db.session.commit()
    flash(f'Company "{company_name}" has been added. They can now log in with {work_email}.', 'success')
    return redirect(url_for('admin.companies'))


@admin_bp.route('/companies/<int:company_id>/toggle', methods=['POST'])
@admin_required
def toggle_company(company_id):
    """Activate or deactivate a company account."""
    profile = CompanyProfile.query.get_or_404(company_id)
    user = profile.user
    user.is_active = not user.is_active
    db.session.commit()
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'Company "{profile.company_name}" has been {status}.', 'info')
    return redirect(url_for('admin.companies'))


@admin_bp.route('/companies/<int:company_id>/remove', methods=['POST'])
@admin_required
def remove_company(company_id):
    """Permanently remove a company and all their data."""
    profile = CompanyProfile.query.get_or_404(company_id)
    company_name = profile.company_name
    user = profile.user
    # Cascades will delete profile + internships + applications
    db.session.delete(user)
    db.session.commit()
    flash(f'Company "{company_name}" and all their data have been permanently removed.', 'warning')
    return redirect(url_for('admin.companies'))


# ─── Student Management ───────────────────────────────────────────────────────

@admin_bp.route('/students')
@admin_required
def students():
    """List all students."""
    all_students = (StudentProfile.query
                    .join(User, User.id == StudentProfile.user_id)
                    .order_by(StudentProfile.full_name)
                    .all())
    return render_template('admin/students.html', students=all_students)


@admin_bp.route('/students/<int:student_id>/toggle', methods=['POST'])
@admin_required
def toggle_student(student_id):
    """Activate or deactivate a student account."""
    profile = StudentProfile.query.get_or_404(student_id)
    user = profile.user
    user.is_active = not user.is_active
    db.session.commit()
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'Student "{profile.full_name or user.email}" has been {status}.', 'info')
    return redirect(url_for('admin.students'))


# ─── Internships Overview ─────────────────────────────────────────────────────

@admin_bp.route('/internships')
@admin_required
def internships():
    all_internships = Internship.query.order_by(Internship.created_at.desc()).all()
    return render_template('admin/internships.html', internships=all_internships)


# ─── Users (legacy redirect) ──────────────────────────────────────────────────

@admin_bp.route('/users')
@admin_required
def users():
    return redirect(url_for('admin.students'))
