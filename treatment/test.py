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
import sqlite3

TTest = namedtuple("TTest", "personne_id date_test heure_test date_resultat heure_resultat resultat")
RTest = namedtuple("RTest", "id personne_id date_test heure_test date_resultat heure_resultat resultat")

class Test(DB):
    
    def add(self, test):
        r = ("INSERT INTO test "
             "(personne_id, date_test, heure_test, date_resultat, heure_resultat, resultat) "
             "VALUES (?, ?, ?, ?, ?, ?)")
        try:
            self.conn.execute(r, test)
            self.conn.commit()
            return self.get_last_row_id("test")
        except sqlite3.IntegrityError:
            return None
        
    def get_one(self, id):
        self.cur.execute("SELECT  * FROM test WHERE id=? ORDER BY id ASC", id)
        row = self.cur.fetchone()
        if (row != None):
            return RTest(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        return None
        
    def get_all(self):
        self.cur.execute("SELECT  * FROM test ORDER BY id ASC")
        rows = self.cur.fetchall()
        return [RTest(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows]
    
    def delete(self, id):
        self.conn.execute("DELETE FROM relations WHERE id=?", str(id))
        self.conn.commit()
        return True