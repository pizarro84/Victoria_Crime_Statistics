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
        crime_stats_vic.row_id,
        crime_stats_vic.year,
        crime_stats_vic.local_government_area,
        crime_stats_vic.offence_division,
        crime_stats_vic.incidents_recorded
    ).all()

    return query_results_to_dicts(results)

@app.route("/api/values/<for_column>/<group_by>")
@app.route("/api/values/<for_column>/", defaults={'group_by': None})
def values(for_column, group_by = None):
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

@app.route("/api/where/<local_government_area>")
def where(local_government_area):
    
    results = db.engine.execute(text("""
        SELECT * FROM crime_lga 
        WHERE UPPER(local_government_area) = :local_government_area
    """).bindparams(
        local_government_area=local_government_area.upper().strip()
    ))

    return jsonify([dict(row) for row in results])

@app.route("/api/sum_by/<sum_by>", defaults={'optional_sum_by': None})
@app.route("/api/sum_by/<sum_by>/<optional_sum_by>")
def sum_by(sum_by, optional_sum_by=None):

    # first let's check if we need to filter
    selected_offence = get_lga_param()
   
    # let's first handle the case we there is no `optional_count_by`
    if optional_sum_by is None:
        results = db.session.query(
            getattr(crime_stats_vic, sum_by),
            func.count(getattr(crime_stats_vic, sum_by)).label("total")
        )

        # apply the query stirng filter if present
        if selected_offence is not None:
            results = results.filter(crime_stats_vic.local_government_area == selected_offence)

        results = results.group_by(
            getattr(crime_stats_vic, sum_by)
        ).order_by(
            getattr(crime_stats_vic, sum_by)
        ).all()

    else:
        # lets handle grouping by two columns
        results = db.session.query(
            getattr(crime_stats_vic, sum_by),
            getattr(crime_stats_vic, optional_sum_by),
            func.count(getattr(crime_stats_vic, sum_by)).label("total")
        )

        if selected_offence is not None:
            results = results.filter(crime_stats_vic.offence_division == selected_offence)

        results = results.group_by(
            getattr(crime_stats_vic, sum_by),
            getattr(crime_stats_vic, optional_sum_by)
        ).order_by(
            getattr(crime_stats_vic, sum_by),
            getattr(crime_stats_vic, optional_sum_by),
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
        lga_clause = " AND UPPER(local_government_area) = UPPER(\"" + lga + "\") "

    if offence != "All":
        offence_clause = " AND UPPER(offence_division) = UPPER(\"" + offence + "\") "
    
    
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