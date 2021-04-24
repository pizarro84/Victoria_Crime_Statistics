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

# create route that renders index.html template
@app.route("/heatmap")
def heatmap():
    """
    Render the index.html template
    """
    return render_template("heatmap.html")

# create route that renders index.html template
@app.route("/alldata")
def alldata():
    """
    Render the index.html template
    """
    return render_template("alldata.html")

@app.route("/api/all")
def all():
        
    results = db.session.query(
        crime_stats_vic.year,
        crime_stats_vic.local_government_area,
        crime_stats_vic.offence_division,
        crime_stats_vic.incidents_recorded
    )

    results = results.order_by(
        getattr(crime_stats_vic, 'year'),
        getattr(crime_stats_vic, 'local_government_area'),
    ).all()

    return query_results_to_dicts(results)

@app.route("/api/values/<for_column>")
def values(for_column, group_by = None):
    value_query = db.session.query(
        func.distinct(getattr(crime_stats_vic, for_column))
    )
    
    values = sorted([x[0] for x in value_query.all()])

    return jsonify(values)

@app.route("/api/sum_by_year")
def count_by_lga():
    
    results = db.session.query(
        crime_stats_vic.year,
        func.sum(crime_stats_vic.incidents_recorded).label("total")
    )

    results = results.group_by(
        crime_stats_vic.year
    ).all()

    return query_results_to_dicts(results)

@app.route("/api/sum_by_incidents")
def count_by_offence():
    
    results = db.session.query(
        crime_stats_vic.offence_division,
        func.sum(crime_stats_vic.incidents_recorded).label("total")
    )

    results = results.group_by(
        crime_stats_vic.offence_division
    ).all()

    return query_results_to_dicts(results)

@app.route("/api/query/<year>/<lga>/<offence>")
def query(year, lga, offence):
    
    year_clause = "";
    lga_clause = "";
    offence_clause="";

    if year != "All":
        year_clause = " AND year = " + year + " "

    if lga != "All":
        lga_clause = " AND UPPER(local_government_area) = UPPER('" + lga + "') "

    if offence != "All":
        offence_clause = " AND UPPER(offence_division) = UPPER('" + offence + "') "
    
    
    results = db.engine.execute(text("WITH temp AS(SELECT * FROM crime_lga  WHERE 1 = 1 " 
                                     + year_clause + lga_clause + offence_clause
                                     + "), totals AS(SELECT year, local_government_area, "
                                     + "                    SUM(incidents_recorded) total "
                                     + "               FROM temp GROUP BY year, local_government_area limit 10) "
                                     + "SELECT tm.year, tm.local_government_area,tm.offence_division,"
                                     + "       tm.incidents_recorded,tot.total "
                                     + "  FROM temp tm, totals tot "
                                     + " WHERE tm.year = tot.year "
                                     + "   AND tm.local_government_area = tot.local_government_area "
                                     + " ORDER BY total DESC, incidents_recorded DESC"))

    return jsonify([dict(row) for row in results])

@app.route("/api/getalldata")
def getalldata():   
    results = db.engine.execute(text("WITH temp AS(SELECT * FROM crime_lga  WHERE 1 = 1 " 
                                     + "), totals AS(SELECT year, local_government_area, "
                                     + "                    SUM(incidents_recorded) total "
                                     + "               FROM temp GROUP BY year, local_government_area) "
                                     + "SELECT tm.year, tm.local_government_area,tm.offence_division,"
                                     + "       tm.incidents_recorded,tot.total "
                                     + "  FROM temp tm, totals tot "
                                     + " WHERE tm.year = tot.year "
                                     + "   AND tm.local_government_area = tot.local_government_area "
                                     + " ORDER BY total DESC, incidents_recorded DESC"))

    return jsonify([dict(row) for row in results])



if __name__ == "__main__":
    app.run(debug=True)