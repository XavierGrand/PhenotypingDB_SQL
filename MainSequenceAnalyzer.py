#!/usr/bin/env python3

#Projet HMSN204 : Grand Xavier, Vargas Jessica, Salson Marine, M1 BCD

import os
from Bio.Blast import NCBIWWW
from Bio import SeqIO
from lib.EntrezRequest import EntrezFct
from lib.translate import translate
from lib.Blast import blast
from lib.alignement import alignement_fichier_sortie
from argparse import ArgumentParser

################################################################################################################
### Passage des gène, mutant, espèce, database en arguments ####################################################
################################################################################################################

### Décommenter pour utiliser hors tests :
parser = ArgumentParser()
parser.add_argument("gene", help="Wild type gene name. ex : 'NRT2'")
parser.add_argument("mutant", help="Mutant name. ex : 'nrt2.5'")
parser.add_argument("db", help="Database to request : 'nucleotide' or 'protein'.")
parser.add_argument("-al", "--align", action="store_true", help="To perform WT versus mutant sequences.")
# parser.add_argument("-tr", "--translate", action="store_true", help="To translate sequences.")
parser.add_argument("-bl", "--blast", action="store_true", help = "To Blast mutant sequence on NBCI Blastn portal")

args = parser.parse_args()

gene = args.gene #"NRT2"
mutant = args.mutant #"nrt2.5"
db = args.db #"nucleotide"
### Jusqu'ici et commenter la partie test.

### Partie test sans passage en arguments :

# gene = "NRT2" #passage en argument ?
# mutant = "nrt2.5" #passage en argument ?
# db = "nucleotide" #passage en argument ?

################################################################################################################
### Welcome message ############################################################################################
################################################################################################################

print("Project HMSN204 :")
print("Sequence Analyzer part :")
print("\nPresented by :\nMarine Salson,\nJessica Vargas,\nXavier Grand.\n###############################")


################################################################################################################
### Récupération des SeqRecord sur NCBI ########################################################################
################################################################################################################

print("\nLet's begin !!")
print("\nYou are working on " + gene + " gene,\nAnd the mutant " + mutant + ".\n")
print("Sequence request on NCBI Entrez...")
print("Please wait...")

Sequences = EntrezFct(gene, mutant, db) # revoie deux seqRecord
filenameSeq = "./Resultats/" + gene + "_" + mutant + "_" + db + "_sequences.fasta"
SeqIO.write(Sequences, filenameSeq, "fasta")

print("Sequences are saved '" + filenameSeq + "' file.")

seq1 = str(Sequences[0].seq)
seq2 = str(Sequences[1].seq)

################################################################################################################
### Alignement des deux séquences avec algo de progammation dynamique ##########################################
################################################################################################################

if(args.align):
    print("\nYou choose to align WT and mutant sequences.")

    filename = "./Resultats/" + gene + "_Vs_" + mutant + "_SeqAlignement.res"
    alignement_fichier_sortie(seq1, seq2, 3, -1, -1, "maxi", filename)

################################################################################################################
### Translate ##################################################################################################
################################################################################################################

# if(args.translate and db == "nucleotide"):
#   print(\n"Translation of sequences.")
# translatedSeq1 = translate(Sequences[0])
# print(translatedSeq1)

# elif(args.tr == "-tr" and args.db == "protein"):
#   print("Not possible to translate protein sequences")

################################################################################################################
### Blast ######################################################################################################
################################################################################################################

if(args.blast and db == "nucleotide"):
    print("\nYou choose to Blast the mutant nucleic sequence on NCBI.")
    blast(Sequences[1])
elif(args.blast and db == "protein"):
    print("\n___ WARNING ___ \nYou choose to Blast a proteic sequence... \nThis function is not implemented for instance. Please, wait for v2.")

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
