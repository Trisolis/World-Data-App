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
    region = request.args.get('region')

    conn = get_db()

    if region:
        stats = conn.execute('''
            SELECT 
                COUNT(DISTINCT c.iso_code) AS country_count,
                COUNT(DISTINCT ci.name) AS cities_count,
                SUM(i.population) AS total_population,
                SUM(e.gdp) AS total_gdp,
                AVG(i.hdi) AS avg_hdi,
                AVG(i.life_expectancy) as avg_life_expectancy,
                AVG(i.literacy_rate) as avg_literacy,
                AVG(e.unemployment) as avg_unemployment
            FROM countries c 
            LEFT JOIN indicators i ON c.iso_code=i.iso_code
            LEFT JOIN economy e ON c.iso_code=e.iso_code
            LEFT JOIN cities ci ON c.iso_code=ci.iso2
            WHERE c.region = ?

        ''', (region,)).fetchone()
    else:
        stats = conn.execute('''
            SELECT 
                COUNT(DISTINCT c.iso_code) AS country_count,
                COUNT(DISTINCT ci.name) AS cities_count,
                SUM(i.population) AS total_population,
                SUM(e.gdp) AS total_gdp,
                AVG(i.hdi) AS avg_hdi,
                AVG(i.life_expectancy) as avg_life_expectancy,
                AVG(i.literacy_rate) as avg_literacy,
                AVG(e.unemployment) as avg_unemployment
            FROM countries c 
            LEFT JOIN indicators i ON c.iso_code=i.iso_code
            LEFT JOIN economy e ON c.iso_code=e.iso_code
            LEFT JOIN cities ci ON c.iso_code=ci.iso2
        ''').fetchone()

    regions = conn.execute('SELECT DISTINCT region FROM countries ORDER BY region').fetchall()
    conn.close()
    return render_template('index.html', stats=stats, regions=regions, current_region=region)

# Lists all countries, perhaps filtered by region
@app.route('/countries')
def countries():
    region = request.args.get('region')
    search = request.args.get('search')

    conn = get_db()

    if region:
        results = conn.execute('''
            SELECT * FROM countries
            WHERE region = ?
            ORDER BY name
        ''', (region,)).fetchall()
    elif search:
        results = conn.execute('''
            SELECT * FROM countries
            WHERE name LIKE ?
            ORDER BY name
        ''', (f'%{search}%',)).fetchall()
    else:
        results = conn.execute('''
            SELECT * FROM countries
            ORDER BY name
        ''').fetchall()

    regions = conn.execute('SELECT DISTINCT region FROM countries ORDER BY region').fetchall()
    conn.close()
    return render_template('countries.html', countries=results, regions=regions, current_region=region, current_search=search)

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
    region = request.args.get('region')
    search = request.args.get('search')

    conn = get_db()

    
    if region:
        results = conn.execute('''
            SELECT ci.*, co.name as country_name, co.region
            FROM cities ci
            JOIN countries co ON ci.iso2 = co.iso_code
            WHERE co.region = ?
            ORDER BY ci.population DESC
        ''', (region,)).fetchall()
    elif search:
        results = conn.execute('''
            SELECT ci.*, co.name as country_name, co.region
            FROM cities ci
            JOIN countries co ON ci.iso2 = co.iso_code
            WHERE ci.name LIKE ? OR co.name LIKE ?
            ORDER BY ci.population DESC
        ''', (f'%{search}%', f'%{search}%')).fetchall()
    else:
        results = conn.execute('''
            SELECT ci.*, co.name as country_name, co.region
            FROM cities ci
            JOIN countries co ON ci.iso2 = co.iso_code
            ORDER BY ci.population DESC
        ''').fetchall()

    regions = conn.execute('SELECT DISTINCT region FROM countries ORDER BY region').fetchall()
    conn.close()
    return render_template('cities.html', cities=results, regions=regions, current_region=region, current_search=search)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()