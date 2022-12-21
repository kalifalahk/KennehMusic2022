import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, ArtistForm, RegistrationForm, VenueForm, EventForm
from app.models import Artist, Event, Venue, ArtistToEvent, User
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/artists')
def artists():
    art = Artist.query.all()
    print(art)
    return render_template('artists.html', title='Artists', artists=art)


@app.route('/artist/<name>')
def artist(name):
    art = Artist.query.filter(Artist.name == name).first_or_404()

    return render_template('artist.html', title=art.name, artist=art)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/new_artist', methods=['GET', 'POST'])
@login_required
def new_artist():
    if request.method == 'POST':
        artist_name = request.form["name"]
        artist_home = request.form["home"]
        artist_desc = request.form["description"]
        art = Artist.query.filter(Artist.name == artist_name).first()
        if art is not None:
            return render_template('artists.html', title='Artists', artists=Artist.query.all(), error=True,
                                   error_artist=artist_name)
        db.session.add(Artist(name=artist_name, hometown=artist_home, description=artist_desc))
        db.session.commit()
        return render_template('artists.html', title='Artists', artists=Artist.query.all())
    else:
        form = ArtistForm()
        return render_template('newartist.html', form=form)


@app.route('/new_venue', methods=['GET', 'POST'])
def new_venue():
    form = VenueForm()
    if form.validate_on_submit():
        venue = Venue(name=form.name.data, location=form.address.data + "," + form.city.data + "," + form.state.data)
        db.session.add(venue)
        db.session.commit()
        flash('New venue created!')
        return redirect(url_for('index'))
    return render_template('newvenue.html', form=form)


@app.route('/new_event', methods=['GET', 'POST'])
def new_event():
    form = EventForm()
    form.venue.choices = [v.name for v in Venue.query.all()]
    form.artist.choices = [v.name for v in Artist.query.all()]
    if form.validate_on_submit():
        print(form.venue.data)
        event = Event(name=form.name.data, date=form.date.data,
                      venue_id=Venue.query.filter(Venue.name == form.venue.data).first().id)
        db.session.add(event)
        db.session.commit()
        for artist in form.artist.data:
            db_Artist = Artist.query.filter(Artist.name == artist).first()
            if db_Artist is not None:
                artistevent = ArtistToEvent(artist_id=db_Artist.id, event_id=event.id)
                db.session.add(artistevent)
                db.session.commit()

        flash('New Event created!')
        return redirect(url_for('index'))
    return render_template('newevent.html', form=form)


@app.route('/populate_db')
def populate_db():
    artists = [
        Artist(name='Chief Keef', hometown='Chicago', description="Test"),
        Artist(name='Lil Baby', hometown='Atlanta', description="Test"),
        Artist(name='Jay-Z', hometown='Brooklyn', description="Test"),
        Artist(name='Kay Flock', hometown='Bronx', description="Test"),
        Artist(name='Drake', hometown='Toronto', description="Test")
    ]
    db.session.add_all(artists)
    db.session.commit()

    # venues
    venues = [
        Venue(name='Madison Square Garden', location='New York'),
        Venue(name='Hollywood Bowl', location='Los Angeles'),
        Venue(name='United Center', location='Chicago'),
        Venue(name='Disney World', location='Miami'),
        Venue(name='United Center', location='Chicago')
    ]
    db.session.add_all(venues)
    db.session.commit()

    # events
    events = [
        Event(name=' Rolling Loud', venue_id=venues[0].id,
              date=datetime.datetime.strptime("Sat, Oct 06 2022", "%a, %b %d %Y")),
        Event(name='Lalapolloza', venue_id=venues[1].id,
              date=datetime.datetime.strptime("Mon, Apr 04 2022", "%a, %b %d %Y")),
        Event(name='VMA', venue_id=venues[2].id, date=datetime.datetime.strptime("Sat, Oct 06 2022", "%a, %b %d %Y")),
        Event(name='BET awards', venue_id=venues[0].id,
              date=datetime.datetime.strptime("Fri, Jun 01 2022", "%a, %b %d %Y")),
        Event(name='Halftime Show', venue_id=venues[1].id,
              date=datetime.datetime.strptime("Sun, Jul 04 2022", "%a, %b %d %Y")),
        Event(name='Governors Ball', venue_id=venues[2].id,
              date=datetime.datetime.strptime("Sun, Jul 14 2022", "%a, %b %d %Y")),
        Event(name='Hip Hop Awards', venue_id=venues[0].id,
              date=datetime.datetime.strptime("Fri, Apr 20 2022", "%a, %b %d %Y"))
    ]
    db.session.add_all(events)
    db.session.commit()
    artist_to_events = [
        ArtistToEvent(artist_id=artists[0].id, event_id=events[0].id),
        ArtistToEvent(artist_id=artists[1].id, event_id=events[0].id),
        ArtistToEvent(artist_id=artists[2].id, event_id=events[1].id),
        ArtistToEvent(artist_id=artists[3].id, event_id=events[1].id),
        ArtistToEvent(artist_id=artists[4].id, event_id=events[2].id),
        ArtistToEvent(artist_id=artists[2].id, event_id=events[2].id),
        ArtistToEvent(artist_id=artists[3].id, event_id=events[3].id),
        ArtistToEvent(artist_id=artists[4].id, event_id=events[3].id),
        ArtistToEvent(artist_id=artists[4].id, event_id=events[0].id),
        ArtistToEvent(artist_id=artists[1].id, event_id=events[3].id),
        ArtistToEvent(artist_id=artists[1].id, event_id=events[4].id)

    ]
    db.session.add_all(artist_to_events)
    db.session.commit()

    flash("Database has been populated")
    return render_template('base.html', title='Home')


@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()
