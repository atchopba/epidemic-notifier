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
from treatment.db.db import DB
import sqlite3

TPNotification = namedtuple("TPNotification", "notification_id personne_id personne_id_due texte date_ heure_")
RPNotification = namedtuple("RPNotification", "id notification_id personne_id personne_id_due texte date_ heure_")

class PNotification(DB):
    
    def add(self, pnotification):
        r = ("INSERT INTO personne_notifications "
             "(pnotification_id, personne_id, personne_id_due, texte, date_, heure_) "
             "VALUES (?, ?, ?, ?, ?, ?)")
        try:
            self.conn.execute(r, pnotification)
            self.conn.commit()
            return self.get_last_row_id("personne_notifications")
        except sqlite3.IntegrityError:
            return None
        
    def get_one(self, id):
        self.cur.execute("SELECT  * FROM personne_notifications WHERE id=? ORDER BY id ASC", id)
        row = self.cur.fetchone()
        if (row != None):
            return RPNotification(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        return None
        
    def get_all(self):
        self.cur.execute("SELECT  * FROM personne_notifications ORDER BY id ASC")
        rows = self.cur.fetchall()
        return [RPNotification(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows]