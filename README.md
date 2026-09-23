# Debre Berhan University — Online Student Internship Matching Platform 🎓

A full-stack web application designed for Debre Berhan University students and partner employers. The platform coordinates the internship lifecycle with 3 distinctly differentiated user roles, separate dashboards, unique credentials, and dedicated workflows.

---

## 👥 Three Differentiated User Roles

### 1. 🏛️ University Administrator (Debre Berhan University)
- **Role & Access**: Platform supervisor managing the university's corporate partnership network.
- **Dedicated Dashboard**: Platform metrics, student registries, and partner company directory.
- **Key Capabilities**:
  - **Add Partner Companies**: Creates company accounts with company work email and password.
  - **Remove / Deactivate Companies**: Permanently remove or temporarily deactivate company access.
  - **Reset Company Password**: Reset credentials for partner companies when requested.
  - **Manage Students**: View registered student accounts, departments, and account statuses.
  - **Listing Oversight**: Global directory of all internship listings across companies.
- **Login Credentials**: `admin@dbu.edu.et` (or `admin@internmatch.com`) / `admin123`

---

### 2. 🏢 Company Administrator (Partner Employer)
- **Role & Access**: Individual employer representative authorized by the university.
- **Dedicated Dashboard**: Applicant decision center, listing performance, and company settings.
- **Key Capabilities**:
  - **Approve or Decline Applications**: Review student candidate profiles, academic field, year, GPA, skills, and CVs, and directly **Approve (Accept)** or **Decline (Reject)** applications with one click.
  - **Interview Management**: Move candidates to the interview stage or email them directly.
  - **Post & Edit Internships**: Create listings with required skills, openings, deadlines, work type (Remote/Hybrid/On-site), and Ethiopian locations.
  - **Company Settings**: Update profile overview and independently manage company password.
- **Login Credentials**:
  - `abc@techcorp.com` / `company123` (ABC Technology)
  - `xyz@solutions.com` / `company123` (XYZ Solutions)
  - `nova@digital.com` / `company123` (Nova Digital Agency)

---

### 3. 👨‍🎓 Student
- **Role & Access**: Debre Berhan University students seeking internship opportunities.
- **Dedicated Dashboard**: Active applications tracker, saved bookmarks, and profile status.
- **Key Capabilities**:
  - **Self-Registration**: Register with student ID, department, university, and year of study.
  - **Profile & Skills**: Select technical skills, career interests, and upload CV (`.pdf`/`.docx`) and essays.
  - **Browse & Search**: Filter internships by keyword, field, work type, and Ethiopian cities.
  - **Application Tracking**: Real-time status updates as Company Admins review, approve, or decline applications.
- **Login Credentials**: `ruhama@student.com` / `student123` (or self-register a new account)

---

## 🚀 Quick Start & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Ruhama27/internship-portal.git
cd internship-portal
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000/`.

---

## 🔑 Demo Credentials Summary

| Role | Work / Student Email | Password | Primary Dashboard Actions |
|---|---|---|---|
| **🏛️ University Admin** | `admin@dbu.edu.et` | `admin123` | Add & Remove Companies, Student Directory, Platform Oversight |
| **🏢 Company Admin (ABC)** | `abc@techcorp.com` | `company123` | Approve / Decline Student Applications, Post Internships |
| **🏢 Company Admin (XYZ)** | `xyz@solutions.com` | `company123` | Approve / Decline Student Applications, Post Internships |
| **👨‍🎓 Student** | `ruhama@student.com` | `student123` | Browse Internships, Upload CV, Apply & Track Status |

---

## 🛠️ Technology Stack

- **Backend**: Python 3.x, Flask, Flask-SQLAlchemy, Flask-Login
- **Database**: SQLite (SQLAlchemy ORM)
- **Frontend**: Responsive HTML5, Vanilla CSS3, JavaScript (Debre Berhan University Portal styling)
