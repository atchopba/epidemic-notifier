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

TPVCondition = namedtuple("TPVCondition", "personne_id is_en_couple has_enfant nb_enfant has_personne_agee nb_personne_agee has_possibilite_isolement has_been_in_contact_personne_risque date_edit")
RPVCondition = namedtuple("RPVCondition", "id personne_id is_en_couple has_enfant nb_enfant has_personne_agee nb_personne_agee has_possibilite_isolement has_been_in_contact_personne_risque date_edit")

class PVCondition(DB):
    
    def add(self, pvcondition):
        r = (''' INSERT INTO personne_vie_conditions 
             (personne_id, is_en_couple, has_enfant, nb_enfant, has_personne_agee, nb_personne_agee, has_possibilite_isolement, has_been_in_contact_personne_risque, date_edit) 
             VALUES 
             (?, ?, ?, ?, ?, ?, ?, ?, ?) ''')
        try:
            self.conn.execute(r, pvcondition)
            self.conn.commit()
            return self.get_last_row_id("personne_vie_conditions")
        except sqlite3.IntegrityError:
            return None
    
    def get_by_personne_id(self, personne_id):
        r = "SELECT * FROM personne_vie_conditions WHERE personne_id={}".format(personne_id)
        self.cur.execute(r)
        rows = self.cur.fetchall()
        return [RPVCondition(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]) for row in rows]
    
    def get_all(self):
        self.cur.execute("SELECT * FROM personne_vie_conditions")
        rows = self.cur.fetchall()
        return [RPVCondition(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]) for row in rows]

    def delete(self, personne_id):
        return super().delete("personne_vie_conditions", personne_id)
