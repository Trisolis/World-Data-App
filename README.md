# World-Data-App
Creating a small app using Flask to analyze world data from my earlier SQL project

## Features
- An index page featuring global or regional statistics (region can be selected from a dropdown menu by the user)
- A countries page which lists all countries linking to their respective pages. Can be filtered by region from a dropdown menu, or filtered by a search parameter the user inputs
- A country specific page for each country entry, listing specific statistics from world.db
- A cities page with the same features as the countries page, but does not have city specific pages/data
Built with Flask, SQLite, and Bootstrap

## Data
Covers ~240 countries with geographic, economic, and development indicators including GDP, HDI, life expectancy, literacy rate, and major cities. Database generated from cleaned CSVs included in the repo.

## Setup
Note: This project includes cleaned CSVs and schema.py from the SQL World Data project to generate the local database. No separate installation of that project is needed.
1. git clone ...
2. cd project
3. python -m venv venv
4. source venv/Scripts/activate
5. pip install -r requirements.txt
6. python schema.py    # generates world.db from included CSVs
7. python app.py
8. Visit http://127.0.0.1:5000

## Example Usage
Will fill out when pages have been stylized