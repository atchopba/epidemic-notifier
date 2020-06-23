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
from epidemic_notifier.core.db.db import DB
import sqlite3

TUserHistorique = namedtuple("TUserHistorique", "user_id personne_id action date_edit heure_edit")
RUserHistorique = namedtuple("RUserHistorique", "id user_id personne_id action date_edit heure_edit")

class UserHistorique(DB):
    
    def add(self, ruhistorique):
        r = ('''INSERT INTO user_historiques 
             (user_id, personne_id, action, date_edit, heure_edit) 
             VALUES (?, ?, ?, ?, ?)''')
        try:
            self.conn.execute(r, ruhistorique)
            self.conn.commit()
            return self.get_last_row_id("user_historiques")
        except sqlite3.IntegrityError:
            return None
        
    def get_one(self, id_):
        self.cur.execute("SELECT  * FROM user_historiques WHERE id=? ORDER BY id ASC", id_)
        row = self.cur.fetchone()
        if (row != None):
            return RUserHistorique(row[0], row[1], row[2], row[3], row[4], row[5])
        return None
        
    def get_all(self):
        self.cur.execute("SELECT  * FROM user_historiques ORDER BY id ASC")
        rows = self.cur.fetchall()
        return [RUserHistorique(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]
    
    def delete(self, id_):
        return super().delete("user_historiques", id_)
