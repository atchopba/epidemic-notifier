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

import os
import json
from epidemic_notifier.treatment.db.test import Test
from epidemic_notifier.treatment.db.contact_relation_personne import CRP

from config import Config

def set_group(suspect_, teste_):
    if teste_ == None:
        if not (suspect_ == "oui"):
            group_ = "0"
        else:
            group_ = "1"
    else:
        if teste_ == 1:
            if not (suspect_ == "oui"):
                group_ = "2"
            else:
                group_ = "3"
        elif teste_ == 0:
            if not (suspect_ == "oui"):
                group_ = "4"
            else:
                group_ = "5"
    return group_


def get_nodes_graph():
    tp_dict =  []
    for tp in Test().find_for_graph():
        # 
        tp_dict.append({
            "id": tp.p_nom,
            "group": set_group(tp.p_suspect, tp.t_resultat) 
        })
    return tp_dict

def get_links_graph():
    crp_dict = []
    for crp_ in CRP().find_for_graph():
        crp_dict.append({
            "source": crp_.nom,
            "target": crp_.nom_2,
            "value": 4 * int(crp_.nb_contact)
        })
    return crp_dict

def build_graph():
    if os.path.exists(Config.PATH_GRAPH):
        os.remove(Config.PATH_GRAPH)
    with open(Config.PATH_GRAPH, "w") as outfile: 
          json.dump({
                "nodes": get_nodes_graph(),
                "links": get_links_graph()
            }, outfile, indent=4)
