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


def notifier_personne(notification_id):
    # 1. selectionner les personnes avec le test positifs
    personnes_dict = Test().get_all("1")

    print("=> personnes_dict => ", personnes_dict)

    # 2. pour chaque (1), selectionner les personnes avec qui il a été en "contact"
    for p in personnes_dict:
        
        # 3. pour chaque (2), ...
        crp_dict = CRP().get_personnes_crp(p.p_id)
        
        print("=> crp_dict => ", crp_dict)
        
        for crp in crp_dict:
            print()
            # 3.1. envoyer un message pour le notifier 
            p_notif = cm.NOTIF.format(p.p_nom +" "+ p.p_prenom, p.date_test, crp.relation, crp.nom +" "+ crp.prenom)
            print (p_notif)
            
            # https://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python
            
            # 3.2. + enregistrement de la notification en base 
            pnotif = TPNotification(notification_id, crp.id, p.p_id, p_notif, cm.get_current_date(), cm.get_current_time())
            PNotification().add(pnotif)
            