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
import sqlite3

TPersonne = namedtuple("TPersonne", "nom prenom date_naiss num_telephone email")
RPersonne = namedtuple("RPersonne", "id nom prenom date_naiss num_telephone email")

class Personne(DB):
    
    ACTION_INSERT = ACTION_INSERT + "personne"
    ACTION_DELETE = ACTION_DELETE + "personne"
    ACTION_LIST = ACTION_LIST + "personne"
    
    def add(self, personne):
        r = ('''INSERT INTO personnes 
             (nom, prenom, date_naiss, num_telephone, email) VALUES 
             (?, ?, ?, ?, ?)''')
        try:
            self.conn.execute(r, personne)
            self.conn.commit()
            return self.get_last_row_id("personnes")
        except sqlite3.IntegrityError:
            return None
    
    def get_one(self, id_):
        self.cur.execute("SELECT  * FROM personnes WHERE id=? ORDER BY id ASC", str(id_))
        row = self.cur.fetchone()
        if (row != None):
            return RPersonne(str(row[0]), row[1], row[2], row[3], row[4], row[5])
        return None
    
    def get_r_personne(self, rows):
       return [RPersonne(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows] 
    
    def get_all(self):
        self.cur.execute("SELECT  * FROM personnes ORDER BY id ASC")
        rows = self.cur.fetchall()
        return [RPersonne(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows] 
    
    def find_by_name(self, id_, name_):
        r = "SELECT * FROM personnes WHERE (nom LIKE '%{}%' OR prenom LIKE '%{}%') AND id is not {} ".format(name_, name_, id_)
        self.cur.execute(r)
        rows = self.cur.fetchall()
        return [RPersonne(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows] 
    
    def find_by_name_in_crp(self, id_, name_):
        r = (''' 
            SELECT * FROM personnes 
            WHERE (nom LIKE '%{}%' OR prenom LIKE '%{}%') AND id != '{}' and id not in
            (SELECT crp.personne_id_2 
            FROM personnes p
            JOIN contact_relation_personnes crp ON p.id = crp.personne_id_2
            WHERE crp.personne_id_1 = '{}' 
            UNION
            SELECT crp.personne_id_1 
            FROM personnes p
            JOIN contact_relation_personnes crp ON p.id = crp.personne_id_2
            WHERE crp.personne_id_2 = '{}')   
        ''').format(name_, name_, id_, id_, id_)
        self.cur.execute(r)
        rows = self.cur.fetchall()
        return [RPersonne(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows] 
    
    def delete(self, id_):
        return super().delete("personnes", id_)
    
    def get_count(self):
        return super().get_count("personnes")
    
    def get_count_suspect(self):
        r = "SELECT * FROM personnes WHERE suspect='1'"
        return self.get_count_r(r)
    
    def get_count_gueri(self):
        r = "SELECT * FROM personnes WHERE gueri IS NOT NULL or gueri=''"
        return self.get_count_r(r)
