from app import app, cache
from app.api import Films, Series
from app.forms import LoginForm
from app.models import User, TrackedFilms, TrackedSeries
from flask import render_template, url_for, request, redirect, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/results", methods=["GET", "POST"])
def results():
    if request.form.get("film_title"):
        film_title = request.form["film_title"]
        films = Films()
        results = films.search_films(film_title)
    elif request.form.get("series_title"):
        series_title = request.form["series_title"]
        series = Series()
        results = series.search_series(series_title)

    return render_template("results.html", results=results)


@app.route("/films", methods=["GET", "POST"])
@login_required
@cache.cached(timeout=100)
def films():
    films = Films()
    results = films.popular_films()
    return render_template("films.html", results=results)


@app.route("/tvseries", methods=["GET", "POST"])
@login_required
@cache.cached(timeout=100)
def tvseries():
    series = Series()
    results = series.popular_series()
    return render_template("tvseries.html", results=results)


# makign 'title' optional parameter
@app.route("/viewitem/<int:item_id>/", methods=["GET", "POST"])
@app.route("/viewitem/<int:item_id>/<title>", methods=["GET", "POST"])
def viewitem(item_id, title=None):
    if title:
        film = Films()
        results = film.film_details(item_id=item_id)
    else:
        series = Series()
        results = series.series_details(item_id=item_id)
    return render_template("viewitem.html", item_id=item_id, results=results)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("user"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)

    return render_template("login.html", title="Sign In", form=form)


@app.route("/user/<username>", methods=["GET", "POST"])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    films = current_user.trackedfilms()
    series = current_user.trackedseries()
    return render_template(
        "user.html", user=current_user, trackedfilms=films, trackedseries=series
    )


@app.route("/track/<int:item_id>", methods=["GET", "POST"])
def track(item_id):
    print(f"Tracking this film: {item_id}")
    return render_template("user.html", user=user)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("index"))
