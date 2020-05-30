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

from flask import Blueprint, render_template, redirect, url_for, request, make_response
from flask_login import login_required, logout_user

from .treatment.db.db import DB
from .treatment.db.personne import Personne, TPersonne
from .treatment.db.relation import Relation, TRelation
from .treatment.db.contact_relation_personne import CRP, TCRP
from .treatment.db.test import Test, TTest
from .treatment.db.notification import Notification
from .treatment.db.personne_notification import PNotification
from .treatment import notifier as notifier
from .treatment.personne_graph import build_graph
from .treatment import common as cm
from config import Config
import json

# Blueprint Configuration
main_bp = Blueprint('main_bp', 
                    __name__,
                    template_folder='templates',
                    static_folder='static')

@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))

@main_bp.route("/")
@login_required
def home():
    cpersonne_ = cm.CPersonne(Personne().get_count(), Personne().get_count_gueri(), Personne().get_count_suspect())
    ctest_ = cm.CTest(Test().get_count(), Test().get_count_positif(), Test().get_count_negatif())
    return render_template("myapp/index.html", cpersonne=cpersonne_, ctest=ctest_)

@main_bp.route("/db")
@login_required
def db_home():
    return render_template("myapp/db.html")

@main_bp.route("/db", methods=["POST"])
@login_required
def db_create():
    DB().create_db()
    return redirect("/relations")

@main_bp.route("/personnes")
@login_required
def home_personne():
    personnes = CRP().get_personnes_crp() #Personne().get_all()
    return render_template("myapp/personne.html", personnes=personnes, nb_personnes=len(personnes))

@main_bp.route("/personnes/graph")
@login_required
def graph_personne():
    # selection des personnes pour construire le graphe
    p_ = Personne().get_all()
    graph_msg = "Aucune personne enregistrée pour tracer le graphe!" if len(p_) == 0 else ""
    build_graph()
    return render_template("myapp/personne-graph.html", graph_msg=graph_msg)

@main_bp.route("/personnes/search", methods=["POST"])
@login_required
def search_personne():
    p_name = request.form["search_name"]
    personne_id_1 = request.form["personne_id_1"]
    json_ = json.dumps(Personne().find_by_name_in_crp(personne_id_1, p_name))
    resp = make_response(json_)
    resp.status_code = 200
    resp.headers["Access-Control-Allow-Origin"] = '*'
    return resp

@main_bp.route("/personnes/guerison/<int:id_personne>", methods=["GET"])
@login_required
def guerison_personne(id_personne):
    personne = Personne().get_one(id_personne)
    return render_template("myapp/personne_guerison.html", personne=personne)

@main_bp.route("/personnes/guerison", methods=["POST"])
@login_required
def set_guerison_personne():
    id_ = request.form["personne_id"]
    gueri_ = cm.PERSONNE_GUERI_1 if request.form["gueri"] == "1" else cm.PERSONNE_GUERI_2
    update_ = Personne().update_gueri(id_, gueri_)
    if update_ :
        return redirect("/tests")
    return render_template("/personne/guerison/"+ id_, error=Config.ERROR_MSG_INSERT)

def param_and_add_personne(request):
    nom = request.form["nom"]
    prenom = request.form["prenom"]
    date_naiss = request.form["date_naiss"]
    num_telephone = request.form["num_telephone"]
    email = request.form["email"]
    try:
        suspect = cm.SUSPECT_VALUE_POS if request.form["suspect"] == cm.SUSPECT_CHECKBOX else cm.SUSPECT_VALUE_NEG
    except:
        suspect = cm.SUSPECT_VALUE_NEG
    try:
        p_signe = cm.P_SIGNE_VALUE_POS if request.form["presente_signe"] == cm.P_SIGNE_CHECKBOX else cm.P_SIGNE_VALUE_NEG
    except:
        p_signe = cm.P_SIGNE_VALUE_NEG
    personne = TPersonne(nom, prenom, date_naiss, num_telephone, email, suspect, p_signe)
    return Personne().add(personne)
    
@main_bp.route("/personnes", methods=["POST"])
@login_required
def add_personne():
    personne_id = param_and_add_personne(request)
    if personne_id is not None:
        return redirect("/personnes")
    return render_template("myapp/personne.html", error=Config.ERROR_MSG_INSERT)

@main_bp.route("/personnes/delete/<int:id_personne>")
@login_required
def delete_personne(id_personne):
    Personne().delete(id_personne)
    CRP().delete_due_2_personne(id_personne)
    return redirect("/personnes")

@main_bp.route("/relations")
@login_required
def home_relation():
    relations = Relation().get_all()
    return render_template("myapp/relation.html", relations=relations)
    
