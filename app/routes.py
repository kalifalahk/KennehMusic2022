import datetime

from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm
from app.models import Artist, Event, Venue, ArtistToEvent


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


@app.route('/new_artist', methods=['GET', 'POST'])
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
        form = LoginForm()
        return render_template('newartist.html', form=form)


@app.route('/populate_db')
def populate_db():
    artists = [
        Artist(name='Chief Keef', hometown='Chicago'),
        Artist(name='Lil Baby', hometown='Atlanta'),
        Artist(name='Jay-Z', hometown='Brooklyn'),
        Artist(name='Kay Flock', hometown='Bronx'),
        Artist(name='Drake', hometown='Toronto')
    ]
    db.session.add_all(artists)
    db.session.commit()

    # venues
    venues = [
        Venue(name='Madison Square Garden', location='New York'),
        Venue(name='Hollywood Bowl', location='Los Angeles'),
        Venue(name='United Center', location='Chicago')
    ]
    db.session.add_all(venues)
    db.session.commit()

    # events
    events = [
        Event(name=' Rolling Loud', venue_id=venues[0].id,
              date=datetime.datetime.strptime("Sat, Oct 06 2018", "%a, %b %d %Y")),
        Event(name='Lalapolloza', venue_id=venues[1].id,
              date=datetime.datetime.strptime("Sat, Oct 06 2018", "%a, %b %d %Y")),
        Event(name='VMA', venue_id=venues[2].id, date=datetime.datetime.strptime("Sat, Oct 06 2018", "%a, %b %d %Y")),
        Event(name='BET awards', venue_id=venues[0].id,
              date=datetime.datetime.strptime("Sat, Oct 06 2018", "%a, %b %d %Y")),
        Event(name='Halftime Show', venue_id=venues[1].id,
              date=datetime.datetime.strptime("Sat, Oct 06 2018", "%a, %b %d %Y")),
        Event(name='Governors Ball', venue_id=venues[2].id,
              date=datetime.datetime.strptime("Sat, Oct 06 2018", "%a, %b %d %Y")),
        Event(name='Hip Hop Awards', venue_id=venues[0].id,
              date=datetime.datetime.strptime("Sat, Oct 06 2018", "%a, %b %d %Y"))
    ]
    db.session.add_all(events)
    db.session.commit()
    artist_to_events = [
        ArtistToEvent(artist_id=artists[0].id, event_id=events[0].id),
        ArtistToEvent(artist_id=artists[1].id, event_id=events[0].id),
        ArtistToEvent(artist_id=artists[2].id, event_id=events[1].id),
        ArtistToEvent(artist_id=artists[3].id, event_id=events[1].id),
        ArtistToEvent(artist_id=artists[4].id, event_id=events[2].id)
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
