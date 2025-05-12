from flask import Flask, render_template
from extensions import db, login_manager
from models.user import User
from sqlalchemy.exc import OperationalError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

# URI de la base de datos primaria (SQLite)
primary_db_uri = 'mysql+pymysql://bookstore_user:bookstore_pass@34.196.144.93:3306/bookstore'

# URI de la base de datos secundaria (MySQL) con las credenciales proporcionadas
secondary_db_uri = 'mysql+pymysql://bookstore_user:bookstore_pass@54.210.119.201:3306/bookstore'

# Intentar conectar a la base de datos primaria
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = primary_db_uri
    db.init_app(app)
    print("Conexión exitosa a la base de datos primaria (SQLite)")
except OperationalError as e:
    print(f"Error al conectar con la base de datos primaria, intentando con la base de datos secundaria: {e}")
    
    # Si la base de datos primaria falla, intenta conectarse a la base de datos secundaria (MySQL)
    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = secondary_db_uri
        db.init_app(app)
        print("Conexión exitosa a la base de datos secundaria (MySQL)")
    except OperationalError as e:
        print(f"Error al conectar con la base de datos secundaria: {e}")

login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Luego importar blueprints
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

if __name__ == '__main__':
    # Crear las tablas e inicializar los proveedores de entrega
    with app.app_context():
        db.create_all()
        initialize_delivery_providers()
    app.run(host="0.0.0.0", debug=True)
