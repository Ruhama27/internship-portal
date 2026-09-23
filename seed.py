"""
seed.py — Populates the database with initial data.
Run automatically on first startup (if tables are empty).
"""
from models import db, User, StudentProfile, CompanyProfile, Skill, Interest, Internship, Application
from datetime import date


SKILLS_DATA = [
    # Programming
    ('Python',       'Programming'),
    ('Java',         'Programming'),
    ('JavaScript',   'Programming'),
    ('C++',          'Programming'),
    ('C#',           'Programming'),
    ('TypeScript',   'Programming'),
    ('Go',           'Programming'),
    ('Kotlin',       'Programming'),
    # Web
    ('HTML',         'Web'),
    ('CSS',          'Web'),
    ('React',        'Web'),
    ('Vue.js',       'Web'),
    ('Angular',      'Web'),
    ('Node.js',      'Web'),
    ('Django',       'Web'),
    ('Flask',        'Web'),
    ('REST API',     'Web'),
    ('GraphQL',      'Web'),
    # Database
    ('MySQL',        'Database'),
    ('PostgreSQL',   'Database'),
    ('MongoDB',      'Database'),
    ('SQLite',       'Database'),
    ('Redis',        'Database'),
    # DevOps / Tools
    ('Git',          'Tools'),
    ('Docker',       'Tools'),
    ('Linux',        'Tools'),
    ('AWS',          'Cloud'),
    ('Azure',        'Cloud'),
    # Data Science
    ('Machine Learning', 'Data Science'),
    ('TensorFlow',   'Data Science'),
    ('PyTorch',      'Data Science'),
    ('Data Analysis','Data Science'),
    ('Pandas',       'Data Science'),
    ('NumPy',        'Data Science'),
    ('SQL',          'Data Science'),
    # Design
    ('Figma',        'Design'),
    ('UI/UX Design', 'Design'),
    # Networking
    ('Cisco',        'Networking'),
    ('Network Security', 'Networking'),
]

INTERESTS_DATA = [
    'Web Development',
    'Mobile Development',
    'Artificial Intelligence',
    'Machine Learning',
    'Data Science',
    'Cybersecurity',
    'Networking',
    'Cloud Computing',
    'DevOps',
    'Software Engineering',
    'Game Development',
    'UI/UX Design',
    'Embedded Systems',
    'Blockchain',
    'Database Administration',
]

COMPANIES_DATA = [
    {
        'email': 'abc@techcorp.com',
        'company_name': 'ABC Technology',
        'phone': '+251-11-234-5678',
        'website': 'https://abctechcorp.example.com',
        'location': 'Addis Ababa, Ethiopia',
        'industry': 'Software Development',
        'description': 'ABC Technology is a leading software development company specializing in enterprise web applications, mobile solutions, and cloud infrastructure. We are passionate about mentoring the next generation of developers.',
        'contact_email': 'hr@abctechcorp.example.com',
    },
    {
        'email': 'xyz@solutions.com',
        'company_name': 'XYZ Solutions',
        'phone': '+251-11-345-6789',
        'website': 'https://xyzsolutions.example.com',
        'location': 'Addis Ababa, Ethiopia',
        'industry': 'Data Analytics',
        'description': 'XYZ Solutions is a data analytics and AI company helping businesses transform data into actionable insights. We work on cutting-edge machine learning and data engineering projects.',
        'contact_email': 'careers@xyzsolutions.example.com',
    },
    {
        'email': 'nova@digital.com',
        'company_name': 'Nova Digital Agency',
        'phone': '+251-11-456-7890',
        'website': 'https://novadigital.example.com',
        'location': 'Addis Ababa, Ethiopia',
        'industry': 'Digital Marketing & Design',
        'description': 'Nova Digital is a creative agency blending beautiful design with powerful technology. We build brands, websites, and digital products that inspire.',
        'contact_email': 'hello@novadigital.example.com',
    },
    {
        'email': 'cyber@shield.com',
        'company_name': 'CyberShield Inc.',
        'phone': '+251-11-567-8901',
        'website': 'https://cybershield.example.com',
        'location': 'Addis Ababa, Ethiopia',
        'industry': 'Cybersecurity',
        'description': 'CyberShield Inc. is a cybersecurity firm protecting critical infrastructure and private organizations from digital threats. We offer hands-on learning in ethical hacking, network security, and incident response.',
        'contact_email': 'internships@cybershield.example.com',
    },
]


