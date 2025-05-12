from extensions import db

class DeliveryProvider(db.Model):
    __bind_key__ = 'master'
    __tablename__ = 'delivery_provider'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    coverage_area = db.Column(db.String(150))
    cost = db.Column(db.Float)

    assignments = db.relationship('DeliveryAssignment', back_populates='provider')
