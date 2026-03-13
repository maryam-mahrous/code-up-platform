# API Documentation — Code Academy

Base URL: `http://localhost:5000`

---

## Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Login |
| POST | `/api/auth/logout` | Logout |
| GET | `/api/auth/me` | Current user data |

### Register
```json
{
  "username": "Ahmed",
  "email": "ahmed@mail.com",
  "password": "123456"
}
```

### Login
```json
{
  "email": "ahmed@mail.com",
  "password": "123456"
}
```

---

## Courses

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/courses/` | All courses |
| GET | `/api/courses/?category=python` | Filter by category |
| GET | `/api/courses/?level=beginner` | Filter by level |
| GET | `/api/courses/?search=python` | Search |
| GET | `/api/courses/<id>` | Course details + lessons |
| POST | `/api/courses/<id>/enroll` | Enroll in course |
| GET | `/api/courses/<id>/lessons/<id>` | View lesson |
| POST | `/api/courses/<id>/lessons/<id>/complete` | Mark lesson complete |
| GET | `/api/courses/categories` | All categories |

---

## Quizzes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/quizzes/course/<id>` | Course quizzes |
| GET | `/api/quizzes/<id>` | Quiz details + questions |
| POST | `/api/quizzes/<id>/submit` | Submit answers |

### Submit Quiz
```json
{
  "answers": {
    "question_id": "choice_id"
  }
}
```

---

## Certificates

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/certificates/my` | My certificates |
| GET | `/api/certificates/verify/<code>` | Verify certificate (public) |

---

## Profile

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/profile/` | View profile |
| PUT | `/api/profile/` | Edit profile |

### Edit Profile
```json
{
  "username": "NewName",
  "bio": "Web Developer"
}
```

---

## Analytics (Admin only)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analytics/overview` | Platform statistics |
| GET | `/api/analytics/hardest-courses` | Courses with highest fail rate |
| GET | `/api/analytics/completion-time` | Average completion time |

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request |
| 401 | Not logged in |
| 403 | Forbidden |
| 404 | Not found |
| 409 | Already exists |

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
