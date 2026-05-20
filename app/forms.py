from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, RadioField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.models import User


class RegisterForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired(), Length(min=3, max=20)])
    email = EmailField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Password:", validators=[DataRequired(), Length(min=8, max=50)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    gender = RadioField("Gender", choices=[("male", "Male"), ("female", "Female")], validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError(f"Username '{username.data} already exist")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError(f"Email '{email.data} already exist")

        
class LoginForm(FlaskForm):
    email = EmailField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Password:", validators=[DataRequired(), Length(min=8, max=50)])
    submit = SubmitField("Login")


class AnswerForm(FlaskForm):
    answer = StringField("Answer:", validators=[DataRequired()])
    submit = SubmitField("Submit")