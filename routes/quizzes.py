import json
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Quiz, Question, Choice, QuizAttempt, Course

quizzes_bp = Blueprint('quizzes', __name__, url_prefix='/api/quizzes')


@quizzes_bp.route('/course/<int:course_id>', methods=['GET'])
@login_required
def course_quizzes(course_id):
    course = Course.query.get_or_404(course_id)
    if not current_user.is_enrolled(course_id):
        return jsonify({'error': 'You must enroll in this course first'}), 403

    quizzes = course.quizzes.filter_by(is_published=True).all()
    result = []
    for quiz in quizzes:
        last_attempt = QuizAttempt.query.filter_by(
            user_id=current_user.id, quiz_id=quiz.id
        ).order_by(QuizAttempt.completed_at.desc()).first()
        d = quiz.to_dict()
        d['last_attempt'] = {
            'score': last_attempt.score,
            'passed': last_attempt.passed,
            'completed_at': last_attempt.completed_at.isoformat() if last_attempt.completed_at else None
        } if last_attempt else None
        result.append(d)
    return jsonify(result), 200


@quizzes_bp.route('/<int:quiz_id>', methods=['GET'])
@login_required
def get_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if not current_user.is_enrolled(quiz.course_id):
        return jsonify({'error': 'You must enroll in this course first'}), 403

    questions = quiz.questions.order_by(Question.order).all()
    data = quiz.to_dict()
    data['questions'] = [q.to_dict() for q in questions]
    return jsonify(data), 200


@quizzes_bp.route('/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if not current_user.is_enrolled(quiz.course_id):
        return jsonify({'error': 'You must enroll in this course first'}), 403

    data = request.get_json()
    if not data or 'answers' not in data:
        return jsonify({'error': 'Answers required — send {"answers": {"question_id": choice_id}}'}), 400

    answers = data['answers']
    questions = quiz.questions.all()
    total_points = sum(q.points for q in questions)
    earned_points = 0
    result_details = []

    for question in questions:
        choice_id = answers.get(str(question.id))
        is_correct = False
        selected_choice = None
        correct_choice = question.choices.filter_by(is_correct=True).first()

        if choice_id:
            selected_choice = Choice.query.get(int(choice_id))
            if selected_choice and selected_choice.is_correct:
                earned_points += question.points
                is_correct = True

        result_details.append({
            'question_id': question.id,
            'question_text': {'en': question.text_en, 'ar': question.text_ar},
            'is_correct': is_correct,
            'selected_choice_id': selected_choice.id if selected_choice else None,
            'correct_choice_id': correct_choice.id if correct_choice else None,
            'explanation': {'en': question.explanation_en, 'ar': question.explanation_ar}
        })

    score = round((earned_points / total_points) * 100, 1) if total_points > 0 else 0
    passed = score >= quiz.passing_score

    attempt = QuizAttempt(
        user_id=current_user.id, quiz_id=quiz_id,
        score=score, passed=passed,
        answers_json=json.dumps(answers),
        completed_at=datetime.utcnow()
    )
    db.session.add(attempt)
    db.session.commit()

    return jsonify({
        'attempt_id': attempt.id,
        'score': score,
        'passed': passed,
        'passing_score': quiz.passing_score,
        'earned_points': earned_points,
        'total_points': total_points,
        'details': result_details
    }), 200
