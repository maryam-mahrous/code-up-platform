from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'البيانات مطلوبة'}), 400

    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not username or not email or not password:
        return jsonify({'error': 'كل الحقول مطلوبة'}), 400
    if len(username) < 3:
        return jsonify({'error': 'الاسم على الأقل 3 أحرف'}), 400
    if len(password) < 6:
        return jsonify({'error': 'كلمة المرور على الأقل 6 أحرف'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'البريد الإلكتروني مستخدم بالفعل'}), 409
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'اسم المستخدم مستخدم بالفعل'}), 409

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    return jsonify({
        'message': 'تم إنشاء الحساب بنجاح',
        'user': {'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role}
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'البيانات مطلوبة'}), 400

    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    remember = data.get('remember', False)

    if not email or not password:
        return jsonify({'error': 'الإيميل وكلمة المرور مطلوبان'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'البريد الإلكتروني أو كلمة المرور غير صحيحة'}), 401

    login_user(user, remember=remember)
    return jsonify({
        'message': 'تم تسجيل الدخول بنجاح',
        'user': {
            'id': user.id, 'username': user.username,
            'email': user.email, 'role': user.role,
            'bio': user.bio, 'created_at': user.created_at.isoformat()
        }
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'تم تسجيل الخروج بنجاح'}), 200


@auth_bp.route('/me', methods=['GET'])
@login_required
def me():
    return jsonify({
        'id': current_user.id, 'username': current_user.username,
        'email': current_user.email, 'role': current_user.role,
        'bio': current_user.bio, 'created_at': current_user.created_at.isoformat()
    }), 200
