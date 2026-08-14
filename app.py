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

'''
# Accepts query parameter and searches countries by name (should redirect to /countries?region=Europe or something similar)
@app.route('/search?q=<something>')
def search():
    # code here
    pass
'''

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
        SELECT c.*, i.population, i.life_expectancy, i.literacy_rate, i.hdi, e.gdp_per_capita, e.inflation, e.unemployment, e.gdp
        FROM countries c
        LEFT JOIN indicators i ON c.iso_code=i.iso_code
        LEFT JOIN economy e ON c.iso_code=e.iso_code
        WHERE c.iso_code = ?
        ''', (iso_code,)).fetchone()
    conn.close()
    return render_template('country.html', country=results)

@app.route('/cities')
def cities():
    conn = get_db()
    return render_template('cities.html')

if __name__ == '__main__':
    app.run(debug=True) # remove before deploying