from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user, login_required
from models import db, User, StudentProfile, CompanyProfile

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return _redirect_dashboard()
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            flash(f'Welcome back, {user.display_name}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or _redirect_dashboard())
        flash('Invalid email or password.', 'danger')
    return render_template('auth/login.html')


@auth_bp.route('/register/student', methods=['GET', 'POST'])
def register_student():
    if current_user.is_authenticated:
        return _redirect_dashboard()
    if request.method == 'POST':
        email      = request.form.get('email', '').strip().lower()
        password   = request.form.get('password', '')
        confirm    = request.form.get('confirm_password', '')
        full_name  = request.form.get('full_name', '').strip()
        student_id = request.form.get('student_id', '').strip()
        university = request.form.get('university', '').strip()
        department = request.form.get('department', '').strip()
        year       = request.form.get('year_of_study', 1, type=int)

        if password != confirm:
            flash('Passwords do not match.', 'danger')
        elif User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
        else:
            user = User(email=email, role='student')
            user.set_password(password)
            db.session.add(user)
            db.session.flush()

            profile = StudentProfile(
                user_id      = user.id,
                full_name    = full_name,
                student_id   = student_id,
                university   = university,
                department   = department,
                year_of_study= year,
            )
            db.session.add(profile)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created! Complete your profile to get started.', 'success')
            return redirect(url_for('student.profile'))
    return render_template('auth/register_student.html')


@auth_bp.route('/register/company', methods=['GET', 'POST'])
def register_company():
    if current_user.is_authenticated:
        return _redirect_dashboard()
    if request.method == 'POST':
        email        = request.form.get('email', '').strip().lower()
        password     = request.form.get('password', '')
        confirm      = request.form.get('confirm_password', '')
        company_name = request.form.get('company_name', '').strip()
        phone        = request.form.get('phone', '').strip()
        website      = request.form.get('website', '').strip()
        location     = request.form.get('location', '').strip()
        description  = request.form.get('description', '').strip()

        if password != confirm:
            flash('Passwords do not match.', 'danger')
        elif User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
        else:
            user = User(email=email, role='company')
            user.set_password(password)
            db.session.add(user)
            db.session.flush()

            profile = CompanyProfile(
                user_id      = user.id,
                company_name = company_name,
                phone        = phone,
                website      = website,
                location     = location,
                description  = description,
                contact_email= email,
            )
            db.session.add(profile)
            db.session.commit()
            login_user(user, remember=True)
            flash('Company account created! Post your first internship.', 'success')
            return redirect(url_for('company.dashboard'))
    return render_template('auth/register_company.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


def _redirect_dashboard():
    if current_user.role == 'student':
        return url_for('student.dashboard')
    elif current_user.role == 'company':
        return url_for('company.dashboard')
    elif current_user.role == 'admin':
        return url_for('admin.dashboard')
    return url_for('main.index')
