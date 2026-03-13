from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='student')
    avatar = db.Column(db.String(200), default='')
    bio = db.Column(db.Text, default='')
    bio_ar = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    enrollments = db.relationship('Enrollment', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    lesson_progress = db.relationship('LessonProgress', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    quiz_attempts = db.relationship('QuizAttempt', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    certificates = db.relationship('Certificate', backref='student', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_course_progress(self, course_id):
        enrollment = self.enrollments.filter_by(course_id=course_id).first()
        if not enrollment:
            return 0
        course = Course.query.get(course_id)
        if not course:
            return 0
        total_lessons = course.lessons.count()
        if total_lessons == 0:
            return 0
        completed = self.lesson_progress.filter_by(course_id=course_id, completed=True).count()
        return round((completed / total_lessons) * 100)

    def is_enrolled(self, course_id):
        return self.enrollments.filter_by(course_id=course_id).first() is not None

    def __repr__(self):
        return f'<User {self.username}>'


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    # English
    name_en = db.Column(db.String(100), nullable=False)
    description_en = db.Column(db.Text, default='')
    # Arabic
    name_ar = db.Column(db.String(100), nullable=False)
    description_ar = db.Column(db.Text, default='')

    slug = db.Column(db.String(100), unique=True, nullable=False)
    icon = db.Column(db.String(50), default='📚')

    courses = db.relationship('Course', backref='category', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'icon': self.icon,
            'name': {'en': self.name_en, 'ar': self.name_ar},
            'description': {'en': self.description_en, 'ar': self.description_ar},
            'courses_count': self.courses.count()
        }

    def __repr__(self):
        return f'<Category {self.name_en}>'


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    # English
    title_en = db.Column(db.String(200), nullable=False)
    description_en = db.Column(db.Text, nullable=False)
    short_description_en = db.Column(db.String(300), default='')
    # Arabic
    title_ar = db.Column(db.String(200), nullable=False)
    description_ar = db.Column(db.Text, nullable=False)
    short_description_ar = db.Column(db.String(300), default='')

    thumbnail = db.Column(db.String(300), default='')
    level = db.Column(db.String(20), default='beginner')
    duration_hours = db.Column(db.Float, default=0)
    is_published = db.Column(db.Boolean, default=True)
    is_free = db.Column(db.Boolean, default=True)
    price = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    instructor = db.relationship('User', foreign_keys=[instructor_id])
    lessons = db.relationship('Lesson', backref='course', lazy='dynamic',
                               order_by='Lesson.order', cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', backref='course', lazy='dynamic', cascade='all, delete-orphan')
    quizzes = db.relationship('Quiz', backref='course', lazy='dynamic', cascade='all, delete-orphan')

    def enrolled_count(self):
        return self.enrollments.count()

    def to_dict(self, completed_lessons=None):
        return {
            'id': self.id,
            'title': {'en': self.title_en, 'ar': self.title_ar},
            'description': {'en': self.description_en, 'ar': self.description_ar},
            'short_description': {'en': self.short_description_en, 'ar': self.short_description_ar},
            'thumbnail': self.thumbnail,
            'level': self.level,
            'level_label': {
                'en': {'beginner': 'Beginner', 'intermediate': 'Intermediate', 'advanced': 'Advanced'}.get(self.level, self.level),
                'ar': {'beginner': 'مبتدئ', 'intermediate': 'متوسط', 'advanced': 'متقدم'}.get(self.level, self.level)
            },
            'is_free': self.is_free,
            'price': self.price,
            'duration_hours': self.duration_hours,
            'lessons_count': self.lessons.count(),
            'enrolled_count': self.enrolled_count(),
            'quizzes_count': self.quizzes.count(),
            'category': self.category.to_dict() if self.category else None,
            'instructor': {'id': self.instructor.id, 'username': self.instructor.username} if self.instructor else None,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<Course {self.title_en}>'


class Lesson(db.Model):
    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)
    # English
    title_en = db.Column(db.String(200), nullable=False)
    description_en = db.Column(db.Text, default='')
    content_en = db.Column(db.Text, default='')
    # Arabic
    title_ar = db.Column(db.String(200), nullable=False)
    description_ar = db.Column(db.Text, default='')
    content_ar = db.Column(db.Text, default='')

    video_url = db.Column(db.String(500), default='')
    duration_minutes = db.Column(db.Integer, default=0)
    order = db.Column(db.Integer, default=0)
    is_free_preview = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    progress_records = db.relationship('LessonProgress', backref='lesson', lazy='dynamic', cascade='all, delete-orphan')

    def get_youtube_embed(self):
        url = self.video_url
        if 'youtube.com/watch?v=' in url:
            video_id = url.split('v=')[1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        return url

    def to_dict(self, is_completed=False):
        return {
            'id': self.id,
            'title': {'en': self.title_en, 'ar': self.title_ar},
            'description': {'en': self.description_en, 'ar': self.description_ar},
            'content': {'en': self.content_en, 'ar': self.content_ar},
            'video_url': self.video_url,
            'video_embed': self.get_youtube_embed(),
            'duration_minutes': self.duration_minutes,
            'order': self.order,
            'is_free_preview': self.is_free_preview,
            'is_completed': is_completed
        }

    def __repr__(self):
        return f'<Lesson {self.title_en}>'


class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_completed = db.Column(db.Boolean, default=False)

    __table_args__ = (db.UniqueConstraint('user_id', 'course_id', name='unique_enrollment'),)


class LessonProgress(db.Model):
    __tablename__ = 'lesson_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    __table_args__ = (db.UniqueConstraint('user_id', 'lesson_id', name='unique_lesson_progress'),)


class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(200), nullable=False)
    title_ar = db.Column(db.String(200), nullable=False)
    description_en = db.Column(db.Text, default='')
    description_ar = db.Column(db.Text, default='')
    passing_score = db.Column(db.Integer, default=70)
    time_limit_minutes = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy='dynamic',
                                 order_by='Question.order', cascade='all, delete-orphan')
    attempts = db.relationship('QuizAttempt', backref='quiz', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'title': {'en': self.title_en, 'ar': self.title_ar},
            'description': {'en': self.description_en, 'ar': self.description_ar},
            'passing_score': self.passing_score,
            'time_limit_minutes': self.time_limit_minutes,
            'questions_count': self.questions.count(),
            'course_id': self.course_id
        }


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    text_en = db.Column(db.Text, nullable=False)
    text_ar = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), default='mcq')
    order = db.Column(db.Integer, default=0)
    points = db.Column(db.Integer, default=1)
    explanation_en = db.Column(db.Text, default='')
    explanation_ar = db.Column(db.Text, default='')

    choices = db.relationship('Choice', backref='question', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self, include_correct=False):
        return {
            'id': self.id,
            'text': {'en': self.text_en, 'ar': self.text_ar},
            'points': self.points,
            'explanation': {'en': self.explanation_en, 'ar': self.explanation_ar},
            'choices': [c.to_dict(include_correct) for c in self.choices.all()]
        }


class Choice(db.Model):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    text_en = db.Column(db.String(500), nullable=False)
    text_ar = db.Column(db.String(500), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

    def to_dict(self, include_correct=False):
        d = {
            'id': self.id,
            'text': {'en': self.text_en, 'ar': self.text_ar}
        }
        if include_correct:
            d['is_correct'] = self.is_correct
        return d


class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    score = db.Column(db.Float, default=0)
    passed = db.Column(db.Boolean, default=False)
    answers_json = db.Column(db.Text, default='{}')
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)


class Certificate(db.Model):
    __tablename__ = 'certificates'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    certificate_code = db.Column(db.String(50), unique=True, nullable=False)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)
    final_score = db.Column(db.Float, default=100.0)

    course = db.relationship('Course')

    __table_args__ = (db.UniqueConstraint('user_id', 'course_id', name='unique_certificate'),)

    def to_dict(self):
        return {
            'id': self.id,
            'certificate_code': self.certificate_code,
            'issued_at': self.issued_at.isoformat(),
            'final_score': self.final_score,
            'course': {
                'id': self.course.id,
                'title': {'en': self.course.title_en, 'ar': self.course.title_ar},
                'thumbnail': self.course.thumbnail
            }
        }
