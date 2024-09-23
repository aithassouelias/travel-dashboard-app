from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Users(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Personnal informations
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False) 
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    
    # Optional informations
    biography = db.Column(db.String(150))
    instagram_link = db.Column(db.String(150))
    tiktok_link = db.Column(db.String(150))

    # User Preferences
    account_type = db.Column(db.Boolean, nullable=False)

    # Relationships
    trips = db.relationship('Trips', backref='trips', lazy=True)

class Destinations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)

class Transport_Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    icon = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
class Trips(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Trip informations
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    destination = db.Column(db.String(100))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    cover_picture = db.Column(db.String(100))

    # Relationships
    destinations = db.relationship('Destinations', backref='trips', lazy=True)
    pois = db.relationship('Points_Of_Interest', backref='trips', lazy=True)
    users = db.relationship('Users', backref='trips', lazy=True)
    owner_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    transport_type_id = db.Column(db.Integer, db.ForeignKey('Transport_Type.id'), nullable=False)

class Points_Of_Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # POI informations
    name = db.Column(db.String(100), nullable=False)
    visit_date = db.Column(db.Date, nullable=False)  
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    visited = db.Column(db.Boolean, nullable=False)
    type = db.Column(db.String(100)) # Monument, restaurant...

    # POI optional informations
    notes = db.Column(db.String(255))
    link_info = db.Column(db.String(100))

    # Relationships
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)