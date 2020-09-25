from app import app, db, lm
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from datetime import datetime

from app.models.tables import User, Post
from app.models.forms import LoginForm, RegisterForm, PostForm

@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()




@app.route("/index/")
@app.route("/")
def index():
    posts = Post.query.filter_by(id=current_user.get_id())
    return render_template('index.html',posts=posts)


@app.route("/login/", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash("Logged in.")
            return redirect(url_for("index"))
        else:
            flash("Invalid login.")
    else:
        print(form.errors)
    return render_template('login.html', form=form)


@app.route('/logout/')
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))


@app.route('/register/', methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            NewUserData = User(form.username.data,form.password.data,form.name.data,form.email.data)
            print(NewUserData)
            db.session.add(NewUserData)
            db.session.commit()
            return redirect(url_for("login"))
        except:
            return redirect(url_for("register"))
    else:
        print(form.errors)
    return render_template('register.html', form=form)


@app.route('/posts')
@app.route('/post/', methods=['GET','POST'])
def post():
    form = PostForm()
    if request.method == 'GET':
        if current_user.is_authenticated == True:
            return render_template('post.html', form=form)
        else:
            return redirect(url_for("login"))
    else:
        if form.validate_on_submit():
            try:
                date = datetime.now().strftime('%d/%m/%Y %H:%M')
                NewPost = Post(form.content.data,form.title.data, str(date), current_user.get_id())
                db.session.add(NewPost)
                db.session.commit()
                print(NewPost)
                return redirect(url_for("index"))
            except:
                print("erro")
                return redirect(url_for("post"))
        else:
            return "ERRO!!"


@app.route('/profile/<int:id>/')
def profile(id):
    posts = Post.query.filter_by(id=id)

    if current_user.id == id:
        return redirect(url_for("my_profile"))
    else:
        return render_template('profile.html',profile=user, posts=posts)


@app.route('/profile/')
def my_profile():
    if current_user.is_authenticated == True:
        user = User.query.filter_by(id=current_user.id)
        posts = Post.query.filter_by(id=current_user.get_id())
        return render_template('my_profile.html', profile=user, posts=posts)
    else:
        redirect(url_for("register"))