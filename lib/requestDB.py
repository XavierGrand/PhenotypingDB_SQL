#!/usr/bin/env python3

import sqlite3

#***************************************************************************************************************
#************** Requetes sur les tables de la BD relationnelle : ***********************************************
#***************************************************************************************************************

def resquestExemple(dbname):

    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    with open("./Resultats/Resultats_requetes_SQL", "w") as fichier :

        fichier.write("Resutlats des exemples de requetes sur la base de donnees :\n\n")

        fichier.write("\n** requete : SELECT * FROM Seedling \n")
        c.execute('SELECT * FROM Seedling')
        cpt = 0
        for ligne in c :
            if cpt < 10 :
                fichier.write(f"{ligne}\n")
            cpt = cpt + 1

        fichier.write("\n** requete : SELECT * FROM Ontologies \n")
        c.execute('SELECT * FROM Ontologies')
        for ligne in c :
            fichier.write(f"{ligne}\n")

        fichier.write("\n** requete : SELECT s.species, count(*) from Seedling s group by s.species \n")
        fichier.write("Nombre de plantules totales :\n")
        c.execute('SELECT s.species, count(*) from Seedling s group by s.species')
        for res in c :
            fichier.write(f"{res}\n")

        fichier.write("\n** requete : SELECT genotype, count(*) from Seedling group by genotype\n")
        fichier.write("Nombre de plantules de chaque genotype :\n")
        c.execute('SELECT genotype, count(*) from Seedling group by genotype')
        for res in c :
            fichier.write(f"{res}\n")

        fichier.write("\n** requete : SELECT avg(Value), Feature_Id from Feature group by Feature_Id \n")
        fichier.write("Moyenne des differents caracteres morphologiques chez toutes les plantules:\n")
        c.execute(f"SELECT avg(Value), Feature_Id from Feature group by Feature_Id")
        for res in c :
            fichier.write(f"{res}\n")

        fichier.write("\n** requete : SELECT avg(Value), Feature_Id, genotype from Feature f, Seedling s where f.IdSeedling = s.Id and genotype = {gtp} and Feature_Id = {prl} group by Feature_Id \n")
        fichier.write("Moyenne des longueurs des racines primaires chez Col_0:\n")
        gtp = "\'Col_0\'"
        prl = "\'PRLength\'"
        c.execute(f"SELECT avg(Value), Feature_Id, genotype from Feature f, Seedling s where f.IdSeedling = s.Id and genotype = {gtp} and Feature_Id = {prl} group by Feature_Id")
        for res in c :
            fichier.write(f"{res}\n")

        fichier.write("\n** requete : SELECT avg(Value), Feature_Id, genotype from Feature f, Seedling s where f.IdSeedling = s.Id and genotype = {gtp} and Feature_Id = {prl} group by Feature_Id\n")
        fichier.write("Moyenne des longueurs des racines primaires chez le mutant nrt:\n")
        gtp = "\'nrt\'"
        prl = "\'PRLength\'"
        c.execute(f"SELECT avg(Value), Feature_Id, genotype from Feature f, Seedling s where f.IdSeedling = s.Id and genotype = {gtp} and Feature_Id = {prl} group by Feature_Id")
        for res in c :
            fichier.write(f"{res}\n")

        fichier.write("\n** requete : SELECT avg(Value), Feature_Id, genotype from Feature f, Seedling s where f.IdSeedling = s.Id and genotype = {gtp} and Feature_Id = {prl} group by Feature_Id\n")
        fichier.write("Moyenne des longueurs des racines primaies chez le mutant pgm:\n")
        gtp = "\'pgm\'"
        prl = "\'PRLength\'"
        c.execute(f"SELECT avg(Value), Feature_Id, genotype from Feature f, Seedling s where f.IdSeedling = s.Id and genotype = {gtp} and Feature_Id = {prl} group by Feature_Id")
        for res in c :
            fichier.write(f"{res}\n")

        fichier.write("\n** requete : SELECT avg(Value), Feature_Id, genotype from Feature f, Seedling s where f.IdSeedling = s.Id and genotype = {gtp} and Feature_Id = {prl} group by Feature_Id\n")
        fichier.write("Moyenne des longueurs des racines primaies chez le mutant sex1:\n")
        gtp = "\'sex1\'"
        prl = "\'PRLength\'"
        c.execute(f"SELECT avg(Value), Feature_Id, genotype from Feature f, Seedling s where f.IdSeedling = s.Id and genotype = {gtp} and Feature_Id = {prl} group by Feature_Id")
        for res in c :
            fichier.write(f"{res}\n")

        fichier.write("\n** requete : SELECT f.IdSeedling, genotype,Feature_Id, MAX(Value), Medium from Feature f, Seedling s, Plate p where Feature_Id = {prl} and f.IdSeedling = p.IdSeedling and f.IdSeedling = s.Id \n")
        fichier.write("Individu avec les racines primaires les plus longues, et son milieu, et son genotype:\n")
        prl = "\'PRLength\'"
        c.execute(f"SELECT f.IdSeedling, genotype,Feature_Id, MAX(Value), Medium from Feature f, Seedling s, Plate p where Feature_Id = {prl} and f.IdSeedling = p.IdSeedling and f.IdSeedling = s.Id ")
        for res in c :
            fichier.write(f"{res}\n")

    conn.commit()
    conn.close()

    print("\nResultats_requetes_SQL file created.\n")

    # ***************************************************************************************************************
    # ************** Requetes On demand : ***************************************************************************
    # ***************************************************************************************************************

def ondemandrequest(dbname, req):

    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute(req)
    for res in c:
        print(f"{res}\n")

    conn.commit()
    conn.close()
