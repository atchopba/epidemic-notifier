EPIDEMIC NOTIFIER
-----------------
L'outil est fait pour notifier les personnes qui ont été en contact avec une autre:
1. après un test de l'épidémie + 
2. le test de la personne est positif + 
3. MAJ du dossier de la personne 
=> notification de toute personne ayant été en contact X jours auparavant

SQLite, Python, Flask
DB:
- patient
- a_ete_contact/proche: nature (boulot, voisinage, ...)
-

=====

    def get_all_crp_with_id_personne(self, personne_id=None):
        r = ("SELECT p.id, p.nom, p.prenom, p.date_naiss, p.num_telephone, p.email, COUNT(crp.id) "
            "FROM contact_relation_personnes crp "
            "JOIN personnes p ON p.id = crp.personne_id_1 ")
        if personne_id is not None:
            r += "WHERE p.id=?"
            self.cur.execute(r, personne_id)
        else:
            self.cur.execute(r)
        rows = self.cur.fetchall()
        print("=> rows : ", rows)
        return [RCRPPersonne(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows]
        
    """
    def get_all_crp_with_id_personne(self, id_personne):
        #r = ("SELECT * FROM personnes WHERE id IN "
        #     "(SELECT personne_id_2 FROM contact_relation_personnes WHERE personne_id_1=?)")
        r = "SELECT DISTINCT personne_id_2 FROM contact_relation_personnes WHERE personne_id_1=?"
        self.cur.execute(r, id_personne)
        rows = self.cur.fetchall()
        if len(rows) > 0:
            #print("=> rows : ", rows)
            p_id_str = "','".join([str(row[0]) for row in rows])
            r = "SELECT * FROM personnes WHERE id IN ('"+ p_id_str +"')"
            #print("=> requete => ", r)
            self.cur.execute(r)
            rows = self.cur.fetchall()
            #
            if len(rows) > 0:
                #print("=> get_all_crp_with_id_personne : ", rows)
                return [RPersonne(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]
        return None
    """