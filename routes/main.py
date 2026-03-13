from flask import Blueprint, jsonify
from models import Course, Category, Enrollment

main_bp = Blueprint('main', __name__, url_prefix='/api')


@main_bp.route('/', methods=['GET'])
def index():
    featured_courses = Course.query.filter_by(is_published=True).limit(6).all()
    categories = Category.query.all()
    return jsonify({
        'total_courses': Course.query.filter_by(is_published=True).count(),
        'total_students': Enrollment.query.distinct(Enrollment.user_id).count(),
        'categories': [{'id': c.id, 'name': c.name, 'slug': c.slug, 'icon': c.icon} for c in categories],
        'featured_courses': [{
            'id': c.id, 'title': c.title,
            'short_description': c.short_description,
            'thumbnail': c.thumbnail, 'level': c.level,
            'is_free': c.is_free, 'lessons_count': c.lessons.count(),
            'enrolled_count': c.enrolled_count()
        } for c in featured_courses]
    }), 200
