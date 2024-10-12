from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from utils.functions import generate_username,create_map_with_multiple_routes, create_empty_map, create_map_with_multiple_pois, get_coordinates, get_location_info, get_pretty_location_infos
from utils.forms import AddTripForm, AddPOIForm, ModifyProfileForm, AddUserForm, UserConnexionForm
from utils.models import db, Trips, Points_Of_Interest, Users
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from logging import FileHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

# Initialize Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'sign_in'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/sign-up', methods=['GET','POST'])
def sign_up():
    form = AddUserForm()
    if form.validate_on_submit():
        
        # Check if the email already exists
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            flash('Cette adresse mail est déjà utilisée.')
            return redirect(url_for('sign_in'))
        
        if form.password.data == form.password_confirm.data:
            new_user = Users(
                email=form.email.data,
                name=form.email.data.split('@')[0],
                password=generate_password_hash(form.password.data, method='pbkdf2:sha256'),
                username=form.email.data.split('@')[0],
                account_type=1
            )
            db.session.add(new_user)
            db.session.commit()  # This should save the new user to the database
            return redirect(url_for('dashboard'))
        else:
            flash('Veuillez confirmer votre mot de passe avec un mot de passe identique')
    else:
        print(form.errors)  # Print errors if form validation fails

    return render_template('sign-up.html', form=form)

@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    form = UserConnexionForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = Users.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password) :
            print(user.password, password)
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid credentials. Please try again.', 'danger')
    return render_template('sign-in.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('sign_in'))

@app.route('/dashboard')
@login_required
def dashboard():
    trips = Trips.query.filter_by(owner_user=current_user.id).all()
    num_trips = 0+ len(trips)
    countries_visited = 0+ len(trips)
    

    destinations = []
    for trip in trips:
        lat, lon = get_coordinates(trip.destination)
        if trip.destination:  # Assurez-vous que la destination existe
            destinations.append((
                trip.title,         # Nom de la destination
                [lat, lon]
            ))
    # Créer la carte avec les destinations
    map_html = create_map_with_multiple_pois(destinations)  # Remplacez par votre clé API
    return render_template('dashboard.html', num_trips=num_trips, map_html=map_html)

@app.route('/travels', methods=['GET', 'POST'])
@login_required
def travels():
    form = AddTripForm()
    if form.validate_on_submit():
        # Get destinations informations
        destination_infos = get_pretty_location_infos(form.destination.data)
        city = destination_infos[0]
        country = destination_infos[1]
        
        # Save this trip
        new_trip = Trips(
            title=form.title.data,
            destination=city+","+country,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            transport_type = form.transport_type.data,
            owner_user = current_user.id
        )
        db.session.add(new_trip)
        db.session.commit()
        return redirect(url_for('travels'))
    
    trips = Trips.query.all()  # Recup all trips in the database
    return render_template('travels.html', trips=trips, form=form)

@app.route('/travel/<int:trip_id>', methods=['GET', 'POST'])
@login_required
def travel_details(trip_id):
    trip = Trips.query.get_or_404(trip_id)
    pois = Points_Of_Interest.query.filter_by(trip_id=trip_id).all()
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
            print(form.visited.data)
            new_poi = Points_Of_Interest(
                name=form.name.data,
                visit_date=form.visit_date.data,
                latitude=coordinates[0],
                longitude=coordinates[1],
                visited=bool(form.visited.data),
                trip_id=trip.id
            )
            db.session.add(new_poi)
            db.session.commit()
            return redirect(url_for('travel_details', trip_id=trip.id))
    
    if pois: 
        pois_for_map = [
            {
                'name': poi.name,
                'coords': [float(poi.longitude), float(poi.latitude)],
                'date_time': poi.visit_date.strftime('%Y-%m-%d %H:%M')
            }
            for poi in pois
        ]
        api_key = '5b3ce3597851110001cf624859eadc08586440cca8901585be5744ea' 

        map_html = create_map_with_multiple_routes(pois_for_map,api_key)
    else : 
        lat, lon = get_coordinates(trip.destination)
        map_html = create_empty_map(lat, lon)
    
    return render_template('travel_details.html', trip=trip, pois=pois, duration=duration,
                           num_visited_pois=num_visited_pois, num_to_visit_pois=num_to_visit_pois, form=form, map_html=map_html)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ModifyProfileForm()
    if form.validate_on_submit():
        new_user = Users(
            user_id = form.user_id.data, 
            username = form.username.data,
            date_of_birth = form.date_of_birth.data,
            email = form.email.data
        )
    username = current_user.username
    name = current_user.name
    return render_template('profile.html', form=form, username=username, name=name)

@app.route('/friends')
@login_required
def friends():
    return render_template('friends.html')

if __name__ == '__main__':
   with app.app_context():
        db.create_all()  # Crée toutes les tables
   app.run(debug=True)
