def create_classes(db):
    class CRIME_LGA(db.Model):
        __tablename__ = 'CRIME_LGA'

        row_id = db.Column(db.Integer, primary_key=True)
        year = db.Column(db.Integer)
        local_government_area=db.Column(db.String(64))
        offence_division=db.Column(db.String(64))
        incidents_recorded = db.Column(db.Integer)          

        def __repr__(self):
            """
                results = db.session.query(
                                -> this one replace with (crime_stats_vic) AvatarHistory.race,
                                func.count(AvatarHistory.race).label("total")
                                )
            """
            return f'<crime_stats_vic {self.id}>'
    
    return CRIME_LGA