def seed_data():
    """Seeds data if the database is empty."""
    if Skill.query.count() > 0:
        return  # Already seeded

    print("[+] Seeding database...")

    # Skills
    skill_map = {}
    for name, category in SKILLS_DATA:
        skill = Skill(name=name, category=category)
        db.session.add(skill)
        skill_map[name] = skill

    # Interests
    interest_map = {}
    for name in INTERESTS_DATA:
        interest = Interest(name=name)
        db.session.add(interest)
        interest_map[name] = interest

    db.session.flush()

    # University Admin user (Debre Berhan University)
    admin_dbu = User(email='admin@dbu.edu.et', role='admin')
    admin_dbu.set_password('admin123')
    db.session.add(admin_dbu)

    admin_legacy = User(email='admin@internmatch.com', role='admin')
    admin_legacy.set_password('admin123')
    db.session.add(admin_legacy)

    # Demo student
    student_user = User(email='ruhama@student.com', role='student')
    student_user.set_password('student123')
    db.session.add(student_user)
    db.session.flush()

    student_profile = StudentProfile(
        user_id          = student_user.id,
        student_id       = 'DBU/001/2022',
        full_name        = 'Ruhama Nigusu',
        phone            = '+251 91 234 5678',
        university       = 'Debre Berhan University',
        department       = 'Computer Science',
        field_of_study   = 'Software Engineering',
        year_of_study    = 3,
        expected_graduation = '2025',
        gpa              = 3.8,
        location         = 'Addis Ababa, Ethiopia',
        bio              = 'Passionate software engineering student with hands-on experience in web development and a keen interest in AI/ML.',
    )
    db.session.add(student_profile)
    db.session.flush()

    # Add skills and interests to demo student
    student_skills_list = ['Python', 'JavaScript', 'React', 'HTML', 'CSS', 'MySQL', 'Git']
    student_profile.skills = [skill_map[s] for s in student_skills_list if s in skill_map]

    student_interests_list = ['Web Development', 'Artificial Intelligence', 'Software Engineering']
    student_profile.interests = [interest_map[i] for i in student_interests_list if i in interest_map]

    # Companies
    company_profiles = []
    for cdata in COMPANIES_DATA:
        cuser = User(email=cdata['email'], role='company')
        cuser.set_password('company123')
        db.session.add(cuser)
        db.session.flush()

        cp = CompanyProfile(
            user_id      = cuser.id,
            company_name = cdata['company_name'],
            phone        = cdata['phone'],
            website      = cdata['website'],
            location     = cdata['location'],
            industry     = cdata['industry'],
            description  = cdata['description'],
            contact_email= cdata['contact_email'],
        )
        db.session.add(cp)
        db.session.flush()
        company_profiles.append(cp)

    abc, xyz, nova, cyber = company_profiles

    # Internships
    internships_data = [
        {
            'company': abc,
            'title': 'Frontend Developer Intern',
            'description': 'Join our frontend team to build responsive, beautiful web interfaces using React. You will work on real client projects, collaborate with senior developers, and learn modern web development best practices.',
            'field': 'Software Engineering',
            'location': 'Addis Ababa, Ethiopia',
            'work_type': 'hybrid',
            'num_students': 3,
            'start_date': date(2025, 1, 15),
            'end_date': date(2025, 6, 15),
            'deadline': date(2024, 12, 31),
            'contact_email': 'hr@abctechcorp.example.com',
            'required': ['React', 'JavaScript', 'HTML', 'CSS'],
            'preferred': ['TypeScript', 'Git', 'REST API'],
            'tags': ['Web Development', 'Software Engineering'],
        },
        {
            'company': abc,
            'title': 'Backend Developer Intern',
            'description': 'Work with our backend team using Python and Django to build scalable APIs. You will design database schemas, implement REST endpoints, and write unit tests.',
            'field': 'Software Engineering',
            'location': 'Addis Ababa, Ethiopia',
            'work_type': 'on-site',
            'num_students': 2,
            'start_date': date(2025, 2, 1),
            'end_date': date(2025, 7, 1),
            'deadline': date(2025, 1, 15),
            'contact_email': 'hr@abctechcorp.example.com',
            'required': ['Python', 'Django', 'MySQL', 'REST API'],
            'preferred': ['Docker', 'Git', 'PostgreSQL'],
            'tags': ['Web Development', 'Software Engineering'],
        },
        {
            'company': xyz,
            'title': 'Data Science Intern',
            'description': 'Dive into real-world data science projects: building predictive models, cleaning datasets, creating visualizations, and presenting insights to clients.',
            'field': 'Data Science',
            'location': 'Addis Ababa, Ethiopia',
            'work_type': 'remote',
            'num_students': 4,
            'start_date': date(2025, 1, 20),
            'end_date': date(2025, 7, 20),
            'deadline': date(2025, 1, 5),
            'contact_email': 'careers@xyzsolutions.example.com',
            'required': ['Python', 'Data Analysis', 'Pandas', 'NumPy'],
            'preferred': ['Machine Learning', 'SQL', 'TensorFlow'],
            'tags': ['Data Science', 'Machine Learning', 'Artificial Intelligence'],
        },
        {
            'company': xyz,
            'title': 'Machine Learning Intern',
            'description': 'Help our AI team build and fine-tune machine learning models for natural language processing and computer vision tasks.',
            'field': 'Artificial Intelligence',
            'location': 'Addis Ababa, Ethiopia',
            'work_type': 'hybrid',
            'num_students': 2,
            'start_date': date(2025, 3, 1),
            'end_date': date(2025, 9, 1),
            'deadline': date(2025, 2, 1),
            'contact_email': 'careers@xyzsolutions.example.com',
            'required': ['Python', 'Machine Learning', 'TensorFlow'],
            'preferred': ['PyTorch', 'Data Analysis', 'NumPy'],
            'tags': ['Artificial Intelligence', 'Machine Learning', 'Data Science'],
        },
        {
            'company': nova,
            'title': 'UI/UX Design Intern',
            'description': 'Create stunning user interfaces and experiences. You will conduct user research, build wireframes, and design high-fidelity prototypes using Figma.',
            'field': 'Design',
            'location': 'Addis Ababa, Ethiopia',
            'work_type': 'on-site',
            'num_students': 2,
            'start_date': date(2025, 2, 15),
            'end_date': date(2025, 6, 15),
            'deadline': date(2025, 2, 1),
            'contact_email': 'hello@novadigital.example.com',
            'required': ['Figma', 'UI/UX Design'],
            'preferred': ['HTML', 'CSS', 'JavaScript'],
            'tags': ['UI/UX Design', 'Web Development'],
        },
        {
            'company': nova,
            'title': 'Full Stack Developer Intern',
            'description': 'Work on end-to-end web application development. You will build features from database design to responsive UI.',
            'field': 'Software Engineering',
            'location': 'Addis Ababa, Ethiopia',
            'work_type': 'hybrid',
            'num_students': 3,
            'start_date': date(2025, 1, 10),
            'end_date': date(2025, 7, 10),
            'deadline': date(2024, 12, 20),
            'contact_email': 'hello@novadigital.example.com',
            'required': ['JavaScript', 'React', 'Node.js', 'MySQL'],
            'preferred': ['TypeScript', 'MongoDB', 'Docker'],
            'tags': ['Web Development', 'Software Engineering'],
        },
        {
            'company': cyber,
            'title': 'Cybersecurity Intern',
            'description': 'Learn the fundamentals of offensive and defensive security. You will participate in vulnerability assessments, penetration testing, and security audits.',
            'field': 'Cybersecurity',
            'location': 'Addis Ababa, Ethiopia',
            'work_type': 'on-site',
            'num_students': 2,
            'start_date': date(2025, 2, 1),
            'end_date': date(2025, 8, 1),
            'deadline': date(2025, 1, 10),
            'contact_email': 'internships@cybershield.example.com',
            'required': ['Network Security', 'Linux'],
            'preferred': ['Python', 'Cisco'],
            'tags': ['Cybersecurity', 'Networking'],
        },
    ]

    for idata in internships_data:
        internship = Internship(
            company_id    = idata['company'].id,
            title         = idata['title'],
            description   = idata['description'],
            field         = idata['field'],
            location      = idata['location'],
            work_type     = idata['work_type'],
            num_students  = idata['num_students'],
            start_date    = idata['start_date'],
            end_date      = idata['end_date'],
            deadline      = idata['deadline'],
            contact_email = idata['contact_email'],
            is_active     = True,
        )
        internship.required_skills  = [skill_map[s] for s in idata['required']  if s in skill_map]
        internship.preferred_skills = [skill_map[s] for s in idata['preferred'] if s in skill_map]
        internship.tags             = [interest_map[t] for t in idata['tags']   if t in interest_map]
        db.session.add(internship)

    db.session.flush()

    # Seed initial demo applications from student to companies
    abc_internship = Internship.query.filter_by(company_id=abc.id).first()
    if abc_internship:
        app1 = Application(
            student_id   = student_profile.id,
            internship_id= abc_internship.id,
            cover_letter = 'Dear ABC Technology hiring team, I am an enthusiastic 3rd-year Software Engineering student at Debre Berhan University. I have hands-on experience in full-stack web development and would love to contribute to your team.',
            status       = 'pending',
        )
        db.session.add(app1)

    xyz_internship = Internship.query.filter_by(company_id=xyz.id).first()
    if xyz_internship:
        app2 = Application(
            student_id   = student_profile.id,
            internship_id= xyz_internship.id,
            cover_letter = 'Hello XYZ Solutions, I am passionate about data analytics and machine learning applications. I have built models using Python, TensorFlow, and Pandas during my coursework at DBU.',
            status       = 'accepted',
        )
        db.session.add(app2)

    db.session.commit()
    print("[+] Database seeded successfully!")
    print("\n[+] Demo credentials for 3 distinct roles:")
    print("   🏛️ University Admin: admin@dbu.edu.et       / admin123  (or admin@internmatch.com)")
    print("   🏢 Company Admin 1:   abc@techcorp.com        / company123 (ABC Technology)")
    print("   🏢 Company Admin 2:   xyz@solutions.com       / company123 (XYZ Solutions)")
    print("   👨‍🎓 Student:           ruhama@student.com      / student123")
