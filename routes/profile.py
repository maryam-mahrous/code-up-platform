from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, User

profile_bp = Blueprint('profile', __name__, url_prefix='/api/profile')


@profile_bp.route('/', methods=['GET'])
@login_required
def view_profile():
    enrollments = current_user.enrollments.all()
    courses_data = [{
        'course_id': e.course_id,
        'course_title': e.course.title,
        'is_completed': e.is_completed,
        'enrolled_at': e.enrolled_at.isoformat(),
        'progress': current_user.get_course_progress(e.course_id)
    } for e in enrollments]

    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'bio': current_user.bio,
        'role': current_user.role,
        'created_at': current_user.created_at.isoformat(),
        'enrollments': courses_data,
        'certificates_count': current_user.certificates.count()
    }), 200


@profile_bp.route('/', methods=['PUT'])
@login_required
def edit_profile():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'البيانات مطلوبة'}), 400

    username = data.get('username', '').strip()
    bio = data.get('bio', '').strip()

    if username and len(username) < 3:
        return jsonify({'error': 'الاسم على الأقل 3 أحرف'}), 400

    if username and username != current_user.username:
        existing = User.query.filter_by(username=username).first()
        if existing:
            return jsonify({'error': 'اسم المستخدم مستخدم بالفعل'}), 409
        current_user.username = username

    if bio is not None:
        current_user.bio = bio

    db.session.commit()
    return jsonify({
        'message': 'تم تحديث البروفايل بنجاح',
        'user': {
            'id': current_user.id, 'username': current_user.username,
            'email': current_user.email, 'bio': current_user.bio
        }
    }), 200
