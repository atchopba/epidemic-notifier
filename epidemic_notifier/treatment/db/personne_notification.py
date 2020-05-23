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

from collections import namedtuple
from epidemic_notifier.treatment.db.db import DB
from epidemic_notifier.treatment.db.notification import Notification
import sqlite3

TPNotification = namedtuple("TPNotification", "notification_id personne_id personne_id_due texte date_ heure_")
RPNotification = namedtuple("RPNotification", "id notification_id personne_id personne_id_due texte date_ heure_")
RPNNotification = namedtuple("RPNNotification", "id date_ heure_ nb_notifies")

class PNotification(DB):
    
    def add(self, pnotification):
        r = ("INSERT INTO personne_notifications "
             "(notification_id, personne_id, personne_id_due, texte, date_, heure_) "
             "VALUES (?, ?, ?, ?, ?, ?)")
        try:
            self.conn.execute(r, pnotification)
            self.conn.commit()
            return self.get_last_row_id("personne_notifications")
        except sqlite3.IntegrityError:
            return None
        
    def get_one(self, id_):
        self.cur.execute("SELECT  * FROM personne_notifications WHERE id=? ORDER BY id ASC", id_)
        row = self.cur.fetchone()
        if (row != None):
            return RPNotification(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        return None
        
    def get_all(self):
        self.cur.execute("SELECT  * FROM personne_notifications ORDER BY id ASC")
        rows = self.cur.fetchall()
        return [RPNotification(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows]
    
    def delete(self, id_):
        return super().delete("_personne_notifications", id_)
    
    def get_notification_nb_pnotification(self, notification_id):
        r = "SELECT COUNT(*) FROM personne_notifications WHERE notification_id={}".format(notification_id) #?"
        self.cur.execute(r)#, str(notification_id))
        row = self.cur.fetchone()
        return row[0]
    
    def get_notification_pnotifications(self, notification_id=None):
        notifications = Notification().get_all() if notification_id is None else [Notification().get_one(notification_id)]
        n_dict = []
        for n in notifications:
            n_pn = RPNNotification(n.id, n.date_, n.heure_, self.get_notification_nb_pnotification(n.id))
            n_dict.append(n_pn)
        return n_dict
    