from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, TextAreaField, SelectField,
                     BooleanField, IntegerField, FloatField, SubmitField, HiddenField)
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange, URL


class RegisterForm(FlaskForm):
    username = StringField('اسم المستخدم', validators=[
        DataRequired(message='الاسم مطلوب'),
        Length(min=3, max=80, message='الاسم بين 3 و 80 حرف')
    ])
    email = StringField('البريد الإلكتروني', validators=[
        DataRequired(message='الإيميل مطلوب'),
        Email(message='إيميل غير صحيح')
    ])
    password = PasswordField('كلمة المرور', validators=[
        DataRequired(message='كلمة المرور مطلوبة'),
        Length(min=6, message='كلمة المرور على الأقل 6 أحرف')
    ])
    confirm_password = PasswordField('تأكيد كلمة المرور', validators=[
        DataRequired(message='تأكيد كلمة المرور مطلوب'),
        EqualTo('password', message='كلمتا المرور غير متطابقتين')
    ])
    submit = SubmitField('إنشاء حساب')


class LoginForm(FlaskForm):
    email = StringField('البريد الإلكتروني', validators=[
        DataRequired(message='الإيميل مطلوب'),
        Email(message='إيميل غير صحيح')
    ])
    password = PasswordField('كلمة المرور', validators=[
        DataRequired(message='كلمة المرور مطلوبة')
    ])
    remember = BooleanField('تذكرني')
    submit = SubmitField('تسجيل الدخول')


class ProfileForm(FlaskForm):
    username = StringField('اسم المستخدم', validators=[
        DataRequired(), Length(min=3, max=80)
    ])
    bio = TextAreaField('نبذة عنك', validators=[Optional(), Length(max=500)])
    submit = SubmitField('حفظ التغييرات')


class CourseForm(FlaskForm):
    title = StringField('عنوان الكورس', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('وصف الكورس', validators=[DataRequired()])
    short_description = StringField('وصف مختصر', validators=[Optional(), Length(max=300)])
    thumbnail = StringField('رابط الصورة', validators=[Optional()])
    level = SelectField('المستوى', choices=[
        ('beginner', 'مبتدئ'),
        ('intermediate', 'متوسط'),
        ('advanced', 'متقدم')
    ])
    category_id = SelectField('التصنيف', coerce=int, validators=[Optional()])
    duration_hours = FloatField('المدة (ساعات)', validators=[Optional(), NumberRange(min=0)])
    is_free = BooleanField('مجاني')
    price = FloatField('السعر', validators=[Optional(), NumberRange(min=0)], default=0)
    is_published = BooleanField('منشور', default=True)
    submit = SubmitField('حفظ الكورس')


class LessonForm(FlaskForm):
    title = StringField('عنوان الدرس', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('وصف الدرس', validators=[Optional()])
    content = TextAreaField('محتوى الدرس', validators=[Optional()])
    video_url = StringField('رابط الفيديو (YouTube)', validators=[Optional()])
    duration_minutes = IntegerField('المدة (دقائق)', validators=[Optional(), NumberRange(min=0)], default=0)
    order = IntegerField('الترتيب', validators=[Optional(), NumberRange(min=0)], default=0)
    is_free_preview = BooleanField('معاينة مجانية')
    submit = SubmitField('حفظ الدرس')


class QuizForm(FlaskForm):
    title = StringField('عنوان الاختبار', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('وصف الاختبار', validators=[Optional()])
    passing_score = IntegerField('درجة النجاح (%)', validators=[
        DataRequired(), NumberRange(min=1, max=100)
    ], default=70)
    time_limit_minutes = IntegerField('وقت الاختبار (دقائق - 0 = بلا حد)', validators=[
        Optional(), NumberRange(min=0)
    ], default=0)
    is_published = BooleanField('منشور', default=True)
    submit = SubmitField('حفظ الاختبار')


class QuizAnswerForm(FlaskForm):
    """Dynamic form for quiz submission - choices handled in route"""
    submit = SubmitField('تسليم الإجابات')
