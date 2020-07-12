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
from epidemic_notifier.core.db.personne_diagnostic import PDiagnostic
import sqlite3

TTest = namedtuple("TTest", "personne_id test_type_id_1 test_type_id_2 test_type_id_3 test_type_id_4 test_lieu_id adresse_lieu_test date_test heure_test date_resultat heure_resultat commentaires resultat date_edit")
RTest = namedtuple("RTest", "id personne_id p_nom p_prenom test_type_id_1 test_type_id_2 test_type_id_3 test_type_id_4 test_lieu_id adresse_lieu_test date_test heure_test date_resultat heure_resultat commentaires resultat date_edit presente_signe suspect gueri")

RTestPersonne = namedtuple("RTestPersonne", "p_id p_nom p_prenom p_date_naiss p_suspect t_id t_personne_id t_resultat")

class Test(DB):
    
    ACTION_INSERT = ACTION_INSERT + "test"
    ACTION_DELETE = ACTION_DELETE + "test"
    ACTION_LIST = ACTION_LIST + "test"
    
    def add(self, test):
        r = ('''INSERT INTO tests 
             (personne_id, test_type_id_1, test_type_id_2, test_type_id_3, test_type_id_4, test_lieu_id, adresse_lieu_test, date_test, heure_test, date_resultat, heure_resultat, commentaires, resultat, date_edit) 
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''')
        try:
            self.conn.execute(r, test)
            self.conn.commit()
            return self.get_last_row_id("tests")
        except sqlite3.IntegrityError:
            return None
    
    def get_one(self, id_):
        r = ('''SELECT SELECT t.id, p.id, p.nom, p.prenom, t1.libelle, t2.libelle, t3.libelle, t4.libelle, tl.libelle, t.adresse_lieu_test, t.date_test, t.heure_test, t.date_resultat, t.heure_resultat, t.commentaires, t.resultat, t.date_edit, pd.date_debut, pd.calcul_score, pg.date_guerison
            FROM tests t 
            JOIN personnes p ON p.id = t.personne_id 
            LEFT JOIN personne_guerisons pg ON pg.personne_id = p.id 
            LEFT JOIN test_lieux tl ON tl.id = t.test_lieu_id
            LEFT JOIN test_types t1 ON t1.id = t.test_type_id_1 
            LEFT JOIN test_types t2 ON t2.id = t.test_type_id_2 
            LEFT JOIN test_types t3 ON t3.id = t.test_type_id_3 
            LEFT JOIN test_types t4 ON t4.id = t.test_type_id_4 
            WHERE id=? 
            ORDER BY id ASC''').format(id_)
        self.cur.execute(r)
        row = self.cur.fetchone()
        if (row != None):
            return RTest(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
        return None
       
    def get_all(self):
        r = ('''SELECT t.id, p.id, p.nom, p.prenom, t1.libelle, t2.libelle, t3.libelle, t4.libelle, tl.libelle, t.adresse_lieu_test, t.date_test, t.heure_test, t.date_resultat, t.heure_resultat, t.commentaires, t.resultat, t.date_edit, pg.date_guerison
            FROM tests t 
            JOIN personnes p ON p.id = t.personne_id 
            LEFT JOIN personne_guerisons pg ON pg.personne_id = p.id 
            LEFT JOIN test_lieux tl ON tl.id = t.test_lieu_id
            LEFT JOIN test_types t1 ON t1.id = t.test_type_id_1 
            LEFT JOIN test_types t2 ON t2.id = t.test_type_id_2 
            LEFT JOIN test_types t3 ON t3.id = t.test_type_id_3 
            LEFT JOIN test_types t4 ON t4.id = t.test_type_id_4 
            ORDER BY t.id ASC''')
        self.cur.execute(r)
        rows = self.cur.fetchall()
        t_dict = []
        for row in rows:
            diag_prop = PDiagnostic().get_personne_diagnostic_prop(row[1])
            t_dict.append(RTest(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], diag_prop.presente_signe, diag_prop.suspect, 'oui' if row[17] is not None else 'non'))
        return t_dict
    
    def get_supposes_malades(self, score_min):
        r = ('''SELECT t.id, p.id, p.nom, p.prenom, pd.calcul_score, pg.date_guerison, t.test_type_id_1, t.date_test, t.heure_test, t.date_resultat, t.heure_resultat, t.resultat 
                FROM tests t 
                JOIN personnes p ON p.id = t.personne_id 
                LEFT JOIN personne_diagnostics pd ON pd.personne_id = p.id
                LEFT JOIN personne_guerisons pg ON pg.personne_id = p.id
                WHERE pd.calcul_score >= {}
                ORDER BY t.id ASC''').format(score_min)
        self.cur.execute(r)
        rows = self.cur.fetchall()
        return [RTest(row[0], row[1], row[2], row[3], 'oui' if row[4] is not None else 'non', 'oui' if row[5] is not None else 'non', row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18]) for row in rows]
    
    def get_malades(self):
        r = ('''SELECT t.id, p.id, p.nom, p.prenom, pd.calcul_score, pg.date_guerison, t.test_type_id_1, t.date_test, t.heure_test, t.date_resultat, t.heure_resultat, t.resultat 
                FROM tests t 
                JOIN personnes p ON p.id = t.personne_id 
                LEFT JOIN personne_diagnostics pd ON pd.personne_id = p.id
                LEFT JOIN personne_guerisons pg ON pg.personne_id = p.id
                WHERE t.resultat = 'oui'
                ORDER BY t.id ASC''')
        self.cur.execute(r)
        rows = self.cur.fetchall()
        return [RTest(row[0], row[1], row[2], row[3], 'oui' if row[4] is not None else 'non', 'oui' if row[5] is not None else 'non', row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18]) for row in rows]
        
    def find_for_graph(self):
        r = ('''SELECT p.id, p.nom, p.prenom, p.date_naiss, t.id, t.personne_id, t.resultat 
            FROM personnes p 
            LEFT JOIN tests t ON t.personne_id = p.id''')
        self.cur.execute(r)
        rows = self.cur.fetchall()
        t_dict = []
        for row in rows:
            diag_prop = PDiagnostic().get_personne_diagnostic_prop(row[0])
            t_dict.append(RTestPersonne(row[0], row[1], row[2], row[3], diag_prop.suspect, row[4], row[5], row[6]))
        return t_dict
    
    def delete(self, id_):
        return super().delete("tests", id_)

    def get_count(self):
        #return super().get_count("tests")
        r = "SELECT DISTINCT personne_id FROM tests"
        return self.get_count_r(r)
    
    def get_count_positif(self):
        r = "SELECT DISTINCT personne_id FROM tests WHERE resultat='oui'"
        return self.get_count_r(r)
    
    def get_count_negatif(self):
        r = "SELECT DISTINCT personne_id FROM tests WHERE resultat='non'"
        return self.get_count_r(r)
