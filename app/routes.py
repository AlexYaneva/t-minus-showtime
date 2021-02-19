from app import app, cache, dynamo, table
from app.api import GetFilms, GetSeries
from app.email import send_password_reset_email
from app.forms import LoginForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm, SearchForm
from app.models import User
from flask import flash, render_template, url_for, request, redirect, session, jsonify, make_response
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash
import app.utils as utils
import app.db_helpers as db



@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")




@app.route("/results/<group>/<title>", methods=["GET", "POST"])
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
    form = SearchForm()
    if form.validate_on_submit():
        film_title = form.search.data
        return redirect(url_for("results", group="films", title=film_title))
    films = GetFilms(page=1)
    results = films.popular_films()

    return render_template("films.html", results=results, form=form)




@app.route("/tvseries", methods=["GET", "POST"])
def tvseries():
    form = SearchForm()
    if form.validate_on_submit():
        series_title = form.search.data
        return redirect(url_for("results", group="series", title=series_title))
    series = GetSeries(page=1)
    results = series.popular_series()

    return render_template("tvseries.html", results=results, form=form)


@app.route("/series_airing_today", methods=["GET", "POST"])
@cache.cached(timeout=100)
def series_airing_today():
    series = GetSeries(page=1)
    results = series.series_airing_today()

    return render_template("series_airing_today.html", results=results)


@app.route("/series_on_the_air", methods=["GET", "POST"])
@cache.cached(timeout=100)
def series_on_the_air():
    series = GetSeries(page=1)
    results = series.series_on_the_air()

    return render_template("series_on_the_air.html", results=results)


@app.route("/top_rated", methods=["GET", "POST"])
# @cache.cached(timeout=100)
def top_rated():
    page = request.args.get('page', 1, type=int)
    films = GetFilms(page)
    results = films.top_rated()
    return render_template("top_rated_films.html", results=results)


@app.route("/load_more")
def load_more():
    page = request.args.get('page', 2, type=int)
    films = GetFilms(page)
    results = films.top_rated()
    return jsonify(render_template('_display_posters.html', results=results))


@app.route("/films_in_theatres", methods=["GET", "POST"])
@cache.cached(timeout=100)
def films_in_theatres():
    films = GetFilms(page=1)
    results = films.films_in_theatres()

    return render_template("films_in_theatres.html", results=results)


# makign 'title' an optional parameter
@app.route("/viewitem/<int:item_id>/", methods=["GET", "POST"])
@app.route("/viewitem/<int:item_id>/<title>", methods=["GET", "POST"])
@login_required
def viewitem(item_id, title=None):
    if title:
        film = GetFilms(page=1)
        results = film.film_details(item_id=item_id)
        countdwn = utils.countdown(results["release_date"])
        recommends = film.film_recommendations(item_id=item_id)
    else:
        series = GetSeries(page=1)
        results = series.series_details(item_id=item_id)
        if results["next_episode_to_air"]:
            countdwn = utils.countdown(results["next_episode_to_air"]['air_date'])
        else:
            countdwn = -1
        recommends = series.series_recommendations(item_id=item_id)

    return render_template("viewitem.html", item_id=item_id, results=results, recommends=recommends, countdown=countdwn)





@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("user"))
    form = LoginForm()
    if form.validate_on_submit():
        user_record = db.get_user(form.email.data)

        if user_record is None or not User.check_password(user_record["Password_hash"], form.password.data):
            return redirect(url_for("login"))
        user = User(email=user_record["Email"])
        login_user(user, remember=False)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("user", username=user.username)
        return redirect(next_page)

    return render_template("login.html", title="Sign In", form=form)





@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("user"))
    form = RegistrationForm()
    if form.validate_on_submit():

        # add a check if email exists already
        db.create_new_user(form.email.data, form.username.data)
        password_hash = generate_password_hash(form.password.data)
        db.update_password(form.email.data, password_hash)
        flash('You are now registered! Welcome on board.')
        return redirect(url_for('login'))
        
    return render_template('register.html', title='Register', form=form)




@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user_record = db.get_user(form.email.data)
        if isinstance(user_record, str):
            flash('No user found')
            return render_template('login.html')
        user = User(email=user_record["Email"])
        send_password_reset_email(user).apply_async()

        flash('Check your email for instructions to reset your password')
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
    films = current_user.get_trackedfilms()
    series = current_user.get_trackedseries()

    return render_template("user.html", user=current_user, films=films, series=series)




@app.route("/track/<int:item_id>/<countdown>/", methods=["GET", "POST"])
@app.route("/track/<int:item_id>/<countdown>/<title>", methods=["GET", "POST"])
def track(item_id, countdown, title=None):
    if title:
        current_user.track_film(item_id, countdown)
        flash("Success! We've added this film to your dashboard.")
    else:
        current_user.track_series(item_id, countdown)
        flash("Success! We've added this show to your dashboard.")
    films = current_user.get_trackedfilms()
    series = current_user.get_trackedseries()

    return render_template("user.html", user=current_user, films=films, series=series)



@app.route("/untrack/<int:item_id>/", methods=["GET", "POST"])
@app.route("/untrack/<int:item_id>/<title>", methods=["GET", "POST"])
def untrack(item_id, title=None):
    # need to change the url no longer needing title
    current_user.untrack(item_id)
    flash("You're no longer tracking this.")
    films = current_user.get_trackedfilms()
    series = current_user.get_trackedseries()

    return render_template("user.html", user=current_user, films=films, series=series)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()

    return redirect(url_for("index"))
