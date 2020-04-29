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
from treatment.db.personne import Personne
import sqlite3

TCRP = namedtuple("TCRP", "personne_id_1 personne_id_2 relation_id date_contact heure_contact")
RCRP = namedtuple("RCRP", "id personne_id_1 personne_id_2 relation_id date_contact heure_contact")
RCRPPersonne = namedtuple("RCRPPersonne", "id nom prenom date_naiss num_telephone email nb_contact")

class CRP(DB):
    
    def add(self, crp):
        r = ("INSERT INTO contact_relation_personnes "
             "(personne_id_1, personne_id_2, relation_id, date_contact, heure_contact) "
             "VALUES "
             "(?, ?, ?, ?, ?)")
        try:
            self.conn.execute(r, crp)
            self.conn.commit()
            return self.get_last_row_id("contact_relation_personnes")
        except sqlite3.IntegrityError as ie:
            print("=> CRP => add => ", ie)
            return None
        
    def get_one(self, id_):
        self.cur.execute("SELECT  * FROM contact_relation_personnes WHERE id=? ORDER BY id ASC", str(id_))
        row = self.cur.fetchone()
        if (row != None):
            return RCRP(row[0], row[1], row[2], row[3], row[4], row[5])
        return None
        
    def get_all(self):
        self.cur.execute("SELECT  * FROM contact_relation_personnes ORDER BY id ASC")
        rows = self.cur.fetchall()
        return [RCRP(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]
    
    def delete(self, id_):
        return super().delete("contact_relation_personnes", id_)
    
    def delete_due_2_personne(self, id_personne):
        r = ("DELETE FROM contact_relation_personnes WHERE personne_id_1=? or "
             "personne_id_2=?")
        deleted = self.conn.execute(r, str(id_personne), str(id_personne))
        self.conn.commit()
        return deleted
    
    def get_personne_nb_contact(self, personne_id):
        r = "SELECT COUNT(*) FROM contact_relation_personnes WHERE personne_id_1=? OR personne_id_2=? LIMIT 1"
        self.cur.execute(r, (str(personne_id), str(personne_id)))
        row = self.cur.fetchone()
        return row[0]
    
    def get_personnes_crp(self, personne_id=None):
        personnes = Personne().get_all() if personne_id is None else [Personne().get_one(personne_id)]
        p_crp_dict = []
        for p in personnes:
            p_crp = RCRPPersonne(p.id, p.nom, p.prenom, p.date_naiss, p.num_telephone, p.email, self.get_personne_nb_contact(p.id))
            p_crp_dict.append(p_crp)
        return p_crp_dict
