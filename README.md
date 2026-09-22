# Debre Berhan University — Online Student Internship Matching Platform 🎓

A full-stack web application designed for students and employers. The platform helps students discover suitable company internships through AI-assisted skill matching, complete with visual match breakdown progress bars, CV/Essay upload tools, application tracking, and an employer portal for internship posting and applicant management.

---

## ✨ Features

- 🎓 **Student Self-Service Portal**:
  - Profile setup with university details, field of study, expected graduation year, and GPA.
  - Interactive skill selector (Programming, Web, Database, DevOps, Data Science, etc.) and career interest tags.
  - CV (`.pdf`/`.docx`) and Application Essay upload options.
  - Profile completion strength meter.

- 🤖 **AI Matching Engine**:
  - Multi-weighted scoring model: **40% Skill Overlap** + **30% Academic Field Alignment** + **20% Career Interests** + **10% Seniority Bonus**.
  - **"Why Am I Matched?" Breakdown**: Visual score bars for Education, Skills, Interests, and Seniority with dynamic match explanations.

- 🏢 **Employer / Company Portal**:
  - Company registration and profile management.
  - Internship listing creation (required skills, preferred skills, location, work type: `Remote`/`Hybrid`/`On-site`, openings, deadlines).
  - Applicant pipeline management: View student profiles, match %, CV/essay files, cover notes, update status (`Pending`, `Interview`, `Accepted`, `Rejected`), and send direct application emails.

- 🔍 **Search, Filter & Bookmarks**:
  - Multi-criteria filtering by keyword, field, location, work type, and required skills.
  - Save/bookmark internships to a dedicated collection.

- 📊 **Admin Dashboard**:
  - Platform-wide statistics, user activation/deactivation management, and listing oversight.

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

## 🔑 Demo Credentials

| Role | Email | Password | Details |
|---|---|---|---|
| **Student** | `ruhama@student.com` | `student123` | Debre Berhan University 3rd Year Software Engineering Student |
| **Company A** | `abc@techcorp.com` | `company123` | ABC Technology |
| **Company B** | `xyz@solutions.com` | `company123` | XYZ Solutions |
| **Admin** | `admin@internmatch.com` | `admin123` | System Administrator |

---

## 🛠️ Built With

- **Backend**: Python 3.x, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF
- **Database**: SQLite (SQLAlchemy ORM)
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (Debre Berhan University Portal theme)
