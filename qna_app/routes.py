from qna_app.models import User, Question, Comment
from qna_app.forms import registrationForm, loginForm, questionForm, commentForm
from qna_app import app, db, bcrypt
from flask import render_template, url_for, redirect
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = registrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])

def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/question', methods=['GET', 'POST'])
def question():
    form = questionForm()
    if form.validate_on_submit():
        q = Question(content=form.question.data, user_id=current_user.id)
        db.session.add(q)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('question.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def home():
    questions = Question.query.all()
    users = User.query.all()
    return render_template('home.html', questions=questions, users=users)

@app.route('/post/<id>/comment', methods=['GET', 'POST'])
def comment(id):
    form = commentForm()
    if form.validate_on_submit():
        c = Comment(content=form.comment.data, question_id=id,user_id=current_user.id)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('comment.html', form=form)

@app.route('/logout', methods=['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))
