from flask import Blueprint, render_template, redirect, request, url_for, session
from flask_login import login_required, current_user
from app.models import QuizResult, db
from app.forms import AnswerForm
from .classes import Quiz, questions

quiz_system = Blueprint("quiz_system", __name__)

@quiz_system.route("/start")
@login_required
def start():

    session["current_index"] = 0
    session["score"] = 0
    session["user_answers"] = {}
    return redirect(url_for("quiz_system.quiz"))

@quiz_system.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
    quiz = Quiz(questions)
    quiz.current_index = session["current_index"]
    quiz.score = session["score"]
    quiz.user_answers = session["user_answers"]

    form = AnswerForm()
    
    if form.validate_on_submit():
        user_answer = form.answer.data
        quiz.check_answer(user_answer)

        session["current_index"] = quiz.current_index  
        session["score"] = quiz.score
        session["user_answers"] = quiz.user_answers

        if quiz.finished():
            result = QuizResult(score=quiz.score, user_id=current_user.get_id())
            db.session.add(result)
            db.session.commit()
            return redirect(url_for("quiz_system.result"))
        
        return redirect(url_for("quiz_system.quiz"))
    
    question = quiz.get_question()
    return render_template("quiz.html", question=question, number=(session["current_index"]+1), form=form)

    


@quiz_system.route("/result", methods=["GET", "POST"])
@login_required
def result():
    score = session["score"] 
    return render_template(
        "result.html", 
        score=score, 
        results=current_user.results, 
        quiz_overview=session["user_answers"], 
        questions=questions
        )