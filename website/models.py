from . import db
from flask_login import UserMixin

#User Table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

#Artist Table
class Artist(db.Model):
    __bind_key__ = 'two'
    __tablename__ = 'artists'
    ArtistId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))

#Albums Table
class Album(db.Model):
    __bind_key__ = 'two'
    __tablename__ = 'albums'
    AlbumId = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255))
    ArtistId = db.Column(db.Integer, db.ForeignKey('ArtistId'))