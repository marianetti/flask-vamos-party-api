from flask import Flask

from flask_restx import Api

from flask_migrate import Migrate

from .users.views import user_namespace
from .clubs.views import club_namespace
from .events.views import event_namespace

from .config.config import config_dict

from .utils import db

from .models.users import User
from .models.clubs import Club
from .models.events import Event



def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    
    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate(app, db)

    api = Api(app)

    api.add_namespace(user_namespace, path='/users')
    api.add_namespace(club_namespace, path='/clubs')
    api.add_namespace(event_namespace, path='/events')

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db' : db,
            'User' : User,
            'Club' : Club,
            'Event' : Event
        }

    return app