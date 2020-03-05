from app import app
from app.api import API
from app.forms import LoginForm
from app.models import User
from flask import render_template, url_for, request, redirect
from flask_login import current_user, login_user, logout_user


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/results", methods=["GET", "POST"])
def results():
    if request.form.get("film_title"):
        film_title = request.form["film_title"]
        obj = API()
        results = obj.search_film(film_title)
    elif request.form.get("series_title"):
        series_title = request.form["series_title"]
        obj = API()
        results = obj.search_series(series_title)

    return render_template("results.html", results=results)


@app.route("/films", methods=["GET", "POST"])
def films():
    obj = API()
    results = obj.popular_films()
    return render_template("films.html", results=results)


@app.route("/tvseries", methods=["GET", "POST"])
def tvseries():
    obj = API()
    results = obj.popular_series()
    return render_template("tvseries.html", results=results)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)

        # # Storing the value of 'next' i.e. which page the user wanted to see but was prompted to log in first
        # next_page = request.args.get('next')

        # # The parse and netloc are security checks
        # if not next_page or url_parse(next_page).netloc != '':
        # 	next_page = url_for('main.index')
        return redirect(url_for("index"))

    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("index"))
