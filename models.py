from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ─── Association Tables ───────────────────────────────────────────────────────

student_skills = db.Table('student_skills',
    db.Column('student_id', db.Integer, db.ForeignKey('student_profiles.id'), primary_key=True),
    db.Column('skill_id',   db.Integer, db.ForeignKey('skills.id'),           primary_key=True)
)

student_interests = db.Table('student_interests',
    db.Column('student_id',  db.Integer, db.ForeignKey('student_profiles.id'), primary_key=True),
    db.Column('interest_id', db.Integer, db.ForeignKey('interests.id'),         primary_key=True)
)

internship_required_skills = db.Table('internship_required_skills',
    db.Column('internship_id', db.Integer, db.ForeignKey('internships.id'), primary_key=True),
    db.Column('skill_id',      db.Integer, db.ForeignKey('skills.id'),      primary_key=True)
)

internship_preferred_skills = db.Table('internship_preferred_skills',
    db.Column('internship_id', db.Integer, db.ForeignKey('internships.id'), primary_key=True),
    db.Column('skill_id',      db.Integer, db.ForeignKey('skills.id'),      primary_key=True)
)

internship_interests = db.Table('internship_interests',
    db.Column('internship_id', db.Integer, db.ForeignKey('internships.id'), primary_key=True),
    db.Column('interest_id',   db.Integer, db.ForeignKey('interests.id'),   primary_key=True)
)

saved_internships = db.Table('saved_internships',
    db.Column('student_id',    db.Integer, db.ForeignKey('student_profiles.id'), primary_key=True),
    db.Column('internship_id', db.Integer, db.ForeignKey('internships.id'),      primary_key=True)
)


# ─── Core Models ──────────────────────────────────────────────────────────────

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id         = db.Column(db.Integer, primary_key=True)
    email      = db.Column(db.String(150), unique=True, nullable=False)
    password   = db.Column(db.String(200), nullable=False)
    role       = db.Column(db.String(20),  nullable=False)  # student / company / admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active  = db.Column(db.Boolean, default=True)

    student_profile = db.relationship('StudentProfile', backref='user', uselist=False,
                                       cascade='all, delete-orphan')
    company_profile = db.relationship('CompanyProfile', backref='user', uselist=False,
                                       cascade='all, delete-orphan')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def display_name(self):
        if self.role == 'student' and self.student_profile:
            return self.student_profile.full_name
        if self.role == 'company' and self.company_profile:
            return self.company_profile.company_name
        if self.role == 'admin':
            return 'Admin'
        return self.email


class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'
    id                  = db.Column(db.Integer, primary_key=True)
    user_id             = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    student_id          = db.Column(db.String(50), unique=True)
    full_name           = db.Column(db.String(150))
    phone               = db.Column(db.String(30))
    university          = db.Column(db.String(200))
    department          = db.Column(db.String(200))
    field_of_study      = db.Column(db.String(200))
    year_of_study       = db.Column(db.Integer)
    expected_graduation = db.Column(db.String(20))
    gpa                 = db.Column(db.Float)
    location            = db.Column(db.String(200))
    bio                 = db.Column(db.Text)
    cv_filename         = db.Column(db.String(300))
    essay_filename      = db.Column(db.String(300))
    avatar_filename     = db.Column(db.String(300))
    updated_at          = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    skills    = db.relationship('Skill',    secondary=student_skills,    backref='students')
    interests = db.relationship('Interest', secondary=student_interests, backref='students')
    applications = db.relationship('Application', backref='student', cascade='all, delete-orphan')
    saved     = db.relationship('Internship', secondary=saved_internships, backref='savers')

    @property
    def completion_percent(self):
        fields = [
            self.full_name, self.phone, self.university, self.department,
            self.field_of_study, self.year_of_study, self.expected_graduation,
            self.location, self.bio, self.cv_filename, self.essay_filename
        ]
        filled = sum(1 for f in fields if f)
        skills_done = 1 if self.skills else 0
        interests_done = 1 if self.interests else 0
        total = len(fields) + 2
        return int((filled + skills_done + interests_done) / total * 100)


class CompanyProfile(db.Model):
    __tablename__ = 'company_profiles'
    id               = db.Column(db.Integer, primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_name     = db.Column(db.String(200))
    phone            = db.Column(db.String(30))
    website          = db.Column(db.String(300))
    location         = db.Column(db.String(200))
    industry         = db.Column(db.String(200))
    description      = db.Column(db.Text)
    logo_filename    = db.Column(db.String(300))
    contact_email    = db.Column(db.String(150))
    updated_at       = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    internships = db.relationship('Internship', backref='company', cascade='all, delete-orphan')


class Skill(db.Model):
    __tablename__ = 'skills'
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(100))  # Programming, Web, Database, etc.

    def __repr__(self):
        return f'<Skill {self.name}>'


class Interest(db.Model):
    __tablename__ = 'interests'
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Interest {self.name}>'


class Internship(db.Model):
    __tablename__ = 'internships'
    id               = db.Column(db.Integer, primary_key=True)
    company_id       = db.Column(db.Integer, db.ForeignKey('company_profiles.id'), nullable=False)
    title            = db.Column(db.String(200), nullable=False)
    description      = db.Column(db.Text)
    field            = db.Column(db.String(200))
    location         = db.Column(db.String(200))
    work_type        = db.Column(db.String(30))   # remote / on-site / hybrid
    num_students     = db.Column(db.Integer)
    start_date       = db.Column(db.Date)
    end_date         = db.Column(db.Date)
    deadline         = db.Column(db.Date)
    contact_email    = db.Column(db.String(150))
    is_active        = db.Column(db.Boolean, default=True)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)

    required_skills  = db.relationship('Skill', secondary=internship_required_skills,
                                        backref='required_by')
    preferred_skills = db.relationship('Skill', secondary=internship_preferred_skills,
                                        backref='preferred_by')
    tags             = db.relationship('Interest', secondary=internship_interests,
                                        backref='internships')
    applications     = db.relationship('Application', backref='internship',
                                        cascade='all, delete-orphan')


class Application(db.Model):
    __tablename__ = 'applications'
    id           = db.Column(db.Integer, primary_key=True)
    student_id   = db.Column(db.Integer, db.ForeignKey('student_profiles.id'), nullable=False)
    internship_id= db.Column(db.Integer, db.ForeignKey('internships.id'),      nullable=False)
    cover_letter = db.Column(db.Text)
    status       = db.Column(db.String(30), default='pending')
    # pending / interview / accepted / rejected
    match_score  = db.Column(db.Float)
    applied_at   = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at   = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('student_id', 'internship_id', name='unique_application'),
    )
