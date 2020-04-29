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
RTest = namedtuple("RTest", "id p_id p_nom p_prenom date_test heure_test date_resultat heure_resultat resultat")

POSITIF = "1"

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
        self.cur.execute("SELECT  * FROM tests WHERE id=? ORDER BY id ASC", str(id_))
        row = self.cur.fetchone()
        if (row != None):
            return RTest(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        return None
        
    def get_all(self, resultat=None):
        if resultat is None:
            r = ("SELECT t.id, p.id, p.nom, p.prenom, t.date_test, t.heure_test, t.date_resultat, t.heure_resultat, t.resultat "
                "FROM tests t "
                "JOIN personnes p ON p.id = t.personne_id "
                "ORDER BY t.id ASC")
            self.cur.execute(r)
        else:
            r = ("SELECT t.id, p.id, p.nom, p.prenom, t.date_test, t.heure_test, t.date_resultat, t.heure_resultat, t.resultat "
                "FROM tests t "
                "JOIN personnes p ON p.id = t.personne_id "
                "WHERE t.resultat = ?"
                "ORDER BY t.id ASC")
            self.cur.execute(r, resultat)
        rows = self.cur.fetchall()
        return [RTest(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], str(row[8])) for row in rows]
    
    def delete(self, id_):
        return super().delete("tests", id_)
    