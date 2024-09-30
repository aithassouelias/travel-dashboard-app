from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Personal information
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    profile_picture = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    
    # Optional information
    biography = db.Column(db.String(150))
    instagram_link = db.Column(db.String(150))
    tiktok_link = db.Column(db.String(150))

    # User preferences
    account_type = db.Column(db.Boolean, nullable=False)

    # Relationships
    trips = db.relationship('Trips', backref='user', lazy=True)

class Destinations(db.Model):
    __tablename__ = 'destinations'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)

class Transport_Type(db.Model):
    __tablename__ = 'transport_type'  # Explicit table name

    id = db.Column(db.Integer, primary_key=True)
    icon = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)

class Trips(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    
    # Trip information
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    destination = db.Column(db.String(100))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    cover_picture = db.Column(db.String(100))

    # Relationships
    destinations = db.relationship('Destinations', backref='trip', lazy=True)
    pois = db.relationship('Points_Of_Interest', backref='trip', lazy=True)
    owner_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    transport_type_id = db.Column(db.Integer, db.ForeignKey('transport_type.id'), nullable=False)

class Points_Of_Interest(db.Model):
    __tablename__ = 'points_of_interest'

    id = db.Column(db.Integer, primary_key=True)

    # POI information
    name = db.Column(db.String(100), nullable=False)
    visit_date = db.Column(db.Date, nullable=False)  
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    visited = db.Column(db.Boolean, nullable=False)
    type = db.Column(db.String(100))  # Monument, restaurant...

    # POI optional information
    notes = db.Column(db.String(255))
    link_info = db.Column(db.String(100))

    # Relationships
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
