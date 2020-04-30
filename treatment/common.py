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

from datetime import datetime


NOTIF = ("Dû au resultat positif de {}, fait le {} proche de vous ({}), "
         "nous vous encourageons vivement vous {} à vous mettre en quarantaine "
         "et à faire un test dans l'immédiat!\n"
         "Le Maire du quartier")

def get_current_date():
    return datetime.today().strftime('%d-%m-%Y')

def get_current_time():
    return datetime.today().strftime('%H:%M:%S')