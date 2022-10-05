from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route("/artists")
def artists():
    artist_list = ["Chief Keef", "Lil Baby", "Dababy"]

    return render_template('artists.html', title="Artist list", artists=artist_list)


@app.route('/artist')
def artist():
    info = {"name": "Chief Keef",
            "hometown": "Chicago",
            "description": "Chief Keef is a drill rapper coming from Chicago.He came on the the scene at just 16.",
            "events": ["Madison Square Garden on Friday 4/20", "TD Garden on Saturday 4/21", "Oracle Arena 4/24"]}
    return render_template('artist.html', title=info["name"], info=info)


@app.route('/new_artist', methods=['GET', 'POST'])
def new_artist():
    form = LoginForm()

    if form.validate_on_submit():
        flash('New Artist added'.format(
            form.name.data, form.home.data, form.description.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='New Artist', form=form)
