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
@app.route('/country/<iso_code>')
def country(iso_code):
    conn = get_db()
    results = conn.execute('''
        SELECT c.*, i.population, i.birth_rate, i.death_rate, i.life_expectancy, i.literacy_rate, i.density, i.hdi, e.gdp_ppp,
               e.gdp_per_capita, e.inflation, e.unemployment, e.public_debt_pct, e.gdp
        FROM countries c
        LEFT JOIN indicators i ON c.iso_code=i.iso_code
        LEFT JOIN economy e ON c.iso_code=e.iso_code
        WHERE c.iso_code == ?
        ''', (iso_code,)).fetchone()
    conn.close()
    return render_template('country.html', country=results)

@app.route('/cities')
def cities():
    return render_template('cities.html')
# Still need a 'country' route and a 'cities' route, probably a specific city/cities from x country route too


if __name__ == '__main__':
    app.run(debug=True) # remove before deploying