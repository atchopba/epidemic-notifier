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
from config import Config

DB_EPIDEMIC = Config.DATABASE_URI

class DB(object):
    
    def __init__(self):
        self.conn = sqlite3.connect(DB_EPIDEMIC)
        self.cur = self.conn.cursor()   

    def create_db(self):
        self.create_table_relations()
        self.create_table_personnes()
        self.create_table_crp()
        self.create_table_tests()
        self.create_table_notifications()
        self.create_table_personne_notifications()
        self.create_table_users()
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
            suspect text,
            gueri text,
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
            UNIQUE (personne_id_1, personne_id_2, relation_id, date_contact, heure_contact)
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
        
    def create_table_users(self):
        # notification
        self.cur.execute("DROP TABLE IF EXISTS users")
        self.cur.execute(''' CREATE TABLE users (
            id integer PRIMARY KEY,
            login string,
            mdp string,
            name string,
            email string UNIQUE,
            profil string,
            is_authenticated integer DEFAULT 1,
            is_active integer DEFAULT 1,
            is_anonymous integer DEFAULT 0
            )''')
        self.cur.execute("insert into users(login, mdp, name, profil, email) values('medec1','medec1','medec1', 'medecin', 'medec1@hopital.fr')")
        self.conn.commit()
        self.cur.execute("insert into users(login, mdp, name, profil, email) values('medec2','medec2','medec2', 'medecin', 'medec2@hopital.fr')")
        self.conn.commit()
    
    def get_last_row_id(self, table_):
        cursor = self.cur.execute("SELECT max(id) FROM "+ table_)
        return cursor.fetchone()[0]
    
    def delete_all(self, table):
        return self.cur.execute("DELETE FROM "+ table)
    
    def delete(self, table_, id_):
        r = "DELETE FROM {} WHERE id={}".format(table_, id_)
        deleted = self.conn.execute(r)
        self.conn.commit()
        return deleted
    
    def get_count(self, table_):
        cursor = self.cur.execute("SELECT * FROM "+ table_)
        return len(cursor.fetchall()) 
    
    def get_count_r(self, r):
        cursor = self.cur.execute(r)
        return len(cursor.fetchall()) 
    
    def commit_trans(self):
        self.conn.commit()
        