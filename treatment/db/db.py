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

import sqlite3

DB_EPIDEMIC = "static/data/epidemic.db"

class DB(object):
    
    def __init__(self):
        self.conn = sqlite3.connect(DB_EPIDEMIC)
        self.cur = self.conn.cursor() 
        

    def create_db(self):
        self.create_table_relations()
        self.create_table_personnes
        self.create_table_crp()
        self.create_table_tests()
        self.create_table_notifications()
        self.create_table_personne_notifications()
        return True
    
    def create_table_relations(self):
        # relation
        self.cur.execute("DROP TABLE IF EXISTS relations")
        self.cur.execute(''' CREATE TABLE relations ( 
            id integer PRIMARY KEY,    
            libelle text UNIQUE
            )''')
        
    def create_table_personnes(self):
        self.cur.execute("DROP TABLE IF EXISTS personnes")
        self.cur.execute(''' CREATE TABLE personnes (
            id integer PRIMARY KEY,    
            nom text,
            prenom text,
            date_naiss text,
            num_telephone text,
            email text,
            UNIQUE (nom, prenom, date_naiss)
            )''')
        
    def create_table_crp(self):
        # relationship
        self.cur.execute("DROP TABLE IF EXISTS contact_relation_personnes")
        self.cur.execute(''' CREATE TABLE contact_relation_personnes (
            id integer PRIMARY KEY,    
            personne_id_1 integer,
            personne_id_2 integer,
            relation_id integer,
            date_contact string,
            heure_contact string,
            UNIQUE (personne_id_1, personne_id_2, relation_id, date_, heure_)
            )''')
        
    def create_table_tests(self):
        # test
        self.cur.execute("DROP TABLE IF EXISTS tests")
        self.cur.execute(''' CREATE TABLE tests (
            id integer PRIMARY KEY,    
            personne_id integer,
            date_test string,
            heure_test string,
            date_resultat string,
            heure_resultat string,
            resultat int
            )''')
     
    def create_table_notifications(self):
        # notification
        self.cur.execute("DROP TABLE IF EXISTS notifications")
        self.cur.execute(''' CREATE TABLE notifications (
            id integer PRIMARY KEY,
            date_ string,
            heure_ string
            )''')
        
    def create_table_personne_notifications(self):
        # notification
        self.cur.execute("DROP TABLE IF EXISTS personne_notifications")
        self.cur.execute(''' CREATE TABLE personne_notifications (
            id integer PRIMARY KEY,
            notification_id integer,
            personne_id integer,
            personne_id_due integer,
            texte string,
            date_ string,
            heure_ string
            )''')
    
    def get_last_row_id(self, table):
        cursor = self.cur.execute("SELECT max(id) FROM "+ table)
        return cursor.fetchone()[0]
    
    def delete_all(self, table):
        return self.cur.execute("DELETE FROM "+ table)
    
    def commit_trans(self):
        self.conn.commit()
        