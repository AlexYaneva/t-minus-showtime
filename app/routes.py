from app import app, cache, dynamo, table
from app.api import GetFilms, GetSeries
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask import flash, render_template, url_for, request, redirect, session
from flask_login import current_user, login_user, logout_user, login_required
from app.utils import countdown
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash



@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")




@app.route("/results", methods=["GET", "POST"])
def results():
    if request.form.get("film_title"):
        film_title = request.form["film_title"]
        films = GetFilms()
        results = films.search_films(film_title)
    elif request.form.get("series_title"):
        series_title = request.form["series_title"]
        series = GetSeries()
        results = series.search_series(series_title)

    return render_template("results.html", results=results)




@app.route("/films", methods=["GET", "POST"])
@login_required
@cache.cached(timeout=100)
def films():
    films = GetFilms()
    results = films.popular_films()
    return render_template("films.html", results=results)




@app.route("/tvseries", methods=["GET", "POST"])
@login_required
@cache.cached(timeout=100)
def tvseries():
    series = GetSeries()
    results = series.popular_series()
    return render_template("tvseries.html", results=results)




# makign 'title' an optional parameter
@app.route("/viewitem/<int:item_id>/", methods=["GET", "POST"])
@app.route("/viewitem/<int:item_id>/<title>", methods=["GET", "POST"])
def viewitem(item_id, title=None):
    if title:
        film = GetFilms()
        results = film.film_details(item_id=item_id)
    else:
        series = GetSeries()
        results = series.series_details(item_id=item_id)
    return render_template("viewitem.html", item_id=item_id, results=results)





@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("user"))
    form = LoginForm()
    if form.validate_on_submit():
        find_user = table.get_item(Key={"Email": form.email.data})
        user_item = find_user["Item"]

        if user_item is None or not User.check_password(user_item["password_hash"], form.password.data):
            return redirect(url_for("login"))
        user = User(email=user_item["Email"])
        login_user(user, remember=False)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)

    return render_template("login.html", title="Sign In", form=form)





@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("user"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = table.put_item(
                    Item={
                        "Email": form.email.data,
                        "Username": form.username.data},)
        password_hash = generate_password_hash(form.password.data)
        table.update_item(
            Key={"Email": form.email.data},
            UpdateExpression="SET password_hash = :setpass",
            ExpressionAttributeValues={":setpass": password_hash},)
        flash('You have successfully registered!')
        return redirect(url_for('login'))
        
    return render_template('register.html', title='Register', form=form)



@app.route("/user/<username>", methods=["GET", "POST"])
@login_required
def user(username):
    films = current_user.get_trackedfilms()
    series = current_user.get_trackedseries()
    return render_template("user.html", user=current_user, films=films, series=series, countdown=countdown)




@app.route("/track/<int:item_id>/", methods=["GET", "POST"])
@app.route("/track/<int:item_id>/<title>", methods=["GET", "POST"])
def track(item_id, title=None):
    if title:
        current_user.track_film(item_id)
        flash("Success! We've added this film to your dashboard.")
    else:
        current_user.track_series(item_id)
        flash("Success! We've added this series to your dashboard.")
    films = current_user.get_trackedfilms()
    series = current_user.get_trackedseries()
    return render_template("user.html", user=current_user, films=films, series=series, countdown=countdown)



@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("index"))
