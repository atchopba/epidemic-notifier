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
from treatment.personne import RPersonne
import sqlite3

TCRP = namedtuple("TCRP", "personne_id_1 personne_id_2 relation_id date_contact heure_contact")
RCRP = namedtuple("RCRP", "id personne_id_1 personne_id_2 relation_id date_contact heure_contact")

class CRP(DB):
    
    def add(self, crp, autocommit = True):
        r = ("INSERT INTO contact_relation_personnes "
             "(personne_id_1, personne_id_2, relation_id, date_contact, heure_contact) "
             "VALUES "
             "(?, ?, ?, ?, ?)")
        try:
            self.conn.execute(r, crp)
            if autocommit:
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
    
    
    def delete(self, id):
        self.conn.execute("DELETE FROM contact_relation_personnes WHERE id=?", str(id))
        self.conn.commit()
        return True
    
    def delete_due_2_personne(self, id_personne):
        r = ("DELETE FROM contact_relation_personnes WHERE personne_id_1=? or "
             "personne_id_2=?")
        self.conn.execute(r, str(id_personne), str(id_personne))
        self.conn.commit()
        return True

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
