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

import config
from datetime import datetime
import os
import smtplib


NOTIF = ("Dû au resultat positif de {}, fait le {} proche de vous ({}), "
         "nous vous encourageons vivement vous {} à vous mettre en quarantaine "
         "et à faire un test dans l'immédiat!\n"
         "Le Maire du quartier")

FILE_NOTIF_SMS = "./templates/model/notification.sms.model"
FILE_NOTIF_EMAIL = "./templates/model/notification.email.model"

def get_current_date_fr():
    return datetime.today().strftime("%d-%m-%Y")


def get_current_date_en():
    return datetime.today().strftime("%Y/%m/%d")


def get_current_time():
    return datetime.today().strftime("%H:%M:%S")


def load_file(file_):
    with open(file_,'r') as f:
        file_content = f.read().strip()
    return file_content


def write_file(file_, text_):
    f = open(file_, "a")
    f.write(text_)
    f.close()


def create_folder(paths_):
    os.makedirs(paths_, exist_ok=True)
    
    
def send_email(recipient, body):
    """ 
    Source : https://stackoverflow.com/questions/37224073/smtp-auth-extension-not-supported-by-server
    """
    s = smtplib.SMTP('64.233.184.108',587)
    s.ehlo()
    s.starttls()
    s.login(config.GMAIL_USER,config.GMAIL_PWD)
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (config.GMAIL_USER, recipient, config.SUBJECT, body.encode('utf-8'))
    try:
        s.sendmail(config.GMAIL_USER,recipient,message)
    except:
        print("error")