"""
departments_data.py
Defines Debre Berhan University (DBU) departments and their corresponding
specialization fields for student internships.
"""

DBU_DEPARTMENTS = {
    'Software Engineering': [
        'Full Stack Development',
        'Software Architecture & Design',
        'Web Application Development',
        'Mobile Software Engineering',
        'Quality Assurance & Testing',
        'DevOps & Cloud Engineering',
        'Database Systems',
        'API & Backend Engineering',
        'AI Application Engineering',
    ],
    'Computer Science': [
        'Software Development',
        'Web Development',
        'Mobile App Development',
        'Artificial Intelligence & Machine Learning',
        'Data Science & Analytics',
        'Cybersecurity',
        'Database Administration',
        'Cloud Computing & DevOps',
        'Network & Systems Administration',
        'UI/UX Design',
    ],
    'Information Technology': [
        'Network Administration & Security',
        'System & Server Administration',
        'IT Support & Infrastructure',
        'Database Management',
        'Cybersecurity Operations',
        'Web Technologies',
        'Enterprise Resource Planning (ERP)',
        'Cloud Infrastructure',
    ],
    'Information Systems': [
        'Business Analysis & Systems Design',
        'Enterprise Information Systems',
        'Database & Data Warehousing',
        'IT Project Management',
        'E-Commerce & Digital Systems',
        'Information Security Management',
    ],
    'Electrical & Computer Engineering': [
        'Embedded Systems & IoT',
        'Telecommunications & Network Engineering',
        'Hardware Design & Digital Systems',
        'Control Systems & Automation',
        'Power Systems & Renewable Energy',
        'Signal Processing',
        'Robotics & Industrial Automation',
    ],
    'Mechanical Engineering': [
        'Computer-Aided Design (CAD/CAM)',
        'Manufacturing & Production Systems',
        'Automotive & Vehicle Engineering',
        'Thermal & Fluid Systems',
        'Industrial Maintenance & Safety',
        'HVAC & Energy Systems',
    ],
    'Civil Engineering': [
        'Structural Design & Analysis',
        'Construction Management',
        'Geotechnical Engineering & Surveying',
        'Highway & Transportation Engineering',
        'Water Resources & Hydraulic Engineering',
        'Urban Planning & GIS',
    ],
    'Business & Economics': [
        'Financial Accounting & Auditing',
        'Banking Operations & Analysis',
        'Marketing & Digital Sales',
        'Human Resource Management',
        'Supply Chain & Procurement',
        'Business Development & Consulting',
    ],
}


def get_departments():
    """Return sorted list of all university departments."""
    return list(DBU_DEPARTMENTS.keys())


def get_fields_for_department(dept_name):
    """
    Return list of fields for a given department name.
    Matches case-insensitively and returns fallback if not exact match.
    """
    if not dept_name:
        return []
    dept_name_clean = dept_name.strip().lower()
    for d, fields in DBU_DEPARTMENTS.items():
        if d.lower() == dept_name_clean or dept_name_clean in d.lower() or d.lower() in dept_name_clean:
            return fields
    # Return general tech fields as default fallback
    return DBU_DEPARTMENTS['Software Engineering']
