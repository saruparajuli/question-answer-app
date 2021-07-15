from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from qna_app.models import User

class registrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3,max=20)])
    password = StringField('Password', validators=[DataRequired(), Length(min=3,max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username Taken')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email Taken')
    


class loginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3,max=20)])
    password = StringField('Password', validators=[DataRequired(), Length(min=3,max=20)])
    submit = SubmitField('Login')

    

class questionForm(FlaskForm):
    question = TextAreaField('Question', validators=[DataRequired()])
    submit = SubmitField('Submit')

class commentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')