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

from config import Config
from datetime import datetime
import os
from collections import namedtuple


NOTIF = ("Dû au resultat positif de {}, fait le {} proche de vous ({}), "
         "nous vous encourageons vivement vous {} à vous mettre en quarantaine "
         "et à faire un test dans l'immédiat!\n"
         "Le Maire du quartier")

CPersonne = namedtuple("CPersonne", "nb_personnes nb_p_gueris nb_p_suspects")
CTest = namedtuple("CTest", "nb_t_tests nb_t_positifs nb_t_negatifs")

SUSPECT_CHECKBOX = "suspect"
SUSPECT_VALUE_POS = "oui"
SUSPECT_VALUE_NEG = "non"

P_SIGNE_CHECKBOX = "presente_signe"
P_SIGNE_VALUE_POS = "oui"
P_SIGNE_VALUE_NEG = "non"

PERSONNE_GUERI_1 = "clinique"
PERSONNE_GUERI_2 = "biologique"

def get_current_date_fr():
    return datetime.today().strftime("%d/%m/%Y")

def get_current_date_en():
    return datetime.today().strftime("%Y/%m/%d")

def get_current_time():
    return datetime.today().strftime("%H:%M")

def get_current_timestamp():
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
    
def send_email(recipient, text_):
    #
    # Source : https://realpython.com/python-send-email/#sending-a-plain-text-email
    # 
    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    #
    sender_email = Config.GMAIL_USER
    receiver_email = recipient
    password = Config.GMAIL_PWD
    #
    message = MIMEMultipart("alternative")
    message["Subject"] = Config.SUBJECT
    message["From"] = sender_email
    message["To"] = receiver_email
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    part = MIMEText(text_, "html")
    message.attach(part)
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    except:
        print("erreur lors de l'envoi de mail")
