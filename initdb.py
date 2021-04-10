import os
from sqlalchemy import create_engine, Table, Column, Float, Integer, String, MetaData

meta = MetaData()

#postgresql://admin:aa1320@localhost:5432/VIC_crime


connection = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"

print("connection to databse")
engine = create_engine(connection)

if not engine.has_table("CRIME_LGA"):
    print("Creating Table")

    new_table = Table(
        'CRIME_LGA', meta,
        Column('Year', Integer),
        Column('Year_ending', String),
        Column('Police_Service_Area', String),
        Column('Local_Government_Area', String),
        Column('Offence_Division', String),
        Column('Offence_Subdivision', String),
        Column('Offence_Subgroup', String),
        Column('Incidents_Recorded', Float),
        Column('PSA_Rate_per_100k_population', Float),
        Column('LGA_Rate_per_100k_population', Float),        
    )

    meta.create_all(engine)
    
    print("Table created")

    seed_data = [        {"Year":2020,"Year_ending":"December","Police_Service_Area":"Ballarat","Local_Government_Area":"Ballarat","Offence_Division":"A Crimes against the person","Offence_Subdivision":"A10 Homicide and related offences","Offence_Subgroup":"A10 Homicide and related offences","Incidents_Recorded":2,"PSA_Rate_per_100k_population":1.7,"LGA_Rate_per_100k_population":1.8},
        {"Year":2020,"Year_ending":"December","Police_Service_Area":"Pyrenees","Local_Government_Area":"Ballarat","Offence_Division":"A Crimes against the person","Offence_Subdivision":"A10 Homicide and related offences","Offence_Subgroup":"A10 Homicide and related offences","Incidents_Recorded":2,"PSA_Rate_per_100k_population":1.7,"LGA_Rate_per_100k_population":26.7},
                 
                 {"Year":2020,"Year_ending":"December","Police_Service_Area":"Pyrenees","Local_Government_Area":"Ballarat","Offence_Division":"A Crimes against the person","Offence_Subdivision":"A20 Assault and related offences","Offence_Subgroup":"A211 FV Serious assault","Incidents_Recorded":22,"PSA_Rate_per_100k_population":18.5,"LGA_Rate_per_100k_population":294.1},
    ]
    
    with engine.connect() as conn:
        conn.execute(new_table.insert(), seed_data)

    print("Seed Data Imported")
else:
    print("Table already exists")
print("initdb complete")