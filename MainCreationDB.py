#!/usr/bin/env python3

#API de création de la Base de données relationnelle : Grand Xavier, Vargas Jessica, Salson Marine, M1 BCD

import os
from lib.creationBDRelationnelle import createDB
from lib.requestDB import resquestExemple
from lib.requestDB import ondemandrequest
from argparse import ArgumentParser

################################################################################################################
### Passage du fichichier brut .csv en arguments ###############################################################
################################################################################################################

parser = ArgumentParser()
parser.add_argument("inputFile", help="Phenotyping results in csv file properly formated in ./Datasets/ folder. "
                                      "ex : 'Data_Projet_Entete.csv'")
parser.add_argument("dbname", help="Name of the Data Base")
parser.add_argument("-cr", "--create", action="store_true", help="To create the Data Base, manager only.")
parser.add_argument("-rqex", "--requestexample", action="store_true", help = "To send example requests on existing Data Base.")
parser.add_argument("-rq", "--request", action = "store_true", help = "To send a request on existing Data Base.")

args = parser.parse_args()

inputFile = args.inputFile
dbname = "./DataBase/" + args.dbname

################################################################################################################
### Welcome message ############################################################################################
################################################################################################################

print("Project HMSN204 :")
print("Phenotyping Data Base part :")
print("\nPresented by :\nMarine Salson,\nJessica Vargas,\nXavier Grand.\n###############################")

################################################################################################################
### Creation ###################################################################################################
################################################################################################################

if(args.create):
    print("You ask to create a Data Base named : " + args.dbname + ".")
    liste = os.listdir("./DataBase/")
    if(args.dbname in liste) :
        print("\nData Base allready exists...")
        print("\nData Bases allready created : ")
        print(liste)
        print("\nPlease, use request parameter, modify the Data Base name, or delete and re-create.")
        print("Update DataBase option is not implemented for instance, please wait for v2.")
    else:
        createDB(inputFile, dbname)
        print("Data Base saved in '" + dbname + "' file.")

################################################################################################################
### Request ####################################################################################################
################################################################################################################

if(args.requestexample):
    print("You try to request the Data Base named : " + args.dbname + ".")
    liste = os.listdir("./DataBase/")
    if (args.dbname not in liste):
        print("\nData Base does'nt exist...")
        print("\nData Bases allready created : ")
        print(liste)
        print("\nPlease, modify the Data Base name, or create.")
    else :
        resquestExemple(dbname)


################################################################################################################
### On-demand Request ##########################################################################################
################################################################################################################

if(args.request):
    print("You try to request the Data Base named : " + args.dbname + ".")
    liste = os.listdir("./DataBase/")
    if (args.dbname not in liste):
        print("\nData Base does'nt exist...")
        print("\nData Bases allready created : ")
        print(liste)
        print("\nPlease, modify the Data Base name, or create.")
    else :
        print("Please, type your SQL request : ")
        req = input()
        ondemandrequest(dbname, req)

################################################################################################################
### Goodbye message ##########################################################################################
################################################################################################################

print("\nPress 'Enter' to quit.")
wait = input()

os.system('cls' if os.name == 'nt' else 'clear')
print("####################################################################################################\n")
print("                                   Thank You for using our tool.")
print("                                 We hope you obtained satisfaction.")
print("                                  Don't forget to cite that work !")
print("\n####################################################################################################\n")
