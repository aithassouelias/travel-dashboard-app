from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

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
    return render_template('tables.html')

if __name__ == '__main__':
   app.run()