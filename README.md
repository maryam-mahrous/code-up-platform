# Code Academy — Programming Learning Platform

A complete backend for a programming learning platform built with **Python + Flask + SQLite**

---

## Getting Started

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
python seed_data.py
python app.py
```

App runs at: **http://localhost:5000**

---

## Admin Credentials

- **Email:** `admin@platform.com`
- **Password:** `admin123`

---

## Tech Stack

- Python + Flask
- SQLite + SQLAlchemy
- Flask-Login (Session-based Auth)
- CORS enabled

---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Login |
| POST | `/api/auth/logout` | Logout |
| GET | `/api/auth/me` | Current user data |

### Courses
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/courses/` | All courses |
| GET | `/api/courses/<id>` | Course details + lessons |
| POST | `/api/courses/<id>/enroll` | Enroll in course |
| POST | `/api/courses/<id>/lessons/<id>/complete` | Mark lesson complete |
| GET | `/api/courses/categories` | All categories |

### Quizzes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/quizzes/<id>` | Quiz details + questions |
| POST | `/api/quizzes/<id>/submit` | Submit answers |

### Certificates
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/certificates/my` | My certificates |
| GET | `/api/certificates/verify/<code>` | Verify certificate |

### Profile
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/profile/` | View profile |
| PUT | `/api/profile/` | Edit profile |

### Analytics (Admin only)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analytics/overview` | Platform statistics |
| GET | `/api/analytics/hardest-courses` | Courses with highest fail rate |
| GET | `/api/analytics/completion-time` | Average course completion time |

---

## Features

- Full Authentication (Register / Login / Logout)
- Student enrollment & lesson progress tracking
- Automatic certificates on course completion
- Quizzes with automatic grading
- Bilingual support (Arabic & English)
- Admin analytics dashboard

---

## Authentication

Uses **Session-based auth**. Frontend must send `credentials: 'include'` in every request.

```javascript
fetch('http://localhost:5000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include',
  body: JSON.stringify({ email: '', password: '' })
});
```
