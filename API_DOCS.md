# 📡 API Documentation — كود أكاديمي

Base URL: `http://localhost:5000`

---

## 🔐 Auth

| Method | Endpoint | الوصف |
|--------|----------|-------|
| POST | `/api/auth/register` | إنشاء حساب جديد |
| POST | `/api/auth/login` | تسجيل الدخول |
| POST | `/api/auth/logout` | تسجيل الخروج |
| GET | `/api/auth/me` | بيانات المستخدم الحالي |

### POST /api/auth/register
```json
{
  "username": "Ahmed",
  "email": "ahmed@mail.com",
  "password": "123456"
}
```

### POST /api/auth/login
```json
{
  "email": "ahmed@mail.com",
  "password": "123456",
  "remember": true
}
```

---

## 📚 Courses

| Method | Endpoint | الوصف |
|--------|----------|-------|
| GET | `/api/courses/` | كل الكورسات |
| GET | `/api/courses/?category=python` | فلترة بالتصنيف |
| GET | `/api/courses/?level=beginner` | فلترة بالمستوى |
| GET | `/api/courses/?search=python` | بحث |
| GET | `/api/courses/<id>` | تفاصيل كورس |
| POST | `/api/courses/<id>/enroll` | التسجيل في كورس |
| GET | `/api/courses/<id>/lessons/<id>` | عرض درس |
| POST | `/api/courses/<id>/lessons/<id>/complete` | تحديد درس كمكتمل |
| GET | `/api/courses/categories` | كل التصنيفات |

---

## 🧩 Quizzes

| Method | Endpoint | الوصف |
|--------|----------|-------|
| GET | `/api/quizzes/course/<id>` | اختبارات الكورس |
| GET | `/api/quizzes/<id>` | تفاصيل اختبار مع الأسئلة |
| POST | `/api/quizzes/<id>/submit` | تسليم إجابات |

### POST /api/quizzes/<id>/submit
```json
{
  "answers": {
    "1": 3,
    "2": 7,
    "3": 12
  }
}
```
(question_id: choice_id)

---

## 🏆 Certificates

| Method | Endpoint | الوصف |
|--------|----------|-------|
| GET | `/api/certificates/my` | شهاداتي |
| GET | `/api/certificates/verify/<code>` | التحقق من شهادة (عام) |

---

## 👤 Profile

| Method | Endpoint | الوصف |
|--------|----------|-------|
| GET | `/api/profile/` | عرض البروفايل |
| PUT | `/api/profile/` | تعديل البروفايل |

### PUT /api/profile/
```json
{
  "username": "NewName",
  "bio": "مطور ويب"
}
```

---

## 🏠 General

| Method | Endpoint | الوصف |
|--------|----------|-------|
| GET | `/api/` | الصفحة الرئيسية (كورسات مميزة + إحصائيات) |
| GET | `/api/health` | التحقق من عمل الـ API |

---

## ⚠️ HTTP Status Codes

| Code | المعنى |
|------|--------|
| 200 | نجاح |
| 201 | تم الإنشاء |
| 400 | بيانات غلط |
| 401 | مش مسجّل دخول |
| 403 | مش مصرح ليك |
| 404 | مش موجود |
| 409 | موجود بالفعل |

---

## 🔑 Authentication

الـ API بتستخدم **Session-based auth** (Cookies).
لما تعمل login، الـ session cookie بتتحفظ أوتوماتيكياً.
الفرونت لازم يبعت `credentials: 'include'` في كل request.

### مثال في JavaScript:
```javascript
// Login
const res = await fetch('http://localhost:5000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include',
  body: JSON.stringify({ email: 'test@mail.com', password: '123456' })
});
const data = await res.json();

// Get courses
const courses = await fetch('http://localhost:5000/api/courses/', {
  credentials: 'include'
});
```
