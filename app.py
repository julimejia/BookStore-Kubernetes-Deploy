from flask import Flask, render_template
from extensions import db, login_manager
from models.user import User
from sqlalchemy.exc import OperationalError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

# Conexión a la base de datos maestra (para escrituras)
master_db_uri = 'mysql+pymysql://bookstore_user:bookstore_pass@34.196.144.93:3306/bookstore'

# Conexión a la base de datos esclava (para lecturas)
slave_db_uri = 'mysql+pymysql://bookstore_user:bookstore_pass@54.210.119.201:3306/bookstore'

# Configurar SQLAlchemy para manejar conexiones al master y al slave
app.config['SQLALCHEMY_BINDS'] = {
    'master': master_db_uri,
    'slave': slave_db_uri
}

# Configuración de la base de datos con SQLAlchemy
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

# Registrar blueprints
app.register_blueprint(auth)
app.register_blueprint(book, url_prefix='/book')
app.register_blueprint(purchase)
app.register_blueprint(payment)
app.register_blueprint(delivery)
app.register_blueprint(admin)

from models.delivery import DeliveryProvider

def initialize_delivery_providers():
    with app.app_context():
        if DeliveryProvider.query.count() == 0:
            providers = [
                DeliveryProvider(name="DHL", coverage_area="Internacional", cost=50.0),
                DeliveryProvider(name="FedEx", coverage_area="Internacional", cost=45.0),
                DeliveryProvider(name="Envia", coverage_area="Nacional", cost=20.0),
                DeliveryProvider(name="Servientrega", coverage_area="Nacional", cost=15.0),
            ]
            db.session.bulk_save_objects(providers)
            db.session.commit()

@app.route('/')
def home():
    return render_template('home.html')

# Ruta para escribir en la base de datos (Master)
@app.route('/write')
def write_to_db():
    db.session.bind = db.get_engine(app, bind='master')
    # Realizar operaciones de escritura como insert/update/delete
    return "Escritura exitosa en la base de datos maestra."

# Ruta para leer de la base de datos (Slave)
@app.route('/read')
def read_from_db():
    db.session.bind = db.get_engine(app, bind='slave')
    # Realizar operaciones de lectura como select
    return "Lectura exitosa desde la base de datos esclava."

if __name__ == '__main__':
    with app.app_context():
        # Crear las tablas utilizando el motor de la base de datos maestra
        with db.get_engine(app, bind='master').connect() as connection:
            db.create_all(bind='master')  # Aquí se crea todo en la base de datos maestra
            initialize_delivery_providers()
    app.run(host="0.0.0.0", debug=True)

