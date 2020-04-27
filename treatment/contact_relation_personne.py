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
from treatment.personne import Personne, RPersonne
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
        
    def get_one(self, id):
        self.cur.execute("SELECT  * FROM contact_relation_personnes WHERE id=? ORDER BY id ASC", id)
        row = self.cur.fetchone()
        if (row != None):
            return RCRP(row[0], row[1], row[2], row[3], row[4], row[5])
        return None
        
    def get_all(self):
        self.cur.execute("SELECT  * FROM contact_relation_personnes ORDER BY id ASC")
        rows = self.cur.fetchall()
        return [RCRP(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]
    
    def get_personne_nb_contact(self, personne_id):
        r = "SELECT COUNT(*) FROM contact_relation_personnes WHERE personne_id_1=? OR personne_id_2=? LIMIT 1"
        self.cur.execute(r, (str(personne_id), str(personne_id)))
        row = self.cur.fetchone()
        return row[0]
    
    def delete(self, id):
        deleted = self.conn.execute("DELETE FROM contact_relation_personnes WHERE id=?", str(id))
        self.conn.commit()
        return deleted
    
    def delete_due_2_personne(self, id_personne):
        r = ("DELETE FROM contact_relation_personnes WHERE personne_id_1=? or "
             "personne_id_2=?")
        deleted = self.conn.execute(r, str(id_personne), str(id_personne))
        self.conn.commit()
        return deleted
    
    def get_personnes_crp(self, personne_id=None):
        personnes = Personne().get_all() if personne_id is None else [Personne().get_one(personne_id)]
        p_crp_dict = []
        for p in personnes:
            p_crp = RCRPPersonne(p.id, p.nom, p.prenom, p.date_naiss, p.num_telephone, p.email, self.get_personne_nb_contact(p.id))
            p_crp_dict.append(p_crp)
        return p_crp_dict
    
    def get_all_crp_with_id_personne(self, personne_id=None):
        r = ("SELECT p.id, p.nom, p.prenom, p.date_naiss, p.num_telephone, p.email, COUNT(crp.id) "
            "FROM contact_relation_personnes crp "
            "JOIN personnes p ON p.id = crp.personne_id_1 ")
        if personne_id is not None:
            r += "WHERE p.id=?"
            self.cur.execute(r, personne_id)
        else:
            self.cur.execute(r)
        rows = self.cur.fetchall()
        print("=> rows : ", rows)
        return [RCRPPersonne(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows]
        
    """
    def get_all_crp_with_id_personne(self, id_personne):
        #r = ("SELECT * FROM personnes WHERE id IN "
        #     "(SELECT personne_id_2 FROM contact_relation_personnes WHERE personne_id_1=?)")
        r = "SELECT DISTINCT personne_id_2 FROM contact_relation_personnes WHERE personne_id_1=?"
        self.cur.execute(r, id_personne)
        rows = self.cur.fetchall()
        if len(rows) > 0:
            #print("=> rows : ", rows)
            p_id_str = "','".join([str(row[0]) for row in rows])
            r = "SELECT * FROM personnes WHERE id IN ('"+ p_id_str +"')"
            #print("=> requete => ", r)
            self.cur.execute(r)
            rows = self.cur.fetchall()
            #
            if len(rows) > 0:
                #print("=> get_all_crp_with_id_personne : ", rows)
                return [RPersonne(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]
        return None
    """
