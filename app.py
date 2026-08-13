# Flask and routing logic
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('world.db')
    return conn

# Home page, potentially show summary stats from world.db
@app.route('/')
def home():
    return render_template('index.html')

# Accepts query parameter and searches countries by name
@app.route('/search')
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



if __name__ == '__main__':
    app.run()