from extensions import db

class DeliveryAssignment(db.Model):
    __tablename__ = 'delivery_assignment'
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('delivery_provider.id'))


      # Relationships
    provider = db.relationship('DeliveryProvider', back_populates='assignments')
    purchase = db.relationship('Purchase', back_populates='delivery_assignments')
