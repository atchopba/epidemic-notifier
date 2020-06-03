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
from epidemic_notifier.treatment.db.db import DB

RTLieu = namedtuple("RTLieu", "id libelle")

class TestLieu(DB):
    
    def get_all(self):
        self.cur.execute("SELECT  * FROM test_lieux ORDER BY id ASC")
        rows = self.cur.fetchall()
        return [RTLieu(row[0], row[1]) for row in rows] 
