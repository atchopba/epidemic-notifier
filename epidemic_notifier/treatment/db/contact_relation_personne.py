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
from epidemic_notifier.treatment.db.personne import Personne
import sqlite3

TCRP = namedtuple("TCRP", "personne_id_1 personne_id_2 relation_id date_contact heure_contact")
RCRP = namedtuple("RCRP", "id personne_id_1 personne_id_2 relation_id date_contact heure_contact")
RCRPPersonne = namedtuple("RCRPPersonne", "id nom prenom date_naiss num_telephone email relation nb_contact")

RCRPPersonneG = namedtuple("RCRPPersonneG", "id nom prenom date_naiss num_telephone email relation id_2 nom_2 prenom_2 nb_contact")

class CRP(DB):
    
    def add(self, crp):
        r = ('''INSERT INTO contact_relation_personnes 
             (personne_id_1, personne_id_2, relation_id, date_contact, heure_contact) 
             VALUES 
             (?, ?, ?, ?, ?)''')
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
    
    def delete_due_2_personne(self, personne_id):
        r = ("DELETE FROM contact_relation_personnes WHERE personne_id_1={} or "
             "personne_id_2={}").format(personne_id, personne_id)
        deleted = self.conn.execute(r)
        self.conn.commit()
        return deleted
    
    def get_personne_nb_contact(self, personne_id):
        r = "SELECT COUNT(*) FROM contact_relation_personnes WHERE personne_id_1=? OR personne_id_2=? LIMIT 1"
        self.cur.execute(r, (str(personne_id), str(personne_id)))
        row = self.cur.fetchone()
        return row[0]
    
    def get_personnes_crp(self, personne_id=None):
        if personne_id is None:
            personnes = Personne().get_all()
            p_crp_dict = []
            for p in personnes:
                p_crp = RCRPPersonne(p.id, p.nom, p.prenom, p.date_naiss, p.num_telephone, p.email, "", self.get_personne_nb_contact(p.id))
                p_crp_dict.append(p_crp)
            return p_crp_dict
        else:
            r = ('''
                SELECT p.id, p.nom, p.prenom, p.date_naiss, p.num_telephone, p.email, r.libelle
                FROM contact_relation_personnes crp 
                JOIN personnes p ON p.id = crp.personne_id_1 
                JOIN relations r on r.id = crp.relation_id 
                WHERE crp.personne_id_2 = ?
            ''')
            self.cur.execute(r, str(personne_id))
            rows_1 = self.cur.fetchall()
            #
            r = ('''
                SELECT p.id, p.nom, p.prenom, p.date_naiss, p.num_telephone, p.email, r.libelle
                FROM contact_relation_personnes crp 
                JOIN personnes p ON p.id = crp.personne_id_2 
                JOIN relations r on r.id = crp.relation_id 
                WHERE crp.personne_id_1 = ?
            ''')
            self.cur.execute(r, str(personne_id))
            rows_2 = self.cur.fetchall()
            #
            rows_1 += rows_2
            #
            return [RCRPPersonne(row[0], row[1], row[2], row[3], row[4], row[5], row[6], self.get_personne_nb_contact(row[0])) for row in rows_1]
        
    def find_for_graph(self):
        r = ('''
            SELECT 
            p_1.id, p_1.nom, p_1.prenom, p_1.date_naiss, p_1.num_telephone, p_1.email, crp.relation_id,
            p_2.id, p_2.nom, p_2.prenom 
            FROM contact_relation_personnes crp 
            JOIN personnes p_1 ON p_1.id = crp.personne_id_1
            JOIN personnes p_2 ON p_2.id = crp.personne_id_2         
        ''')
        self.cur.execute(r)
        rows = self.cur.fetchall()
        return [RCRPPersonneG(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], self.get_personne_nb_contact(row[0])) for row in rows]
