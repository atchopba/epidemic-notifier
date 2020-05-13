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
import sqlite3

TTest = namedtuple("TTest", "personne_id date_test heure_test date_resultat heure_resultat resultat")
RTest = namedtuple("RTest", "id p_id p_nom p_prenom p_suspect p_gueri date_test heure_test date_resultat heure_resultat resultat")


class Test(DB):
    
    def add(self, test):
        r = ("INSERT INTO tests "
             "(personne_id, date_test, heure_test, date_resultat, heure_resultat, resultat) "
             "VALUES (?, ?, ?, ?, ?, ?)")
        try:
            self.conn.execute(r, test)
            self.conn.commit()
            return self.get_last_row_id("tests")
        except sqlite3.IntegrityError:
            return None
        
    def get_one(self, id_):
        self.cur.execute("SELECT * FROM tests WHERE id=? ORDER BY id ASC", str(id_))
        row = self.cur.fetchone()
        if (row != None):
            return RTest(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        return None
       
    def get_all(self):
        r = ("SELECT t.id, p.id, p.nom, p.prenom, p.suspect, p.gueri, t.date_test, t.heure_test, t.date_resultat, t.heure_resultat, t.resultat "
            "FROM tests t "
            "JOIN personnes p ON p.id = t.personne_id "
            "ORDER BY t.id ASC")
        self.cur.execute(r)
        rows = self.cur.fetchall()
        return [RTest(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], str(row[10])) for row in rows]
    
    def get_supposes_malades(self):
        r = ("SELECT t.id, p.id, p.nom, p.prenom, p.suspect, p.gueri, t.date_test, t.heure_test, t.date_resultat, t.heure_resultat, t.resultat "
                "FROM tests t "
                "JOIN personnes p ON p.id = t.personne_id "
                "WHERE t.resultat = '1' "
                "ORDER BY t.id ASC")
        self.cur.execute(r)
        rows = self.cur.fetchall()
        return [RTest(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], str(row[10])) for row in rows]
    
    def delete(self, id_):
        return super().delete("tests", id_)

    def get_count(self):
        #return super().get_count("tests")
        r = "SELECT DISTINCT personne_id FROM tests"
        return self.get_count_r(r)
    
    def get_count_positif(self):
        r = "SELECT DISTINCT personne_id FROM tests WHERE resultat='1'"
        return self.get_count_r(r)
    
    def get_count_negatif(self):
        r = "SELECT DISTINCT personne_id FROM tests WHERE resultat='0'"
        return self.get_count_r(r)
