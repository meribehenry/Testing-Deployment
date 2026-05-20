from flask import Blueprint, render_template, redirect, flash, url_for
from app.models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from app.forms import RegisterForm, LoginForm

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        gender = form.gender.data

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password, email=email, gender=gender)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for("auth.login"))
    
    return render_template("register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if email == user.email and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main.dashboard"))
        
        flash("Invalid Credential")
    
    return render_template("login.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))