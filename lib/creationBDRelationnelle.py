#!/usr/bin/env python3

import pprint as pp
import os
import argparse
import sqlite3

#***************************************************************************************************************
#************** Premiere partie : recuperation des donnees au sein du fichier CSV : *****************************
#***************************************************************************************************************

# parser = argparse.ArgumentParser(description='extraction infos du fichier CSV et mise dans base de donnees')
# parser.add_argument('-f', '--csv_file', help='fichier csv avec donnnees', required=True)
#
# args = parser.parse_args()
#
# f_csv = args.csv_file

#Genotype;Milieu;Plate;Id;PR length;Tortuosity;RootArea;LR length;Grouping;Plants/group;distanceFromHypocotyl std (cm);ShootArea;Chlorophyll (a.u) 

def createDB(f_csv, dbname):

	print("\nCreation of the DataBase...")
	print("Please wait...")

	dico_donnees_csv = {}
	with open(f_csv, "r") as fichier_csv :
		cpt = 0 #pour ne pas traiter la premiere ligne
		for ligne in fichier_csv :
			if (cpt>0) : #evite l'entete
				informations = ligne.split(";")
				if (len(informations) == 13) :
					genotype = informations[0]
					milieu = informations[1]
					plate = informations[2]
					Id = informations[3]
					PRlenght = informations[4]
					tortuosity = informations[5]
					rootArea = informations[6]
					LRlength = informations[7]
					grouping = informations[8]
					plantsPerGoup = informations[9]
					distanceFH = informations[10]
					shootArea = informations[11]
					chloro = informations[12]
					chloro = chloro[:-1] #"pour enlever \n
					dico_donnees_csv[Id] = {}
					dico_donnees_csv[Id]["genotype"] = genotype
					dico_donnees_csv[Id]["milieu"] = milieu
					dico_donnees_csv[Id]["plate"] = plate
					dico_donnees_csv[Id]["PRlength"] = PRlenght
					dico_donnees_csv[Id]["tortuosity"] = tortuosity
					dico_donnees_csv[Id]["rootArea"] = rootArea
					dico_donnees_csv[Id]["LRlength"] = LRlength
					dico_donnees_csv[Id]["grouping"] = grouping
					dico_donnees_csv[Id]["plantsPerGoup"] = plantsPerGoup
					dico_donnees_csv[Id]["distanceFH"] = distanceFH
					dico_donnees_csv[Id]["shootArea"] = shootArea
					dico_donnees_csv[Id]["chloro"] = chloro
			cpt = cpt + 1
	#pp.pprint(dico_donnees_csv)

	#donnees sous la forme :

	# 'T2_9': {'LRlength': '6.5',
	#          'PRlength': '3.872',
	#          'chloro': '1.816',
	#          'distanceFH': '0.989',
	#          'genotype': 'pgm',
	#          'grouping': '11',
	#          'milieu': 'Milieu_5',
	#          'plantsPerGoup': '2',
	#          'plate': 'Plate_2',
	#          'rootArea': '0.115',
	#          'shootArea': '0.107',
	#          'tortuosity': '1.107'}}

	#***************************************************************************************************************
	#*********** Deuxieme partie : creation des tables de la BD relationnelle selon diagramme UML: *****************
	#***************************************************************************************************************

	conn = sqlite3.connect(dbname)
	c = conn.cursor()

	c.execute('''CREATE TABLE Seedling
				 (Id string, 
			genotype string, 
			species text, 
			PRIMARY KEY (Id))''')

	c.execute('''CREATE TABLE Plate
				 (IdSeedling string, 
			PlateNumber text, 
			Medium text, 
			PRIMARY KEY (PlateNumber, IdSeedling, Medium), 
			FOREIGN KEY (IdSeedling) REFERENCES Seedling (Id))''')

	c.execute('''CREATE TABLE Grouping
				 (IdSeedling string, 
			GroupingNumber integer, 
			PlateNumber text,
			SeedlingsNumber integer,
			PRIMARY KEY (GroupingNumber, IdSeedling), 
			FOREIGN KEY (IdSeedling) REFERENCES Seedling (Id))''')

	c.execute('''CREATE TABLE Feature
				 (IdSeedling string, 
			Feature_Id text, 
			Value double, 
			PRIMARY KEY (IdSeedling, Feature_Id, Feature_Id, Value), 
			FOREIGN KEY (IdSeedling) REFERENCES Seedling (Id))''')

	c.execute('''CREATE TABLE NucleicAcidSequence
				 (IdSeedling string, 
			id integer, 
			Length double, 
			IsMutated boolean, 
			Sequence string)''')

	c.execute('''CREATE TABLE GlobalAlignment
				 (Id string, 
			Score integer, 
			GapCost integer, 
			IdentityCost integer, 
			SubstitutionCost integer)''')

	c.execute('''CREATE TABLE Ontologies
				 (id integer, 
			libelle text, 
			identifiant_ontologie text, 
			PRIMARY KEY (id))''')

	c.execute('''CREATE TABLE Terms
				 (id integer, 
			term text, 
			PRIMARY KEY (id))''')

	c.execute('''CREATE TABLE Liens
				 (idTerm integer, 
			idOntologie integer, 
			PRIMARY KEY (idTerm, idOntologie), 
			FOREIGN KEY (idTerm) REFERENCES Ontologies (id), 
			FOREIGN KEY (idOntologie) REFERENCES Terms (id))''')

	print("\nDataBase tables created.")

	#***************************************************************************************************************
	#************** Troisieme partie : remplissage des tables de la BD relationnelle : *****************************
	#***************************************************************************************************************
	#utilisation du dictionnaire :
	# 'T2_9': {'LRlength': '6.5',
	#          'PRlength': '3.872',
	#          'chloro': '1.816',
	#          'distanceFH': '0.989',
	#          'genotype': 'pgm',
	#          'grouping': '11',
	#          'milieu': 'Milieu_5',
	#          'plantsPerGoup': '2',
	#          'plate': 'Plate_2',
	#          'rootArea': '0.115',
	#          'shootArea': '0.107',
	#          'tortuosity': '1.107'}}

	for plantule in dico_donnees_csv : #plantule est un dico
		g = dico_donnees_csv[plantule]["genotype"]
		LRl = dico_donnees_csv[plantule]["LRlength"]
		PRl = dico_donnees_csv[plantule]["PRlength"]
		ch = dico_donnees_csv[plantule]["chloro"]
		dfh = dico_donnees_csv[plantule]["distanceFH"]
		rA = dico_donnees_csv[plantule]["rootArea"]
		sA = dico_donnees_csv[plantule]["shootArea"]
		t = dico_donnees_csv[plantule]["tortuosity"]
		pN = dico_donnees_csv[plantule]["plate"] #'plate': 'Plate_2',
		gN = int(dico_donnees_csv[plantule]["grouping"]) # 'grouping': '11',
		ppg = dico_donnees_csv[plantule]["plantsPerGoup"]
		if (dico_donnees_csv[plantule]["milieu"] == "Milieu_1") : #'milieu': 'Milieu_5',
			medium = "Standard"
		elif (dico_donnees_csv[plantule]["milieu"] == "Milieu_2") :
			medium = "Saccharose"
		elif (dico_donnees_csv[plantule]["milieu"] == "Milieu_3") :
			medium = "Microorganism"
		elif (dico_donnees_csv[plantule]["milieu"] == "Milieu_4") :
			medium = "NitrogenDeficiency"
		elif (dico_donnees_csv[plantule]["milieu"] == "Milieu_5") :
			medium = "CarbonDeficiency"
		c.execute(f"insert into Seedling (Id, genotype, species) values ('{plantule}','{g}','Arabidopsis thaliana')")
		c.execute(f"insert into Feature (IdSeedling, Feature_Id, Value) values ('{plantule}','LRLength','{LRl}')")
		c.execute(f"insert into Feature (IdSeedling, Feature_Id, Value) values ('{plantule}','PRLength','{PRl}')")
		c.execute(f"insert into Feature (IdSeedling, Feature_Id, Value) values ('{plantule}','Chlorophyll','{ch}')")
		c.execute(f"insert into Feature (IdSeedling, Feature_Id, Value) values ('{plantule}','distanceFromHypocotyl','{dfh}')")
		c.execute(f"insert into Feature (IdSeedling, Feature_Id, Value) values ('{plantule}','RootArea','{rA}')")
		c.execute(f"insert into Feature (IdSeedling, Feature_Id, Value) values ('{plantule}','ShootArea','{sA}')")
		c.execute(f"insert into Feature (IdSeedling, Feature_Id, Value) values ('{plantule}','tortuosity','{t}')")
		c.execute(f"insert into Plate (IdSeedling, PlateNumber, Medium) values ('{plantule}','{pN}','{medium}')")
		c.execute(f"insert into Grouping (IdSeedling, GroupingNumber, PlateNumber, SeedlingsNumber) values ('{plantule}','{gN}', '{pN}', '{ppg}')")


	c.execute(f"insert into Terms (id, term) values ('1','PRLength')")
	c.execute(f"insert into Terms (id, term) values ('2','RootArea')")
	c.execute(f"insert into Terms (id, term) values ('3','LRLength')")
	c.execute(f"insert into Terms (id, term) values ('4','distanceFromHypocotyl')")
	c.execute(f"insert into Terms (id, term) values ('5','ShootArea')")
	c.execute(f"insert into Terms (id, term) values ('6','Chlorophyll')")

	c.execute(f"insert into Ontologies (id, libelle, identifiant_ontologie) values ('1','root','PO_0009005')")
	c.execute(f"insert into Ontologies (id, libelle, identifiant_ontologie) values ('2','primary root', 'PO_0020127')")
	c.execute(f"insert into Ontologies (id, libelle, identifiant_ontologie) values ('3','lateral root', 'PO_0020121')")
	c.execute(f"insert into Ontologies (id, libelle, identifiant_ontologie) values ('4','shoot','PO_004545')")
	c.execute(f"insert into Ontologies (id, libelle, identifiant_ontologie) values ('5','leaf', 'PO_0025034')")
	c.execute(f"insert into Ontologies (id, libelle, identifiant_ontologie) values ('6','length', 'PATO_0000122')")
	c.execute(f"insert into Ontologies (id, libelle, identifiant_ontologie) values ('7','area', 'PATO_00001323')")
	c.execute(f"insert into Ontologies (id, libelle, identifiant_ontologie) values ('8','distance', 'PATO_0000040')")
	c.execute(f"insert into Ontologies (id, libelle, identifiant_ontologie) values ('9','hypocotyl', 'PO_0020100')")
	c.execute(f"insert into Ontologies (id, libelle, identifiant_ontologie) values ('10','Chlorophyll', 'OMIT_0004055')")

	c.execute(f"insert into Liens (idTerm, idOntologie) values ('1','2')")
	c.execute(f"insert into Liens (idTerm, idOntologie) values ('1','6')")
	c.execute(f"insert into Liens (idTerm, idOntologie) values ('2','1')")
	c.execute(f"insert into Liens (idTerm, idOntologie) values ('2','7')")
	c.execute(f"insert into Liens (idTerm, idOntologie) values ('3','3')")
	c.execute(f"insert into Liens (idTerm, idOntologie) values ('3','6')")
	c.execute(f"insert into Liens (idTerm, idOntologie) values ('4','8')")
	c.execute(f"insert into Liens (idTerm, idOntologie) values ('4','9')")
	c.execute(f"insert into Liens (idTerm, idOntologie) values ('5','4')")
	c.execute(f"insert into Liens (idTerm, idOntologie) values ('5','7')")
	c.execute(f"insert into Liens (idTerm, idOntologie) values ('6','10')")

	conn.commit()
	conn.close()

	print("Data Base tables loaded.\n")
