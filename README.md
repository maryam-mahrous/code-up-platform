# 🚀 كود أكاديمي — منصة تعليم البرمجة

باك اند كامل لمنصة تعليم البرمجة مبني بـ **Python + Flask + SQLite**

---

## 📁 هيكل المشروع

```
coding_platform/
├── app.py                 # نقطة الدخول الرئيسية
├── config.py              # إعدادات التطبيق
├── models.py              # موديلات قاعدة البيانات
├── forms.py               # فورمات WTForms
├── seed_data.py           # بيانات تجريبية (5 كورسات حقيقية)
├── requirements.txt       # المكتبات المطلوبة
├── routes/
│   ├── auth.py            # تسجيل / دخول / خروج
│   ├── main.py            # الصفحة الرئيسية + Dashboard
│   ├── courses.py         # الكورسات + الدروس + التقدم
│   ├── quizzes.py         # الكويزات + النتائج
│   ├── certificates.py    # الشهادات + التحقق
│   └── profile.py         # البروفايل
└── templates/
    ├── base.html           # القالب الأساسي
    ├── auth/              # صفحات login/register
    ├── main/              # index + dashboard
    ├── courses/           # list + detail + lesson
    ├── quizzes/           # list + take + result
    ├── certificates/      # list + view + verify
    └── profile/           # view + edit
```

---

## ⚡ تشغيل المشروع

```bash
# 1. إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# 2. تثبيت المكتبات
pip install -r requirements.txt

# 3. تشغيل البيانات التجريبية
python seed_data.py

# 4. تشغيل التطبيق
python app.py
```

التطبيق سيعمل على: **http://localhost:5000**

---

## 👤 بيانات الأدمن

- **إيميل:** `admin@platform.com`
- **باسوورد:** `admin123`

---

## 🗄️ موديلات قاعدة البيانات

| الجدول | الوصف |
|--------|-------|
| `users` | المستخدمين (طالب / مدرس / أدمن) |
| `categories` | تصنيفات الكورسات |
| `courses` | الكورسات |
| `lessons` | الدروس داخل كل كورس |
| `enrollments` | تسجيل الطلاب في الكورسات |
| `lesson_progress` | تتبع إكمال الدروس |
| `quizzes` | الاختبارات |
| `questions` | أسئلة الاختبار |
| `choices` | اختيارات كل سؤال |
| `quiz_attempts` | محاولات الطلاب في الاختبارات |
| `certificates` | الشهادات المُصدرة |

---

## 🔗 الـ Routes الرئيسية

### Auth
- `GET/POST /auth/register` — إنشاء حساب
- `GET/POST /auth/login` — تسجيل الدخول
- `GET /auth/logout` — تسجيل الخروج

### Courses
- `GET /courses/` — قائمة الكورسات (مع فلترة وبحث)
- `GET /courses/<id>` — تفاصيل الكورس
- `POST /courses/<id>/enroll` — التسجيل في الكورس
- `GET /courses/<id>/lessons/<id>` — عرض الدرس
- `POST /courses/<id>/lessons/<id>/complete` — تحديد الدرس كمكتمل

### Quizzes
- `GET /quizzes/course/<id>` — اختبارات الكورس
- `GET /quizzes/<id>/take` — بدء الاختبار
- `POST /quizzes/<id>/submit` — تسليم الإجابات
- `GET /quizzes/result/<id>` — نتيجة الاختبار

### Certificates
- `GET /certificates/my` — شهاداتي
- `GET /certificates/<id>` — عرض شهادة
- `GET /certificates/verify/<code>` — التحقق من الشهادة (عام)

### Profile
- `GET /profile/` — عرض البروفايل
- `GET/POST /profile/edit` — تعديل البروفايل

### Dashboard
- `GET /` — الصفحة الرئيسية
- `GET /dashboard` — لوحة الطالب

---

## ✨ المميزات

- ✅ Authentication كامل (Register / Login / Logout)
- ✅ تسجيل الطلاب في الكورسات
- ✅ تتبع تقدم الطالب (نسبة الإكمال)
- ✅ مشغّل فيديو YouTube مدمج
- ✅ نظام كويزات كامل مع تصحيح تلقائي
- ✅ شهادات إتمام تُصدر أوتوماتيكياً
- ✅ رابط تحقق عام من الشهادة
- ✅ واجهة عربية RTL بالكامل
- ✅ CSRF Protection على كل الفورمات
- ✅ Passwords مشفرة (bcrypt)
- ✅ 5 كورسات حقيقية جاهزة

---

## 🔒 الأمان

- كلمات المرور مشفرة بـ `werkzeug.security`
- CSRF Protection بـ `Flask-WTF`
- `@login_required` على كل الـ routes الحساسة
- منع الوصول للدروس بدون تسجيل

---

## 🚀 الخطوات القادمة

- [ ] Admin Panel لإضافة/تعديل الكورسات
- [ ] رفع صور للكورسات
- [ ] نظام تعليقات على الدروس
- [ ] إشعارات
- [ ] نظام نقاط وإنجازات
- [ ] API Endpoints لـ Mobile App
