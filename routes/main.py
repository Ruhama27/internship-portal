from flask import Blueprint, render_template
from flask_login import current_user
from models import Internship, StudentProfile, CompanyProfile, Application, User

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    stats = {
        'students':     StudentProfile.query.count(),
        'companies':    CompanyProfile.query.count(),
        'internships':  Internship.query.filter_by(is_active=True).count(),
        'applications': Application.query.count(),
    }
    featured = Internship.query.filter_by(is_active=True).order_by(
        Internship.created_at.desc()).limit(6).all()
    return render_template('landing.html', stats=stats, featured=featured)
