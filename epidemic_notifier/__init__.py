#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = "Albin TCHOPBA"
# __copyright__ = "Copyright 2020 Albin TCHOPBA and contributors"
# __credits__ = ["Albin TCHOPBA and contributors"]
# __license__ = "GPL"
# __version__ = "3"
# __maintainer__ = "Albin TCHOPBA"
# __email__ = "Albin TCHOPBA <atchopba @ gmail dot com"
# __status__ = "Production"

from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()


def create_app():
    #
    app = Flask(__name__, instance_relative_config=False)
    #
    app.config.from_object("config.Config")
    #
    login_manager.init_app(app)
    #
    with app.app_context():
        from . import routes
        from . import auth
        #
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)
        #
        if app.config["FLASK_ENV"] == "development":
            pass
        #
        return app
