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

TPConsultation = namedtuple("TPConsultation", "type_consultation_id personne_id date_consultation heure_consultation date_edit")
RPConsultation = namedtuple("RPConsultation", "id type_consultation_id type_consultation_lib personne_id date_consultation heure_consultation date_edit")

class PConsultation(DB):
    
    def add(self, pconsultation):
        r = ('''INSERT INTO personne_consultations 
             (type_consultation_id, personne_id, date_consultation, heure_consultation, date_edit) VALUES 
             (?, ?, ?, ?, ?)''')
        try:
            self.conn.execute(r, pconsultation)
            self.conn.commit()
            return self.get_last_row_id("personne_consultations")
        except sqlite3.IntegrityError:
            return None
    
    def get_one(self, id_):
        self.cur.execute("SELECT  * FROM personne_consultations WHERE id=? ORDER BY id ASC", str(id_))
        row = self.cur.fetchone()
        if (row != None):
            return RPConsultation(str(row[0]), row[1], "", row[2], row[3], row[4], row[5])
        return None
    
    def get_all(self):
        self.cur.execute("SELECT  * FROM personne_consultations ORDER BY id ASC")
        rows = self.cur.fetchall()
        return [RPConsultation(row[0], row[1], "", row[2], row[3], row[4], row[5]) for row in rows]
    
    def get_by_personne_id(self, personne_id):
        r = (''' 
             SELECT pc.id, pc.type_consultation_id, tc.libelle, pc.personne_id, pc.date_consultation, pc.heure_consultation, pc.date_edit 
             FROM personne_consultations pc
             JOIN type_consultations tc ON tc.id = pc.type_consultation_id 
             WHERE pc.personne_id={}
             ''').format(personne_id)
        self.cur.execute(r)
        rows = self.cur.fetchall()
        return [RPConsultation(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows]
    
    def delete(self, pc_id):
        return super().delete("personne_consultations", pc_id)
