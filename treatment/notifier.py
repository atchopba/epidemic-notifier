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

from treatment import common as cm
from treatment.db.test import Test
from treatment.db.contact_relation_personne import CRP
from treatment.db.personne_notification import TPNotification, PNotification

import json


notif_sms = cm.load_file(cm.FILE_NOTIF_SMS)
notif_email = cm.load_file(cm.FILE_NOTIF_EMAIL)

path_root = "./__temp__/notif/"
path_sms = path_root + "sms/" + cm.get_current_date_en() + "/"
path_email = path_root + "email/" +cm.get_current_date_en() + "/"

cm.create_folder(path_sms)
cm.create_folder(path_email)


def notifier_personne(notification_id):
    
    notif_dict = []
    
    # 1. selectionner les personnes avec le test positifs
    personnes_dict = Test().get_all("1")

    print("=> personnes_dict => ", personnes_dict)

    # 2. pour chaque (1), selectionner les personnes avec qui il a été en "contact"
    for p in personnes_dict:
        
        # 3. pour chaque (2), ...
        crp_dict = CRP().get_personnes_crp(p.p_id)
        
        print("=> crp_dict => ", crp_dict)
        
        for crp in crp_dict:
            
            # 3.1. envoyer un message pour le notifier 
            p_notif = cm.NOTIF.format(p.p_nom +" "+ p.p_prenom, p.date_test, crp.relation, crp.nom +" "+ crp.prenom)
            print (p_notif)
            
            # si un numéro de téléphone, un sms est envoyé
            if crp.num_telephone is not None and crp.num_telephone != "":
                notif_ = notif_sms.format(p.p_nom +" "+ p.p_prenom, p.date_test, crp.relation, crp.nom +" "+ crp.prenom)
                print(notif_)
                cm.write_file(path_sms + str(crp.id) + ".txt", notif_)
            
            # si une @mail est rensigné, un email est envoyé
            if crp.email is not None and crp.email != "":
                notif_ = notif_email.format(p.p_nom +" "+ p.p_prenom, p.date_test, crp.relation, crp.nom +" "+ crp.prenom)
                cm.write_file(path_email + str(crp.id) + ".html", notif_)
                # envoie du mail
                cm.send_email(crp.email, notif_)
            
            # https://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python
            
            # 3.2. + enregistrement de la notification en base 
            pnotif = TPNotification(notification_id, crp.id, p.p_id, p_notif, cm.get_current_date_fr(), cm.get_current_time())
            id_notif = PNotification().add(pnotif)
            
            # ajout de l'id de la nouvelle notification personne
            notif_dict.append(id_notif)
    
    return json.dumps(notif_dict)
