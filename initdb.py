import os
import csv
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy import DateTime, Float, Integer, String

meta = MetaData()

#postgresql://admin:aa1320@localhost:5432/VIC_crime


connection = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"

print("connection to databse: " + connection)
engine = create_engine(connection)

if not engine.has_table("CRIME_LGA"):
    print("Creating Table")

    new_table = Table(
        'CRIME_LGA', meta,
        Column('row_id', Integer),
        Column('Year', Integer),
        Column('Local_Government_Area', String),
        Column('Offence_Division', String),
        Column('Incidents_Recorded', Integer),        
    )

    meta.create_all(engine)
    
    seed_data = list()

    with open('./02-Data/crimesdata_pre_aggregate.csv', newline='') as input_file:
        reader = csv.DictReader(input_file)       #csv.reader is used to read a file
        for row in reader:
            seed_data.append(row)
            
    with engine.connect() as conn:
        conn.execute(new_table.insert(), seed_data)

    print("Data Import Successful")
else:
    print("Table already exists")

print("initdb complete")