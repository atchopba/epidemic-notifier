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
from epidemic_notifier.treatment import common as cm
import sqlite3

TNotification = namedtuple("TNotification", "date_ heure_")
RNotification = namedtuple("RNotification", "id date_ heure_")

class Notification(DB):
    
    def add(self):
        r = ("INSERT INTO notifications "
             "(date_, heure_) "
             "VALUES (?, ?)")
        try:
            self.conn.execute(r, (cm.get_current_date_fr(), cm.get_current_timestamp()))
            self.conn.commit()
            return self.get_last_row_id("notifications")
        except sqlite3.IntegrityError:
            return None
        
    def get_one(self, id_):
        self.cur.execute("SELECT  * FROM notifications WHERE id=? ORDER BY id ASC", str(id_))
        row = self.cur.fetchone()
        if (row != None):
            return RNotification(row[0], row[1])
        return None
        
    def get_all(self):
        self.cur.execute("SELECT  * FROM notifications ORDER BY id ASC")
        rows = self.cur.fetchall()
        return [RNotification(row[0], row[1], row[2]) for row in rows]
    
    def delete(self, id_):
        return super().delete("notifications", id_)
