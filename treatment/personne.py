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
from treatment.db import DB
import sqlite3

TPersonne = namedtuple("TPersonne", "nom prenom date_naiss num_telephone email")
RPersonne = namedtuple("RPersonne", "id nom prenom date_naiss num_telephone email")

class Personne(DB):
    
    def add(self, personne):
        r = ("INSERT INTO personnes "
             "(nom, prenom, date_naiss, num_telephone, email) VALUES "
             "(?, ?, ?, ?, ?)")
        try:
            self.conn.execute(r, personne)
            self.conn.commit()
            return self.get_last_row_id("personnes")
        except sqlite3.IntegrityError as ie:
            print("=> Personne => add => ", ie)
            return None
        
    def get_one(self, id):
        self.cur.execute("SELECT  * FROM personnes WHERE id=? ORDER BY id ASC", id)
        row = self.cur.fetchone()
        if (row != None):
            return RPersonne(str(row[0]), row[1], row[2], row[3], row[4], row[5])
        return None
        
    def get_all(self):
        self.cur.execute("SELECT  * FROM personnes ORDER BY id ASC")
        rows = self.cur.fetchall()
        return [RPersonne(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]
    
    def delete(self, id):
        deleted = self.conn.execute("DELETE FROM personnes WHERE id=?", str(id))
        self.conn.commit()
        return deleted
