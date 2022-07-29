from app import app, cache, dynamo, table
from app.tmdb_api import GetFilms, GetSeries
from app.email import send_password_reset_email, send_notification_emails
from app.forms import LoginForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm, SearchForm
from app.models import User
from flask import flash, render_template, url_for, request, redirect, session, jsonify, make_response
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash
import app.utils as utils
import app.db_helpers as db


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
@cache.cached(timeout=600)
def index():

    return render_template("index.html")


@app.route("/results/<group>/<title>", methods=["GET"])
def results(group, title):

    if group == "films":
        films = GetFilms(page=1)
        results = films.search_films(title)
    elif group == "series":
        series = GetSeries(page=1)
        results = series.search_series(title)
    if not results:
        return render_template("notfound.html")

    return render_template("results.html", results=results)


@app.route("/films", methods=["GET", "POST"])
def films():
    page = 1
    form = SearchForm()
    if form.validate_on_submit():
        film_title = form.search.data
        return redirect(url_for("results", group="films", title=film_title))
    films = GetFilms(page)

    results = films.popular_films()
    top_rated = films.top_rated()
    in_theatres = films.films_in_theatres()

    return render_template("films.html", results=results, top_rated=top_rated, in_theatres=in_theatres, form=form)


@app.route("/top_rated", methods=["GET"])
def top_rated():
    page = request.args.get('page', 2, type=int)
    films = GetFilms(page)
    results = films.top_rated()

    return jsonify(render_template('_display_posters.html', results=results))


@app.route("/films_in_theatres", methods=["GET"])
def films_in_theatres():
    page = request.args.get('page', 2, type=int)
    films = GetFilms(page)
    results = films.films_in_theatres()

    return jsonify(render_template('_display_posters.html', results=results))


@app.route("/popular_films", methods=["GET"])
def popular_films():
    page = request.args.get('page', 2, type=int)
    films = GetFilms(page)
    results = films.popular_films()

    return jsonify(render_template('_display_posters.html', results=results))


@app.route("/tvseries", methods=["GET", "POST"])
def tvseries():
    page = 1
    form = SearchForm()
    if form.validate_on_submit():
        series_title = form.search.data
        return redirect(url_for("results", group="series", title=series_title))
    series = GetSeries(page)

    results = series.popular_series()
    airing_today = series.series_airing_today()
    on_the_air = series.series_on_the_air()

    return render_template("tvseries.html", results=results, on_the_air=on_the_air, airing_today=airing_today,  form=form)


@app.route("/series_airing_today", methods=["GET"])
def series_airing_today():
    page = request.args.get('page', 2, type=int)
    series = GetSeries(page)
    results = series.series_airing_today()

    return jsonify(render_template('_display_posters.html', results=results))


@app.route("/series_on_the_air", methods=["GET"])
def series_on_the_air():
    page = request.args.get('page', 2, type=int)
    series = GetSeries(page)
    results = series.series_on_the_air()

    return jsonify(render_template('_display_posters.html', results=results))


@app.route("/popular_series", methods=["GET"])
def popular_series():
    page = request.args.get('page', 2, type=int)
    series = GetSeries(page)
    results = series.popular_series()

    return jsonify(render_template('_display_posters.html', results=results))


# makign 'title' an optional parameter
@app.route("/viewitem/<int:item_id>/", methods=["GET"])
@app.route("/viewitem/<int:item_id>/<title>", methods=["GET"])
@login_required
def viewitem(item_id, title=None):
    if title:
        film = GetFilms(page=1)
        results = film.film_details(item_id=item_id)
        results = results[0]
        countdwn = film.set_countdown(results)
        recommends = film.film_recommendations(item_id=item_id)
        media_type = "film"
    else:
        series = GetSeries(page=1)
        results = series.series_details(item_id=item_id)
        results = results[0]
        countdwn = series.set_countdown(results)
        recommends = series.series_recommendations(item_id=item_id)
        media_type = "series"

    return render_template("viewitem.html", item_id=item_id, results=results, recommends=recommends,
                           countdown=countdwn, countries=utils.countries, media_type=media_type)


@app.route("/film_watch/<int:item_id>", methods=["GET"])
def film_watch(item_id):
    film = GetFilms(page=1)
    results = film.watch_providers(item_id=item_id)
    return jsonify(results)


@app.route("/series_watch/<int:item_id>", methods=["GET"])
def series_watch(item_id):
    series = GetSeries(page=1)
    results = series.watch_providers(item_id=item_id)
    return jsonify(results)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("user", username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user_record = db.get_user(form.email.data)
        if user_record is None or not User.check_password(user_record["Password_hash"], form.password.data):
            flash("Oops... Invalid username or password. Try again!")
            return redirect(url_for("login"))
        user = User(email=user_record["Email"])
        login_user(user, remember=False)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for(
                "user", username=user.username)
        return redirect(next_page)

    return render_template("login.html", title="Sign In", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("user", username=current_user.username))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_record = db.get_user(form.email.data)
        if user_record is None:
            db.create_new_user(form.email.data, form.username.data)
            password_hash = generate_password_hash(form.password.data)
            db.update_password(form.email.data, password_hash)
            flash('You are now registered. Welcome on board!')
        else:
            flash("Oops... This email is already registered!")
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user_record = db.get_user(form.email.data)
        if user_record is not None:
            user = User(email=user_record["Email"])
            send_password_reset_email(user).apply_async()

        flash('Check your email for instructions to reset your password.')
        return redirect(url_for('login'))

    return render_template('reset_password_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user_record = User.verify_reset_password_token(token)
    if not user_record:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User(email=user_record["Email"])
        user.set_password(form.password.data)
        flash('Success! Your password has been reset.')
        return redirect(url_for('login'))

    return render_template('reset_password.html', form=form)


@app.route("/user/<username>", methods=["GET", "POST"])
@login_required
def user(username):

    # TEST
    # a_dict = db.get_all_releasing_tomorrow("series")
    # send_notification_emails(a_dict)
    # END

    films = current_user.get_trackedfilms()
    series = current_user.get_trackedseries()

    return render_template("user.html", user=current_user, films=films, series=series)


@app.route("/track/<int:item_id>/", methods=["GET", "POST"])
@app.route("/track/<int:item_id>/<group>", methods=["GET", "POST"])
def track(item_id, group):
    if group == "films":
        film = GetFilms(page=1)
        tmdb_response = film.film_details(item_id=item_id)
        title = tmdb_response[0]["title"]
        poster_path = tmdb_response[0]["poster_path"]
        current_user.track_film(item_id, title, poster_path)
    elif group == "series":
        series = GetSeries(page=1)
        tmdb_response = series.series_details(item_id=item_id)
        title = tmdb_response[0]["name"]
        poster_path = tmdb_response[0]["poster_path"]
        current_user.track_series(item_id, title, poster_path)
    flash("Success! We've added this title to your dashboard.")
    films = current_user.get_trackedfilms()
    series = current_user.get_trackedseries()

    return render_template("user.html", user=current_user, films=films, series=series)


@app.route("/untrack/<int:item_id>/", methods=["GET", "POST"])
def untrack(item_id):
    current_user.untrack(item_id)
    flash("You're no longer tracking this.")
    films = current_user.get_trackedfilms()
    series = current_user.get_trackedseries()

    return render_template("user.html", user=current_user, films=films, series=series)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()

    return redirect(url_for("index"))


@app.route("/delete_account/<email>", methods=["GET", "POST"])
def delete_account(email):
    db.delete_user(email)
    flash("Your account has been deleted.")
    return redirect(url_for("index"))
