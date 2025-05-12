from flask import Flask, request
from sqlalchemy.exc import OperationalError
from extensions import db, login_manager
from models.user import User

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

# Función para verificar la conectividad con la base de datos
def check_master_connection():
    try:
        with db.engines['master'].connect() as connection:
            return True  # Si la conexión es exitosa, el maestro está disponible
    except OperationalError as e:
        print(f"Error al conectar al maestro: {e}")
        return False  # El maestro no está disponible

@app.before_request
def before_request():
    """Seleccionar la base de datos según el tipo de operación (lectura o escritura)."""
    # Verifica si el maestro está disponible
    if request.method == "GET":
        # Si el maestro no está disponible, usar el esclavo para lecturas
        if not check_master_connection():
            print("El maestro no está disponible. Usando el esclavo para lecturas.")
            db.session.remove()  # Eliminar la sesión anterior para evitar reutilización
            db.session = db.sessionmaker(bind=db.engines['slave'])()  # Usar el esclavo
            # Cambiar dinámicamente el bind de los modelos a 'slave'
            for model in db.Model._decl_class_registry.values():
                if hasattr(model, '__bind_key__'):
                    model.__bind_key__ = 'slave'
        else:
            db.session.remove()  # Eliminar la sesión anterior
            db.session = db.sessionmaker(bind=db.engines['slave'])()  # Usar el esclavo para lectura
            # Cambiar dinámicamente el bind de los modelos a 'master'
            for model in db.Model._decl_class_registry.values():
                if hasattr(model, '__bind_key__'):
                    model.__bind_key__ = 'master'
    elif request.method in ["POST", "PUT", "DELETE"]:
        # Para operaciones de escritura, usar la base de datos maestra
        db.session.remove()
        db.session = db.sessionmaker(bind=db.engines['master'])()
        # Cambiar dinámicamente el bind de los modelos a 'master'
        for model in db.Model._decl_class_registry.values():
            if hasattr(model, '__bind_key__'):
                model.__bind_key__ = 'master'

@app.teardown_request
def teardown_request(exception=None):
    """Cerrar la sesión al final de cada solicitud."""
    db.session.remove()

# Resto del código...

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
