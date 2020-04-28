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

TRelation = namedtuple("TRelation", "libelle")
RRelation = namedtuple("RRelation", "id libelle")

class Relation(DB):
    
    def add(self, relation):
        r = ("INSERT INTO relations "
             "(libelle) VALUES (?)")
        try:
            self.conn.execute(r, relation)
            self.conn.commit()
            return self.get_last_row_id("relations")
        except sqlite3.IntegrityError as ie:
            print("=> Relations => add => ", ie)
            return None
        
    def get_one(self, id_):
        self.cur.execute("SELECT  * FROM relations WHERE id=? ORDER BY id ASC", id_)
        row = self.cur.fetchone()
        if (row != None):
            return RRelation(row[0], row[1])
        return None
        
    def get_all(self):
        self.cur.execute("SELECT  * FROM relations ORDER BY id ASC")
        rows = self.cur.fetchall()
        return [RRelation(row[0], row[1]) for row in rows]
    
    def delete(self, id_):
        deleted = self.conn.execute("DELETE FROM relations WHERE id=?", str(id_))
        self.conn.commit()
        return deleted