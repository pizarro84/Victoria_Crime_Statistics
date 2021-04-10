def create_classes(db):
    class CRIME_LGA(db.Model):
        __tablename__ = 'CRIME_LGA'

        year = db.Column(db.Integer)
        year_ending = db.Column(db.String(64))
        police_service_area=db.Column(db.String(64))
        local_government_area=db.Column(db.String(64))
        offence_division=db.Column(db.String(64))
        offence_subdivision=db.Column(db.String(64))
        Offence_subgroup=db.Column(db.String(64))
        incidents_recorded = db.Column(db.double)
        psa_rate_per_100k_population = db.Column(db.double)
        lga_rate_per_100k_population = db.Column(db.double)            

        def __repr__(self):
            return '<crime %r>' % (self.name)
    return CRIME_LGA
