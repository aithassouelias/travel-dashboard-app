from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

users_df = pd.read_json("./static/data/users.json")
travels_df = pd.read_json("./static/data/travels.json")
places_visited_df = pd.read_json("./static/data/place_visited.json")
hotels_df = pd.read_json("./static/data/hotels.json")

@app.route('/')
def dashboard():
    # Number of unique visited cities
    visited_cities = travels_df['destination'].nunique()
    
    return render_template('dashboard.html', visited_cities=visited_cities)

@app.route('/travels')
def travels():
    return render_template('travels.html')

@app.route('/travel_details')
def travel_details():
    return render_template('travel_details.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/friends')
def friends():
    return render_template('friends.html')

if __name__ == '__main__':
   app.run(debug=True)