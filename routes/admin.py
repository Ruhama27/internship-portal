from flask import Blueprint, render_template, redirect, url_for, flash, request
from decorators import admin_required
from models import db, User, StudentProfile, CompanyProfile, Internship, Application

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    stats = {
        'students':     StudentProfile.query.count(),
        'companies':    CompanyProfile.query.count(),
        'internships':  Internship.query.count(),
        'active_internships': Internship.query.filter_by(is_active=True).count(),
        'applications': Application.query.count(),
        'accepted':     Application.query.filter_by(status='accepted').count(),
        'users':        User.query.count(),
    }
    recent_apps = (Application.query
                   .order_by(Application.applied_at.desc())
                   .limit(10).all())
    recent_internships = (Internship.query
                          .order_by(Internship.created_at.desc())
                          .limit(10).all())
    return render_template('admin/dashboard.html',
                           stats=stats,
                           recent_apps=recent_apps,
                           recent_internships=recent_internships)


@admin_bp.route('/users')
@admin_required
def users():
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=all_users)


@admin_bp.route('/user/<int:user_id>/toggle', methods=['POST'])
@admin_required
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.email} has been {status}.', 'info')
    return redirect(url_for('admin.users'))


@admin_bp.route('/internships')
@admin_required
def internships():
    all_internships = Internship.query.order_by(Internship.created_at.desc()).all()
    return render_template('admin/internships.html', internships=all_internships)
