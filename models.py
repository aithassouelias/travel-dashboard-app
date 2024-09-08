from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    destination = db.Column(db.String(255))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    image = db.Column(db.String(100))
    destinations = db.relationship('Destination', backref='trip', lazy=True)
    # Relationship with POI
    pois = db.relationship('POI', backref='trip', lazy=True)

class POI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    visit_date = db.Column(db.Date, nullable=True)  # Date of visit
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    visited = db.Column(db.Boolean, nullable=False)  # 0 for "to visit", 1 for "visited"
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
