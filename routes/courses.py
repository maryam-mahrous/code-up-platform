from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Course, Lesson, Enrollment, LessonProgress, Category, Certificate, SearchHistory
import secrets
from datetime import datetime

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')


@courses_bp.route('/', methods=['GET'])
def list_courses():
    category_slug = request.args.get('category')
    level = request.args.get('level')
    search = request.args.get('search', '')

    query = Course.query.filter_by(is_published=True)

    if category_slug:
        category = Category.query.filter_by(slug=category_slug).first()
        if category:
            query = query.filter_by(category_id=category.id)
    if level:
        query = query.filter_by(level=level)
    if search:
        query = query.filter(
            (Course.title_en.ilike(f'%{search}%')) | (Course.title_ar.ilike(f'%{search}%'))
        )

    courses = query.order_by(Course.created_at.desc()).all()

    # Log search history
    if search:
        user_id = current_user.id if current_user.is_authenticated else None
        log = SearchHistory(
            user_id=user_id,
            query=search,
            results_count=len(courses)
        )
        db.session.add(log)
        db.session.commit()

    return jsonify([c.to_dict() for c in courses]), 200


@courses_bp.route('/<int:course_id>', methods=['GET'])
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    lessons = course.lessons.order_by(Lesson.order).all()

    is_enrolled = False
    progress = 0
    completed_lessons = []

    if current_user.is_authenticated:
        is_enrolled = current_user.is_enrolled(course_id)
        if is_enrolled:
            progress = current_user.get_course_progress(course_id)
            completed = current_user.lesson_progress.filter_by(course_id=course_id, completed=True).all()
            completed_lessons = [lp.lesson_id for lp in completed]

    data = course.to_dict()
    data['is_enrolled'] = is_enrolled
    data['progress'] = progress
    data['lessons'] = [l.to_dict(is_completed=l.id in completed_lessons) for l in lessons]
    return jsonify(data), 200


@courses_bp.route('/<int:course_id>/enroll', methods=['POST'])
@login_required
def enroll(course_id):
    course = Course.query.get_or_404(course_id)
    if current_user.is_enrolled(course_id):
        return jsonify({'error': 'Already enrolled in this course'}), 409

    enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({
        'message': {'en': f'Successfully enrolled in "{course.title_en}"', 'ar': f'تم التسجيل في "{course.title_ar}" بنجاح'}
    }), 201


@courses_bp.route('/<int:course_id>/lessons/<int:lesson_id>', methods=['GET'])
@login_required
def lesson_view(course_id, lesson_id):
    course = Course.query.get_or_404(course_id)
    lesson = Lesson.query.get_or_404(lesson_id)

    if lesson.course_id != course_id:
        return jsonify({'error': 'Lesson not found in this course'}), 404
    if not current_user.is_enrolled(course_id) and not lesson.is_free_preview:
        return jsonify({'error': 'You must enroll in this course first'}), 403

    lessons = course.lessons.order_by(Lesson.order).all()
    lesson_ids = [l.id for l in lessons]
    current_idx = lesson_ids.index(lesson_id) if lesson_id in lesson_ids else 0

    completed_lessons = []
    if current_user.is_enrolled(course_id):
        completed = current_user.lesson_progress.filter_by(course_id=course_id, completed=True).all()
        completed_lessons = [lp.lesson_id for lp in completed]

    return jsonify({
        'lesson': lesson.to_dict(is_completed=lesson.id in completed_lessons),
        'course': {
            'id': course.id,
            'title': {'en': course.title_en, 'ar': course.title_ar}
        },
        'prev_lesson_id': lesson_ids[current_idx - 1] if current_idx > 0 else None,
        'next_lesson_id': lesson_ids[current_idx + 1] if current_idx < len(lesson_ids) - 1 else None,
        'completed_lessons': completed_lessons
    }), 200


@courses_bp.route('/<int:course_id>/lessons/<int:lesson_id>/complete', methods=['POST'])
@login_required
def complete_lesson(course_id, lesson_id):
    Course.query.get_or_404(course_id)
    Lesson.query.get_or_404(lesson_id)

    if not current_user.is_enrolled(course_id):
        return jsonify({'error': 'You must enroll in this course first'}), 403

    existing = current_user.lesson_progress.filter_by(lesson_id=lesson_id).first()
    if existing:
        existing.completed = True
        existing.completed_at = datetime.utcnow()
    else:
        progress = LessonProgress(
            user_id=current_user.id, course_id=course_id,
            lesson_id=lesson_id, completed=True, completed_at=datetime.utcnow()
        )
        db.session.add(progress)

    db.session.commit()
    course_progress = current_user.get_course_progress(course_id)
    certificate_issued = False

    if course_progress == 100:
        certificate_issued = _issue_certificate(current_user.id, course_id)

    return jsonify({
        'message': {'en': 'Lesson marked as complete', 'ar': 'تم تحديد الدرس كمكتمل'},
        'course_progress': course_progress,
        'certificate_issued': certificate_issued
    }), 200


def _issue_certificate(user_id, course_id):
    existing = Certificate.query.filter_by(user_id=user_id, course_id=course_id).first()
    if existing:
        return False
    enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
    if enrollment:
        enrollment.is_completed = True
        enrollment.completed_at = datetime.utcnow()
    cert = Certificate(user_id=user_id, course_id=course_id,
                       certificate_code=f'CERT-{secrets.token_hex(6).upper()}')
    db.session.add(cert)
    db.session.commit()
    return True


@courses_bp.route('/categories', methods=['GET'])
def categories():
    cats = Category.query.all()
    return jsonify([c.to_dict() for c in cats]), 200
