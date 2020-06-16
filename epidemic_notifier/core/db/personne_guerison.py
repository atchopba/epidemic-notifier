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

TPGuerison = namedtuple("TPGuerison", "personne_id guerison_id date_guerison has_been_isole has_been_sous_oxygene has_been_sous_antibiotique has_been_hospitalise has_scanner_controle date_edit")
RPGuerison = namedtuple("RPGuerison", "id personne_id guerison_id date_guerison has_been_isole has_been_sous_oxygene has_been_sous_antibiotique has_been_hospitalise has_scanner_controle date_edit")

class PGuerison(DB):
    
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
        self.cur.execute("SELECT * FROM personne_guerisons")
        rows = self.cur.fetchall()
        return [RPGuerison(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]) for row in rows]

    def delete(self, pg_id):
        return super().delete("personne_guerisons", pg_id)
