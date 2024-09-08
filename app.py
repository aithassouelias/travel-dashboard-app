from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from map_route import create_map_with_multiple_routes
from forms import AddTripForm, AddPOIForm
from models import db, Trip, POI

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/travels', methods=['GET', 'POST'])
def travels():
    form = AddTripForm()
    if form.validate_on_submit():
        new_trip = Trip(
            title=form.title.data,
            description=form.description.data,
            destination=form.destination.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            image=form.image.data.filename if form.image.data else None
        )
        db.session.add(new_trip)
        db.session.commit()
        return redirect(url_for('travels'))
    
    trips = Trip.query.all()  # Récupère tous les voyages de la base de données
    return render_template('travels.html', trips=trips, form=form)

@app.route('/travel/<int:trip_id>', methods=['GET', 'POST'])
def travel_details(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    pois = POI.query.filter_by(trip_id=trip_id).all()
    duration = (trip.end_date - trip.start_date).days  # Assuming you want to calculate the duration
    num_visited_pois = len([poi for poi in pois if poi.visited])
    num_to_visit_pois = len([poi for poi in pois if not poi.visited])

    form = AddPOIForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            new_poi = POI(
                name=form.name.data,
                visit_date=form.visit_date.data,
                latitude=form.latitude.data,
                longitude=form.longitude.data,
                visited=form.visited.data,
                trip_id=trip.id
            )
            db.session.add(new_poi)
            db.session.commit()
            return redirect(url_for('travel_details', trip_id=trip.id))
    
    pois_for_map = [
        {
            'name': poi.name,
            'coords': (poi.longitude, poi.latitude),
            'date_time': poi.visit_date.strftime('%Y-%m-%d %H:%M')  # Assuming `visit_date` is a datetime object
        }
        for poi in pois
    ]
    api_key = '5b3ce3597851110001cf624859eadc08586440cca8901585be5744ea' 

    create_map_with_multiple_routes(pois_for_map, api_key)

    
    return render_template('travel_details.html', trip=trip, pois=pois, duration=duration,
                           num_visited_pois=num_visited_pois, num_to_visit_pois=num_to_visit_pois, form=form)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/friends')
def friends():
    return render_template('friends.html')

if __name__ == '__main__':
   with app.app_context():
        db.create_all()  # Crée toutes les tables
   app.run(debug=True)
