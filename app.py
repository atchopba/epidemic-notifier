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

from flask import Flask, render_template, request, redirect, make_response

from treatment.db.db import DB
from treatment.db.personne import Personne, TPersonne
from treatment.db.relation import Relation, TRelation
from treatment.db.contact_relation_personne import CRP, TCRP
from treatment.db.test import Test, TTest
from treatment.db.notification import Notification
from treatment.db.personne_notification import PNotification
import treatment.notifier as notifier
import json

ERROR_MSG = "Veuillez recommencer!"

app = Flask(__name__)
 

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/db")
def db_home():
    return render_template("db.html")

@app.route("/db", methods=["POST"])
def db_create():
    DB().create_db()
    return redirect("/relations")

@app.route("/personnes")
def home_personne():
    personnes = CRP().get_personnes_crp() #Personne().get_all()
    return render_template("personne.html", personnes=personnes, nb_personnes=len(personnes))

@app.route("/personnes/search", methods=["POST"])
def search_personne():
    p_name = request.form["search_name"]
    personne_id_1 = request.form["personne_id_1"]
    json_ = json.dumps(Personne().find_by_name(personne_id_1, p_name))
    resp = make_response(json_)
    resp.status_code = 200
    resp.headers["Access-Control-Allow-Origin"] = '*'
    return resp
    
def param_and_add_personne(request):
    nom = request.form["nom"]
    prenom = request.form["prenom"]
    date_naiss = request.form["date_naiss"]
    num_telephone = request.form["num_telephone"]
    email = request.form["email"]
    personne = TPersonne(nom, prenom, date_naiss, num_telephone, email)
    return Personne().add(personne)
    
@app.route("/personnes", methods=["POST"])
def add_personne():
    personne_id = param_and_add_personne(request)
    if personne_id is not None:
        print("=> personne id : ", personne_id)
        return redirect("/personnes")
    return render_template("personne.html", error=ERROR_MSG)

@app.route("/personnes/delete/<int:id_personne>")
def delete_personne(id_personne):
    Personne().delete(id_personne)
    CRP().delete_due_2_personne(id_personne)
    return redirect("/personnes")

@app.route("/relations")
def home_relation():
    relations = Relation().get_all()
    return render_template("relation.html", relations=relations)
    
@app.route("/relations", methods=["POST"])
def add_relation():
    libelle = request.form["libelle"]
    relation = TRelation(libelle)
    relation_id = Relation().add(relation)
    if relation_id is not None:
        return redirect("/relations")
    return render_template("relation.html", error=ERROR_MSG)
    
@app.route("/relations/delete/<int:id_relation>")
def delete_relation(id_relation):
    Relation().delete(id_relation)
    return redirect("/relations")

@app.route("/crp", methods=["GET"])
def home_rcp():
    personne_id = request.args.get("personne")
    if personne_id is None or personne_id == "":
        return redirect("/personnes")
    personne = Personne().get_one(personne_id)
    relations = Relation().get_all()
    personnes = CRP().get_personnes_crp(personne_id)
    #print("=> personnes : ", personnes)
    #print(")> crp : ", CRP().get_all())
    return render_template("crp.html", personne=personne, relations=relations, personnes=personnes)

@app.route("/crp", methods=["POST"])
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
    return render_template("crp.html", 
                           personne=Personne().get_one(personne_id_1), 
                           relations=Relation().get_all(), 
                           personnes=Personne().get_all(),
                           error=ERROR_MSG)

@app.route("/crp/delete/<int:id_crp>")
def delete_crp(id_crp):
    CRP().delete(id_crp)
    return redirect("/relations")

@app.route("/tests", methods=["GET"])
def home_test():
    personne_id = request.args.get("personne")
    personne = Personne().get_one(personne_id) if personne_id is not None else None
    tests = Test().get_all()
    return render_template("test.html", personne=personne, tests=tests)

@app.route("/tests", methods=["POST"])
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
        return render_template("test.html", Personne().get_one(personne_id), tests=Test().get_all(), error=ERROR_MSG)

@app.route("/tests/delete/<int:id_test>")
def delete_test(id_test):
    Test().delete(id_test)
    return redirect("/tests")

@app.route("/notifications")
def home_notification():
    notifications = PNotification().get_notification_pnotifications() #Notification().get_all()
    return render_template("/notification.html", notifications=notifications)

@app.route("/notifications/add", methods=["POST"])
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
    #return render_template("notification.html", error=ERROR_MSG)
    return resp
    
@app.route("/notifications/delete/<int:id_notification>")
def delete_notification(id_notification):
    Notification().delete(id_notification)
    return redirect("/notifications")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
