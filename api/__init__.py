from flask import Flask

from flask_restx import Api

from flask_migrate import Migrate

from .duenos.views import duenos_namespace
from .discotecas.views import discotecas_namespace

from .config.config import config_dict

from .utils import db

from .models.duenos import Dueno
from .models.discotecas import Discoteca



def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    
    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate(app, db)

    api = Api(app)

    api.add_namespace(duenos_namespace, path='/duenos')
    api.add_namespace(discotecas_namespace, path='/discotecas')

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db' : db,
            'Dueno' : Dueno,
            'Discoteca' : Discoteca
        }

    return app