@main_bp.route("/relations", methods=["POST"])
@login_required
def add_relation():
    libelle = request.form["libelle"]
    relation = TRelation(libelle)
    relation_id = Relation().add(relation)
    if relation_id is not None:
        return redirect("/relations")
    return render_template("myapp/relation.html", error=Config.ERROR_MSG_INSERT)
    
@main_bp.route("/relations/delete/<int:id_relation>")
@login_required
def delete_relation(id_relation):
    Relation().delete(id_relation)
    return redirect("/relations")

@main_bp.route("/crp", methods=["GET"])
@login_required
def home_rcp():
    personne_id = request.args.get("personne")
    if personne_id is None or personne_id == "":
        return redirect("/personnes")
    personne = Personne().get_one(personne_id)
    relations = Relation().get_all()
    personnes = CRP().get_personnes_crp(personne_id)
    #print("=> personnes : ", personnes)
    #print(")> crp : ", CRP().get_all())
    return render_template("myapp/crp.html", personne=personne, relations=relations, personnes=personnes)

@main_bp.route("/crp", methods=["POST"])
@login_required
def add_rcp():
    personne_id_1 = request.form["personne_id_1"]
    # test de l'id de la 2e personne
    try:
        personne_id_2 = int(request.form["personne_id_2"])
    except ValueError:
        personne_id_2 = param_and_add_personne(request)
    # 
    if personne_id_2 is not None:
        #print("=> utilisateur ajouté : ", personne_id_2)
        id_relation = request.form["id_relation"]
        date_ = request.form["date_contact"]
        heure_ = request.form["heure_contact"]
        crp_ = TCRP(personne_id_1, personne_id_2, id_relation, date_, heure_)
        crp = CRP()
        crp_id = crp.add(crp_)
        if crp_id:
            #print("=> CRP_id : ", crp_id)
            #crp.commit_trans()
            return redirect("crp?personne="+str(personne_id_1))
        #else:
        #    print("=> CRP_id : None ", crp_id)
    return render_template("myapp/crp.html", 
                           personne=Personne().get_one(personne_id_1), 
                           relations=Relation().get_all(), 
                           personnes=Personne().get_all(),
                           error=Config.ERROR_MSG_INSERT)

@main_bp.route("/crp/delete/<int:id_crp>")
@login_required
def delete_crp(id_crp):
    CRP().delete(id_crp)
    return redirect("/relations")

@main_bp.route("/tests", methods=["GET"])
@login_required
def home_test():
    personne_id = request.args.get("personne")
    personne = Personne().get_one(personne_id) if personne_id is not None else None
    tests = Test().get_all()
    return render_template("myapp/test.html", personne=personne, tests=tests)

@main_bp.route("/tests", methods=["POST"])
@login_required
def add_test():
    personne_id = request.form["personne_id"]
    date_test = request.form["date_test"]
    heure_test = request.form["heure_test"]
    date_resultat = request.form["date_resultat"]
    heure_resultat = request.form["heure_resultat"]
    resultat = request.form["resultat"]
    test = TTest(personne_id, date_test, heure_test, date_resultat, heure_resultat, resultat)
    test_id = Test().add(test)
    if test_id:
        #print("=> test_id : ", test_id)
        return redirect("/tests")
    else:
        #print("=> error insertion test")
        return render_template("myapp/test.html", Personne().get_one(personne_id), tests=Test().get_all(), error=Config.ERROR_MSG_INSERT)

@main_bp.route("/tests/delete/<int:id_test>")
@login_required
def delete_test(id_test):
    Test().delete(id_test)
    return redirect("/tests")

@main_bp.route("/notifications")
@login_required
def home_notification():
    notifications = PNotification().get_notification_pnotifications() #Notification().get_all()
    return render_template("myapp/notification.html", notifications=notifications)

@main_bp.route("/notifications/add", methods=["POST"])
@login_required
def add_notification():
    notification_id = Notification().add()
    if notification_id is not None:
        print("=> notification_id : ", notification_id) 
        resp = make_response(notifier.notifier_personne(notification_id))
        resp.status_code = 200
        resp.headers["Access-Control-Allow-Origin"] = '*'
        print("=> fin de la notification")
        #return redirect("/notifications")
    else:
        print("=> notification_id : RIEN")
    #return render_template("myapp/notification.html", error=ERROR_MSG)
    return resp
    
@main_bp.route("/notifications/delete/<int:id_notification>")
@login_required
def delete_notification(id_notification):
    Notification().delete(id_notification)
    return redirect("/notifications")
