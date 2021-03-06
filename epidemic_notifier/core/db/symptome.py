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
from epidemic_notifier.core.db.db import DB

RSymptome = namedtuple("RSymptome", "id libelle gravite score")

class Symptome(DB):
    
    def get_all(self):
        self.cur.execute("SELECT  * FROM symptomes ORDER BY id ASC")
        rows = self.cur.fetchall()
        return [RSymptome(row[0], row[1], row[2], row[3]) for row in rows] 
