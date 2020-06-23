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

from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    
    GMAIL_USER = environ.get("GMAIL_USER")
    GMAIL_PWD = environ.get("GMAIL_PWD")
    
    # sujet des mails
    SUBJECT = "Epidemie - alerte"
    
    ERROR_MSG_INSERT = "Veuillez recommencer!"
    
    SUSPECT_SCORE_MIN = 0.6
    
    FILE_NOTIF_SMS = "./epidemic_notifier/templates/model/notification.sms.model"
    FILE_NOTIF_EMAIL = "./epidemic_notifier/templates/model/notification.email.model"

    FLASK_APP = "wsgi.py"
    FLASK_ENV = environ.get("FLASK_ENV")
    SECRET_KEY = environ.get("SECRET_KEY")

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    COMPRESSOR_DEBUG = environ.get('COMPRESSOR_DEBUG')

    # Databases
    MULTI_DATABASE = False
    DATABASE_URI = "./epidemic_notifier/static/data/main.db"
    DATABASE_CLIENT = None
