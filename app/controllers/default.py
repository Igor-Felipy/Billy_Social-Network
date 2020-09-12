from app import app, db, lm
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user

from app.models.tables import User
from app.models.forms import LoginForm, RegisterForm

@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()




@app.route("/index/")
@app.route("/")
def index():
    return render_template('index.html')


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
            NewUserData = User(form.username.data,form.password.data,form.name.data, form.email.data)
            print(NewUserData)
            db.session.add(NewUserData)
            db.session.commit()
            return redirect(url_for("login"))
        except:
            return redirect(url_for("register"))
    else:
        print(form.errors)
    return render_template('register.html', form=form)







@app.route('/teste/<info>/')
@app.route('/teste/', defaults={"info": None})
def teste(info):
    r = User.query.filter_by(password="1234").all()
    print(r)
    return "ok"




# uso do create
#    i = User("IgorFelip","123","Igor Felipy", "igor@gmail.com")
#    db.session.add(i)
#    db.session.commit()