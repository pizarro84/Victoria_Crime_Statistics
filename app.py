# import necessary libraries
import os
from sqlalchemy.sql import select, column, text
from sqlalchemy.sql.expression import func
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
from models import create_classes
import simplejson
from flask_sqlalchemy import SQLAlchemy

# init flask app
app = Flask(__name__)

# setup DB connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create db connection
db = SQLAlchemy(app)

# create a reference to the CRIME_LGA class
crime_stats_vic = create_classes(db)

# create route that renders index.html template
@app.route("/")
def home():
    """
    Render the index.html template
    """
    return render_template("index.html")

def query_results_to_dicts(results):
    # Convert SQLAlchemy query objects to json
    return simplejson.dumps(results)

def get_year_param():
    """
    Helper method for extracting the passed value to `race`
    in the query string - for example.

    http://localhost:5000/api/values/char_class/?race=troll

    Would return `"Troll"`    
    """
    selected_year = request.args.get("year")

    # If we receive "All" from the front-end no filtering
    if selected_year == "All":
        return None

    # Given the characters races in the database are title cased
    # e.g. "Orc" not "orc"
    if selected_year is not None:
        selected_year = selected_year.title()
    
    return selected_year

def get_lga_param():

    selected_lga = request.args.get("lga")

    # If we receive "All" from the front-end no filtering
    if selected_lga == "All":
        return None

    # Given the characters races in the database are title cased
    if selected_lga is not None:
        selected_lga = selected_lga.title()
    
    return selected_lga

def get_offence_param():

    selected_offence = request.args.get("lga")

    # If we receive "All" from the front-end no filtering
    if selected_offence == "All":
        return None

    # Given the characters races in the database are title cased
    if selected_offence is not None:
        selected_offence = selected_offence.title()
    
    return selected_offence

def get_distinct_values(for_column, 
                        year_filter = None, 
                        lga_filter = None, 
                        offence_filter = None):
    """
    Get unique values for a specified column under specific filters
    """
    
    value_query = db.session.query(
        func.distinct(getattr(crime_stats_vic, for_column))
    )

    if year_filter is not None:
        value_query = value_query.filter(
            crime_stats_vic.year == year_filter
        )
    
    if lga_filter is not None:
        value_query = value_query.filter(
            crime_stats_vic.local_government_area == lga_filter
        )
    
    if offence_filter is not None:
        value_query = value_query.filter(
            crime_stats_vic.offence_division == offence_filter
        )
    
    values = sorted([x[0] for x in value_query.all()])

    return values

@app.route("/api/values/<for_column>/<group_by>")
@app.route("/api/values/<for_column>/", defaults={'group_by': None})
def values(for_column, group_by = None):
    """
    This route will return all of the values in a column 
    optionally grouped by another column.

    For example http://localhost:5000/api/values/race/
    [
        "Orc", 
        "Tauren", 
        "Troll", 
        "Undead"
    ]

    Whereas http://localhost:5000/api/values/race/char_class
    {
        "Druid": [
            "Tauren", "Tauren", "Tauren", "Tauren", "Tauren", 
            "Tauren", "Tauren", "Tauren", "Tauren", "Tauren"
            ], 
        "Hunter": [
            "Orc", "Orc", "Orc", "Orc", "Orc", "Orc", "Orc",
            "Tauren", "Tauren", "Tauren", "Tauren", "Tauren"
            ]
    } 
    """
    # get filter parameters
    year_param = get_year_param()
    offence_param = get_offence_param()
    lga_param = get_lga_param()

    if group_by is None:
        values = get_distinct_values(for_column, year_param, lga_param, offence_param)
        return jsonify(values)

    values_for_groupby = dict()

    group_by_values = get_distinct_values(group_by, year_param, lga_param, offence_param)

    results = db.session.query(
        getattr(crime_stats_vic, group_by),
        getattr(crime_stats_vic, for_column),
    )

    if year_param is not None:
        results = results.filter(
            crime_stats_vic.year == year_param
        )
    
    if lga_param is not None:
        results = results.filter(
            crime_stats_vic.local_government_area == lga_param
        )
    
    if offence_param is not None:
        results = results.filter(
            crime_stats_vic.offence_division == offence_param
        )

    results = results.order_by(
        getattr(crime_stats_vic, group_by),
        getattr(crime_stats_vic, for_column),
    ).all()

    for group in group_by_values:
        values_for_groupby[group] = [x[1] for x in results if x[0] == group]

    return query_results_to_dicts(values_for_groupby)

if __name__ == "__main__":
    app.run(debug=True)