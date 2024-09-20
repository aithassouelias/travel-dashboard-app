from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from utils.functions import create_map_with_multiple_routes, create_empty_map, get_coordinates, get_location_info
from utils.forms import AddTripForm, AddPOIForm, ModifyProfileForm, AddUserForm
from utils.models import db, Trip, POI, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = AddUserForm()
    if form.validate_on_submit():
        new_user = User(
            email=form.email.data,
            password=form.password.data,
            username="@eliasait7",
            date_of_birth=form.date_of_birth.data
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('sign-up.html', form=form)

@app.route('/sign-in')
def sign_in():
    return render_template('sign-in.html')

@app.route('/dashboard')
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
            image=form.image.data.filename if form.image.data else None,
            user_id = 1
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
    duration = (trip.end_date - trip.start_date).days
    
    num_visited_pois = 0 + len([poi for poi in pois if poi.visited])
    num_to_visit_pois = 0 + len([poi for poi in pois if not poi.visited])

    form = AddPOIForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # Recup coordinates from place name
            coordinates = get_coordinates(form.name.data)
            place_name = get_location_info(coordinates[0], coordinates[1])
            # Save the new POI in the database
            new_poi = POI(
                name=form.name.data,
                visit_date=form.visit_date.data,
                latitude=coordinates[0],
                longitude=coordinates[1],
                visited=form.visited.data,
                trip_id=trip.id
            )
            db.session.add(new_poi)
            db.session.commit()
            return redirect(url_for('travel_details', trip_id=trip.id))
    
    if pois: 
        pois_for_map = [
            {
                'name': poi.name,
                'coords': (poi.longitude, poi.latitude),
                'date_time': poi.visit_date.strftime('%Y-%m-%d %H:%M')
            }
            for poi in pois
        ]
        api_key = '5b3ce3597851110001cf624859eadc08586440cca8901585be5744ea' 

        # map_html = create_map_with_multiple_routes(pois_for_map, api_key)
        map_html = create_empty_map()
    else : 
        map_html = create_empty_map()
    
    return render_template('travel_details.html', trip=trip, pois=pois, duration=duration,
                           num_visited_pois=num_visited_pois, num_to_visit_pois=num_to_visit_pois, form=form, map_html=map_html)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ModifyProfileForm()
    if form.validate_on_submit():
        new_user = User(
            user_id = form.user_id.data, 
            username = form.username.data,
            date_of_birth = form.date_of_birth.data,
            email = form.email.data
        )
    return render_template('profile.html', form=form)

@app.route('/friends')
def friends():
    return render_template('friends.html')

if __name__ == '__main__':
   with app.app_context():
        db.create_all()  # Crée toutes les tables
   app.run(debug=True)
