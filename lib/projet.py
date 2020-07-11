#!/usr/bin/env python

import pprint as pp
import os
import argparse
import sqlite3

#***************************************************************************************************************
#************** Premiere partie : recuperation des donnees au sein du fichier CSV : *****************************
#***************************************************************************************************************

parser = argparse.ArgumentParser(description='extraction infos du fichier CSV et mise dans base de donnees')
parser.add_argument('-f', '--csv_file', help='fichier csv avec donnnees', required=True)

args = parser.parse_args()

f_csv = args.csv_file 

#Genotype;Milieu;Plate;Id;PR length;Tortuosity;RootArea;LR length;Grouping;Plants/group;distanceFromHypocotyl std (cm);ShootArea;Chlorophyll (a.u) 

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


#***************************************************************************************************************
#*********** Deuxieme partie : creation des tables de la BD relationnelle selon diagramme UML: *****************
#***************************************************************************************************************

conn = sqlite3.connect('base_de_donnees.db') 
c = conn.cursor()
c.execute('''CREATE TABLE Seedling
             (Id string, genotype string, species text)''')

c.execute('''CREATE TABLE Plate
             (PlateNumber text, Medium text)''')

c.execute('''CREATE TABLE Grouping
             (GroupingNumber integer)''')

c.execute('''CREATE TABLE Feature
             (Feature_Id text, Value double)''')

c.execute('''CREATE TABLE NucleicAcidSequence
             (id integer, Length double, IsMutated boolean, Sequence string)''')

c.execute('''CREATE TABLE GlobalAlignment
             (Id string, Score integer, GapCost integer, IdentityCost integer, SubstitutionCost integer)''')

c.execute('''CREATE TABLE Ontologies
             (id integer, libelle text, identifiant_ontologie text)''')

c.execute('''CREATE TABLE Terms
             (id text, term text)''')


#***************************************************************************************************************
#************** Troisieme partie : remplissage des tables de la BD relationnelle : *****************************
#***************************************************************************************************************
#utilisation du dictionnaire :
# 'T2_9': {'LRlength': '6.5',
#          'PRlength': '3.872',
#          'chloro': '1.816\n',  (\n a enlever)
#          'distanceFH': '0.989',
#          'genotype': 'pgm',
#          'grouping': '11',
#          'milieu': 'Milieu_5',
#          'plantsPerGoup': '2',
#          'plate': 'Plate_2',
#          'rootArea': '0.115',
#          'shootArea': '0.107',
#          'tortuosity': '1.107'}}
#exemple : 
#data = [{'x': 1, 'y2': 'aaa'}, {'x': 2, 'y2': 'bbb'}]
#for d in data:
#    c.execute("insert into myTable (x, y) values (:x, :y2)", d)
#c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")



for plantule in dico_donnees_csv : #plantule est un dico
	g = dico_donnees_csv[plantule]["genotype"]
	c.execute(f"insert into Seedling (Id, genotype, species) values ('{plantule}','{g}','Arabidopsis thaliana')")


#***************************************************************************************************************
#************** quatrieme partie : requetes sur les tables de la BD relationnelle : ****************************
#***************************************************************************************************************

c.execute('SELECT * FROM Seedling')

print(c.fetchone())

c.close()
