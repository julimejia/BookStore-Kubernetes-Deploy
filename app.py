from flask import Flask, render_template
from extensions import db, login_manager
from models.user import User
from models.delivery import DeliveryProvider
from models.purchase import Purchase
from models.delivery_assignment import DeliveryAssignment

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

# Conexión a la base de datos maestra (para escrituras)
master_db_uri = 'mysql+pymysql://bookstore_user:bookstore_pass@34.196.144.93:3307/bookstore'

# Conexión a la base de datos esclava (para lecturas)
slave_db_uri = 'mysql+pymysql://bookstore_user:bookstore_pass@54.210.119.201:3307/bookstore'

# Configurar SQLAlchemy para manejar conexiones al master y al slave
app.config['SQLALCHEMY_BINDS'] = {
    'master': master_db_uri,
    'slave': slave_db_uri
}

# Inicializar extensiones
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registrar blueprints
from controllers.auth_controller import auth
from controllers.book_controller import book
from controllers.purchase_controller import purchase
from controllers.payment_controller import payment
from controllers.delivery_controller import delivery
from controllers.admin_controller import admin

app.register_blueprint(auth)
app.register_blueprint(book, url_prefix='/book')
app.register_blueprint(purchase)
app.register_blueprint(payment)
app.register_blueprint(delivery)
app.register_blueprint(admin)

@app.route('/')
def home():
    return render_template('home.html')

def initialize_delivery_providers():
    with db.engines['master'].connect() as connection:
        db.session.bind = connection
        if DeliveryProvider.query.count() == 0:
            providers = [
                DeliveryProvider(name="DHL", coverage_area="Internacional", cost=50.0),
                DeliveryProvider(name="FedEx", coverage_area="Internacional", cost=45.0),
                DeliveryProvider(name="Envia", coverage_area="Nacional", cost=20.0),
                DeliveryProvider(name="Servientrega", coverage_area="Nacional", cost=15.0),
            ]
            db.session.bulk_save_objects(providers)
            db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        # Crear las tablas en orden específico si es necesario
        with db.engines['master'].begin() as connection:
            # Crear tablas sin foreign keys primero
            db.metadata.tables['delivery_provider'].create(connection, checkfirst=True)
            db.metadata.tables['purchase'].create(connection, checkfirst=True)

            # Luego tablas con claves foráneas
            db.metadata.tables['delivery_assignment'].create(connection, checkfirst=True)

        initialize_delivery_providers()
    
    app.run(host="0.0.0.0", debug=True)
