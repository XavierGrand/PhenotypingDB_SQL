#!/usr/bin/env python

import alignement
from Bio.Seq import Seq
from Bio import SeqIO

maSeq1 = Seq("ATGCATGGCATGCATGC")
seq1 = str(maSeq1)

maSeq2 = Seq("ATGCATGCATGCATGCGGAAC")
seq2 = str(maSeq2)

matrice = []

alignement.alignement_fichier_sortie(seq1, seq2, 0, 3, 3, "mini", "fichier_res")

for position in alignement.alignement(seq1, seq2, 0, 3, 3, "mini", matrice) :
	print position 

for ligne in matrice :
	print ligne