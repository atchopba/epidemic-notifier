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
from epidemic_notifier.core.db.db import DB, ACTION_DELETE, ACTION_INSERT, ACTION_LIST
from config import Config
import sqlite3

TPDiagnostic = namedtuple("TPDiagnostic", "personne_id date_debut symptome_id_1 symptome_id_2 symptome_id_3 symptome_id_4 symptome_id_5 calcul_score date_edit")
RPDiagnostic = namedtuple("RPDiagnostic", "id personne_id date_debut symptome_id_1 symptome_id_2 symptome_id_3 symptome_id_4 symptome_id_5 calcul_score date_edit")

class PDiagnostic(DB):
    
    ACTION_INSERT = ACTION_INSERT + "personne_diagnostic"
    ACTION_DELETE = ACTION_DELETE + "personne_diagnostic"
    ACTION_LIST = ACTION_LIST + "personne_diagnostic"
    
    def add(self, pdiagnostic):
        r = ('''INSERT INTO personne_diagnostics 
             (personne_id, date_debut, symptome_id_1, symptome_id_2, symptome_id_3, symptome_id_4, symptome_id_5, calcul_score, date_edit) VALUES 
             (?, ?, ?, ?, ?, ?, ?, ?, ?)''')
        try:
            self.conn.execute(r, pdiagnostic)
            self.conn.commit()
            return self.get_last_row_id("personne_diagnostics")
        except sqlite3.IntegrityError:
            return None
    
    def get_one(self, id_):
        self.cur.execute("SELECT  * FROM personne_diagnostics WHERE id=? ORDER BY id DESC", str(id_))
        row = self.cur.fetchone()
        if (row != None):
            return RPDiagnostic(str(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
        return None
    
    def get_last_by_personne(self, personne_id):
        self.cur.execute("SELECT  * FROM personne_diagnostics WHERE personne_id=? ORDER BY id DESC", str(personne_id))
        row = self.cur.fetchone()
        if (row != None):
            return RPDiagnostic(str(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
        return None
    
    def get_personne_diagnostic_prop(self, personne_id):
        DiagProp = namedtuple("DiagProp", "presente_signe suspect")
        pd = self.get_last_by_personne(personne_id)
        presente_signe = "oui" if pd is not None else "non"
        suspect = "oui" if pd is not None and pd.calcul_score >= Config.SUSPECT_SCORE_MIN else "non"
        return DiagProp(presente_signe, suspect)   
    
    def get_all(self):
        self.cur.execute("SELECT  * FROM personne_diagnostics ORDER BY id ASC")
        rows = self.cur.fetchall()
        return [RPDiagnostic(str(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]) for row in rows]
    
    def get_by_personne_id(self, personne_id):
        r = (''' 
             SELECT pd.id, pd.personne_id, pd.date_debut, s1.libelle, s2.libelle, s3.libelle, s4.libelle, s5.libelle, pd.calcul_score, date_edit
             FROM personne_diagnostics pd
             LEFT JOIN symptomes s1 ON pd.symptome_id_1 = s1.id 
             LEFT JOIN symptomes s2 ON pd.symptome_id_2 = s2.id 
             LEFT JOIN symptomes s3 ON pd.symptome_id_3 = s3.id 
             LEFT JOIN symptomes s4 ON pd.symptome_id_4 = s4.id 
             LEFT JOIN symptomes s5 ON pd.symptome_id_5 = s5.id 
             WHERE pd.personne_id={}
             ''').format(personne_id)
        self.cur.execute(r)
        rows = self.cur.fetchall()
        return [RPDiagnostic(str(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]) for row in rows]
    
    def delete(self, pd_id):
        return super().delete("personne_diagnostics", pd_id)
