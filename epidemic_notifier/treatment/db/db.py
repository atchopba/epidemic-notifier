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
from flask import current_app

class DB(object):
    
    def __init__(self):
        _config = current_app.config
        if _config.get("MULTI_DATABASE"):
            DB_EPIDEMIC = _config.get("DATABASE_CLIENT") if not _config.get("DATABASE_CLIENT") is None else _config.get("DATABASE_URI")
        else:
            DB_EPIDEMIC = _config.get("DATABASE_URI")
        self.conn = sqlite3.connect(DB_EPIDEMIC)
        self.cur = self.conn.cursor()   

    def create_db(self):
        self.create_table_relations()
        self.create_table_personnes()
        self.create_table_type_consultations()
        self.create_table_symptomes()
        self.create_table_personne_consultations()
        self.create_table_personne_vie_conditions()
        self.create_table_personne_diagnostics()
        self.create_table_test_types()
        self.create_table_test_lieux()
        self.create_table_guerison_types()
        self.create_table_personne_guerisons()
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
        self.cur.execute("INSERT INTO relations (libelle) VALUES ('collègue')")
        self.cur.execute("INSERT INTO relations (libelle) VALUES ('famille')")
        self.cur.execute("INSERT INTO relations (libelle) VALUES ('hôpital')")
        self.cur.execute("INSERT INTO relations (libelle) VALUES ('quartier')")
        self.cur.execute("INSERT INTO relations (libelle) VALUES ('voisin')")
        self.conn.commit()
        
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
    
    def create_table_personne_vie_conditions(self):
        self.cur.execute("DROP TABLE IF EXISTS personne_vie_conditions")
        self.cur.execute(''' CREATE TABLE personne_vie_conditions (
            id integer PRIMARY KEY,    
            personne_id integer UNIQUE,
            is_en_couple text DEFAULT 'non',
            has_enfant text DEFAULT 'non',
            nb_enfant int DEFAULT 0,
            has_personne_agee text DEFAULT 'non',
            nb_personne_agee int DEFAULT 0,
            has_been_in_contact_personne_risque text DEFAULT 'non',
            has_possibilite_isolement text DEFAULT 'non',
            date_edit text
            )''')
        
    def create_table_symptomes(self):
        self.cur.execute("DROP TABLE IF EXISTS symptomes")
        self.cur.execute(''' CREATE TABLE symptomes (
            id integer PRIMARY KEY,    
            libelle text UNIQUE,
            gravite text DEFAULT 'non',
            score NUMERIC(1, 7)
            )''')
        # symptômes graves
        self.cur.execute("INSERT INTO symptomes (libelle, gravite, score) VALUES ('essouflement / difficultés à respirer', 'high', '0.2')")
        self.cur.execute("INSERT INTO symptomes (libelle, gravite, score) VALUES ('sensations d''oppression / douleur au niveau de la poitrine', 'high', '0.2')")
        self.cur.execute("INSERT INTO symptomes (libelle, gravite, score) VALUES ('perte d''élocution / perte de motricité', 'high', '0.2')")
        # symptômes fréquents
        self.cur.execute("INSERT INTO symptomes (libelle, gravite, score) VALUES ('fièvre', 'med', '0.075')")
        self.cur.execute("INSERT INTO symptomes (libelle, gravite, score) VALUES ('toux sèche', 'med', '0.075')")
        self.cur.execute("INSERT INTO symptomes (libelle, gravite, score) VALUES ('fatigue', 'med', '0.075')")
        # symptômes moins fréquents
        self.cur.execute("INSERT INTO symptomes (libelle, gravite, score) VALUES ('courbatures', 'low', '0.021875')")
        self.cur.execute("INSERT INTO symptomes (libelle, gravite, score) VALUES ('maux de gorge', 'low', '0.021875')")
        self.cur.execute("INSERT INTO symptomes (libelle, gravite, score) VALUES ('diarrhée', 'low', '0.021875')")
        self.cur.execute("INSERT INTO symptomes (libelle, gravite, score) VALUES ('conjonctivite', 'low', '0.021875')")
        self.cur.execute("INSERT INTO symptomes (libelle, gravite, score) VALUES ('maux de tête', 'low', '0.021875')")
        self.cur.execute("INSERT INTO symptomes (libelle, gravite, score) VALUES ('perte de l''ordorat ou du goût', 'low', '0.021875')")
        self.cur.execute("INSERT INTO symptomes (libelle, gravite, score) VALUES ('éruption cutanée', 'low', '0.021875')")
        self.cur.execute("INSERT INTO symptomes (libelle, gravite, score) VALUES ('décoloration des doigts/orteils', 'low', '0.021875')")
        self.conn.commit()
        
    def create_table_personne_diagnostics(self):
        self.cur.execute("DROP TABLE IF EXISTS personne_diagnostics")
        self.cur.execute(''' CREATE TABLE personne_diagnostics (
            id integer PRIMARY KEY,    
            personne_id integer,
            date_debut text,
            symptome_id_1 integer,
            symptome_id_2 integer,
            symptome_id_3 integer,
            symptome_id_4 integer,
            symptome_id_5 integer,
            calcul_score NUMERIC(1, 10),
            date_edit text
            )''')
    
    def create_table_type_consultations(self):
        # relation
        self.cur.execute("DROP TABLE IF EXISTS type_consultations")
        self.cur.execute(''' CREATE TABLE type_consultations ( 
            id integer PRIMARY KEY,    
            libelle text UNIQUE
            )''')
        self.cur.execute("INSERT INTO type_consultations (libelle) VALUES ('cabinet')")
        self.cur.execute("INSERT INTO type_consultations (libelle) VALUES ('centre médical')")
        self.cur.execute("INSERT INTO type_consultations (libelle) VALUES ('télé-consultation')")
        self.conn.commit()
    
    def create_table_personne_consultations(self):
        self.cur.execute("DROP TABLE IF EXISTS personne_consultations")
        self.cur.execute(''' CREATE TABLE personne_consultations (
            id integer PRIMARY KEY,    
            type_consultation_id integer,
            personne_id integer,
            date_consultation string,
            heure_consultation string,
            date_edit text
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
     
    def create_table_test_types(self):
        # test
        self.cur.execute("DROP TABLE IF EXISTS test_types")
        self.cur.execute(''' CREATE TABLE test_types (
            id integer PRIMARY KEY,    
            libelle string
            )''')
        self.cur.execute("INSERT INTO test_types (libelle) VALUES ('scanner/radio')")
        self.cur.execute("INSERT INTO test_types (libelle) VALUES ('test naso-pharingé')")
        self.cur.execute("INSERT INTO test_types (libelle) VALUES ('test salivaire')")
        self.cur.execute("INSERT INTO test_types (libelle) VALUES ('test sérologique')")
        self.conn.commit()
    
    def create_table_test_lieux(self):
        self.cur.execute("DROP TABLE IF EXISTS test_lieux")
        self.cur.execute(''' CREATE TABLE test_lieux (
            id integer PRIMARY KEY,    
            libelle string
            )''')
        self.cur.execute("INSERT INTO test_lieux (libelle) VALUES ('centre de santé')")
        self.cur.execute("INSERT INTO test_lieux (libelle) VALUES ('laboratoire')")
        self.cur.execute("INSERT INTO test_lieux (libelle) VALUES ('lieu agrée')")
        self.conn.commit()
        
    def create_table_tests(self):
        # test
        self.cur.execute("DROP TABLE IF EXISTS tests")
        self.cur.execute(''' CREATE TABLE tests (
            id integer PRIMARY KEY,  
            personne_id integer,
            test_type_id_1 integer,
            test_type_id_2 integer,
            test_type_id_3 integer,
            test_type_id_4 integer,
            test_lieu_id integer,
            adresse_lieu_test text,
            date_test text,
            heure_test text,
            date_resultat text,
            heure_resultat text,
            commentaires text,
            resultat integer
            )''')
        
    def create_table_guerison_types(self):
        self.cur.execute("DROP TABLE IF EXISTS guerison_types")
        self.cur.execute(''' CREATE TABLE guerison_types (
            id integer PRIMARY KEY,  
            libelle text)''')
        self.cur.execute("INSERT INTO guerison_types (libelle) VALUES ('biologique')")
        self.cur.execute("INSERT INTO guerison_types (libelle) VALUES ('clinique')")
        self.cur.execute("INSERT INTO guerison_types (libelle) VALUES ('scannographique')")
        self.conn.commit()
    
    def create_table_personne_guerisons(self):
        self.cur.execute("DROP TABLE IF EXISTS personne_guerisons")
        self.cur.execute(''' CREATE TABLE personne_guerisons (
            id integer PRIMARY KEY,  
            personne_id integer,
            guerison_id integer,
            date_guerison text,
            has_been_isole text DEFAULT 'non',
            has_been_sous_oxygene text DEFAULT 'non',
            has_been_sous_antibiotique DEFAULT 'non',
            has_been_hospitalise text DEFAULY 'non',
            has_scanner_controle text DEFAULT 'non',
            date_edit text
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
            texte text,
            date_ text,
            heure_ text
            )''')
        
    def create_table_users(self):
        # notification
        self.cur.execute("DROP TABLE IF EXISTS users")
        self.cur.execute(''' CREATE TABLE users (
            id integer PRIMARY KEY,
            login text,
            mdp text,
            name text,
            email text UNIQUE,
            profil text,
            is_authenticated integer DEFAULT 1,
            is_active integer DEFAULT 1,
            is_anonymous integer DEFAULT 0,
            db text
            )''')
        self.cur.execute("insert into users(login, mdp, name, profil, email, db) values('medec1','medec1','medec1', 'medecin', 'medec1@hopital.fr', './epidemic_notifier/static/data/epidemic-c1.db')")
        self.cur.execute("insert into users(login, mdp, name, profil, email, db) values('medec2','medec2','medec2', 'medecin', 'medec2@hopital.fr', './epidemic_notifier/static/data/epidemic-c2.db')")
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
        