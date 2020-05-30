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
from .db import DB

TUser = namedtuple("TUser", "login mdp profil")
RUser = namedtuple("RUser", "id login mdp name profil email is_authenticated is_active is_anonymous db")

class EUser(DB):
    
    def __init__(self):
        super().__init__()
        self.id = None
        self.is_active = 1
        self.is_anonymous = 0
        self.is_authenticated = 1
    
    def set_id(self, id_):
        self.id = id_
    
    def get_id(self):
        return self.id
    
    def get_by_id(self, id_):
        r = "SELECT * FROM users WHERE id='{}'".format(id_)
        cursor = self.cur.execute(r)
        return cursor.fetchone()
    
    def get_by_login(self, login_):
        r = "SELECT * FROM users WHERE login='{}'".format(login_)
        cursor = self.cur.execute(r)
        row = cursor.fetchone()
        if row:
            return RUser(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
        return None
    
    def get_by_user(self, u_):
        r = "SELECT * FROM users WHERE login='{}' AND mdp='{}'".format(u_.login, u_.mdp)
        cursor = self.cur.execute(r)
        row = cursor.fetchone()
        if row:
            return RUser(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
        return None
    
    def __repr__(self):
        print("<{}, {}, {}, {}>".format(self.id, self.is_active, self.is_anonymous, self.is_authenticated))
