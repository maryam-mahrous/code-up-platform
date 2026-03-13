from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from models import Certificate

certs_bp = Blueprint('certificates', __name__, url_prefix='/api/certificates')


@certs_bp.route('/my', methods=['GET'])
@login_required
def my_certificates():
    certs = current_user.certificates.all()
    return jsonify([{
        'id': c.id,
        'certificate_code': c.certificate_code,
        'issued_at': c.issued_at.isoformat(),
        'final_score': c.final_score,
        'course': {'id': c.course.id, 'title': c.course.title, 'thumbnail': c.course.thumbnail}
    } for c in certs]), 200


@certs_bp.route('/verify/<string:code>', methods=['GET'])
def verify(code):
    cert = Certificate.query.filter_by(certificate_code=code).first()
    if not cert:
        return jsonify({'valid': False, 'error': 'الشهادة غير موجودة'}), 404
    return jsonify({
        'valid': True,
        'certificate_code': cert.certificate_code,
        'issued_at': cert.issued_at.isoformat(),
        'student_name': cert.student.username,
        'course_title': cert.course.title,
        'final_score': cert.final_score
    }), 200
