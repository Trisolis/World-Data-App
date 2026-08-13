# Flask and routing logic
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('world.db')
    conn.row_factory = sqlite3.Row # so I can access by name rather than index
    return conn

# Home page, summary stats from the database
@app.route('/')
def home():
    return render_template('index.html')

# Accepts query parameter and searches countries by name (should redirect to /countries?region=Europe or something similar)
@app.route('/search?q=<something>')
def search():
    # code here
    pass

# Lists all countries, perhaps filtered by region
@app.route('/countries')
def countries():
    conn = get_db()
    results = conn.execute('SELECT * FROM countries').fetchall()
    conn.close()
    return render_template('countries.html', countries=results)

# Display a specific country and its data
@app.route('/countries/<iso_code>')
def country(iso_code):
    conn = get_db()
    results = conn.execute('''
        SELECT * 
        FROM countries c
        JOIN indicators i ON c.iso_code=i.iso_code
        JOIN economy e ON c.iso_code=e.iso_code
        JOIN cities c2 ON c.iso_code=c2.iso_code
        WHERE c.iso_code == {country_code}
        ''')
    # query db for this country
    # get its indicators/data (definitely needs to be fixed up)
    return render_template('country.html', data=results)

@app.route('/cities')
def cities():
    return render_template('cities.html')
# Still need a 'country' route and a 'cities' route, probably a specific city/cities from x country route too


if __name__ == '__main__':
    app.run(debug=True) # remove before deploying