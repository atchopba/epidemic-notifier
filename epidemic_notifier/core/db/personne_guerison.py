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
from epidemic_notifier.core.db.personne_diagnostic import PDiagnostic
from epidemic_notifier.core.db.personne_consultation import PConsultation
import sqlite3

TPGuerison = namedtuple("TPGuerison", "personne_id guerison_id date_guerison has_been_isole has_been_sous_oxygene has_been_sous_antibiotique has_been_hospitalise has_scanner_controle date_edit")
RPGuerison = namedtuple("RPGuerison", "id personne_id guerison_id date_guerison has_been_isole has_been_sous_oxygene has_been_sous_antibiotique has_been_hospitalise has_scanner_controle date_edit")

RPersonneGuerison = namedtuple("RPersonneGuerison", "id p_nom p_prenom presente_signe suspect consulte")

DEFAULT_OUI = "oui"
DEFAULT_NON = "non"

class PGuerison(DB):
    
    ACTION_INSERT = ACTION_INSERT + "personne_guerison"
    ACTION_DELETE = ACTION_DELETE + "personne_guerison"
    ACTION_LIST = ACTION_LIST + "personne_guerison"
    
    def add(self, pguerison):
        r = (''' INSERT INTO personne_guerisons 
             (personne_id, guerison_id, date_guerison, has_been_isole, has_been_sous_oxygene, has_been_sous_antibiotique, has_been_hospitalise, has_scanner_controle, date_edit) 
             VALUES 
             (?, ?, ?, ?, ?, ?, ?, ?, ?) ''')
        try:
            self.conn.execute(r, pguerison)
            self.conn.commit()
            return self.get_last_row_id("personne_guerisons")
        except sqlite3.IntegrityError:
            return None
    
    def get_by_personne_id(self, personne_id):
        r = "SELECT * FROM personne_guerisons WHERE personne_id={}".format(personne_id)
        self.cur.execute(r)
        rows = self.cur.fetchall()
        return [RPGuerison(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]) for row in rows]
    
    def get_all(self):
        r = (''' SELECT pg.id id, p.id p_id, p.nom p_nom, p.prenom p_prenom /*, pc.id pc_id */
             FROM personne_guerisons pg 
             LEFT JOIN personnes p ON p.id = pg.personne_id 
             /* LEFT JOIN personne_diagnostics pd ON pd.personne_id = p.id */
             /* LEFT JOIN personne_consultations pc ON pc.personne_id = p.id */
             ''')
        self.cur.execute(r)
        rows = self.cur.fetchall()
        pg_dict = []
        for row in rows:
            diag_prop = PDiagnostic().get_personne_diagnostic_prop(row[1])
            p_consult = PConsultation().get_one(row[1])
            pg_dict.append(RPersonneGuerison(row[0], row[2], row[3], diag_prop.presente_signe, diag_prop.suspect, DEFAULT_OUI if p_consult[0] is not None else DEFAULT_NON))
        return pg_dict

    def delete(self, pg_id):
        return super().delete("personne_guerisons", pg_id)
