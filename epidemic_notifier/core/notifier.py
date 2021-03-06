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

from epidemic_notifier.core import common as cm
from epidemic_notifier.core.db.test import Test
from epidemic_notifier.core.db.contact_relation_personne import CRP
from epidemic_notifier.core.db.personne_notification import TPNotification, PNotification
from config import Config

import json


notif_sm_sms = cm.load_file(Config.FILE_SM_NOTIF_SMS)
notif_sm_email = cm.load_file(Config.FILE_SM_NOTIF_EMAIL)

notif_m_sms = cm.load_file(Config.FILE_M_NOTIF_SMS)
notif_m_email = cm.load_file(Config.FILE_M_NOTIF_EMAIL)

path_root = "./__temp__/notif/"
path_sms = path_root + "sms/" + cm.get_current_date_en() + "/"
path_email = path_root + "email/" +cm.get_current_date_en() + "/"

cm.create_folder(path_sms)
cm.create_folder(path_email)

def param_notif(notif, crp, p):
    notif = notif.replace("#PERSONNE_DUE#", p.p_nom +" "+ p.p_prenom)
    notif = notif.replace("#DATE_TEST_DUE#", p.date_test)
    notif = notif.replace("#RELATION#", crp.relation)
    notif = notif.replace("#PERSONNE_INFORMED#", crp.nom +" "+ crp.prenom)
    notif = notif.replace("#MALADIE#", Config.MALADIE)
    return notif

def notifier_personne(notification_id):
    
    notif_dict = []
    
    # 1. selectionner les personnes avec le test positifs
    p_suppose_malades_dict = Test().get_supposes_malades(Config.SUSPECT_SCORE_MIN)
    p_malades_dict = Test().get_malades()
    
    # appel de la fonction de notification
    notif_dict.append(notify_personne(notif_m_sms, notif_m_email, p_suppose_malades_dict))
    notif_dict.append(notify_personne(notif_sm_sms, notif_sm_email, p_malades_dict))
    
    return json.dumps(notif_dict)

def notify_personne(notification_id, notif_sms, notif_email, personnes_dict):
    notif_dict = []
    # 2. pour chaque (1), selectionner les personnes avec qui il a été en "contact"
    for p in personnes_dict:
        
        # 3. pour chaque (2), ...
        crp_dict = CRP().get_personnes_crp(p.p_id)
        
        print("=> crp_dict => ", crp_dict)
        
        for crp in crp_dict:
            
            # 3.1. envoyer un message pour le notifier 
            p_notif = cm.NOTIF.format(p.p_nom +" "+ p.p_prenom, p.date_test, crp.relation, crp.nom +" "+ crp.prenom)
            #print (p_notif)
            
            # si un numéro de téléphone, un sms est envoyé
            if crp.num_telephone is not None and crp.num_telephone != "":
                notif_ = param_notif(notif_sms, crp, p)
                #print(notif_)
                cm.write_file(path_sms + str(crp.id) + ".txt", notif_)
            
            # si une @mail est rensigné, un email est envoyé
            if crp.email is not None and crp.email != "":
                notif_ = param_notif(notif_email, crp, p)
                #print("email\n : " + notif_)
                cm.write_file(path_email + str(crp.id) + ".html", notif_)
                # envoie du mail
                cm.send_email(crp.email, notif_)
            
            # 3.2. + enregistrement de la notification en base 
            pnotif = TPNotification(notification_id, crp.id, p.p_id, p_notif, cm.get_current_date_fr(), cm.get_current_timestamp())
            id_notif = PNotification().add(pnotif)
            
            # ajout de l'id de la nouvelle notification personne
            notif_dict.append(id_notif)
    
    return notif_dict
