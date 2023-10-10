from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Artist, Album

#Blueprint for View Routes
views = Blueprint("views", __name__)

#Define Home Route (Must be logged in to see).
@views.route('/')
@login_required
def home():
    return render_template("home.html")

#Define Artists Route (Must be logged in to see).
@views.route('/artists')
@login_required
def artist_view():
    artists = Artist.query.all()
    return render_template("artists.html", artists=artists)

#Define Albums Route (Must be logged in to see).
@views.route('/albums')
@login_required
def album_view():
    albums = Album.query.all()
    return render_template("albums.html", albums=albums)