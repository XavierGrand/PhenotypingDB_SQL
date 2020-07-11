#!/usr/bin/env python

import sys
from Bio.Seq import Seq
from Bio import SeqIO

#alignement GLOBAL de deux sequences, avec methode de DISTANCE :

if len(sys.argv) == 3 :

	sequence1 = sys.argv[1]
	sequence2 = sys.argv[2]

	Sequence_1 = SeqIO.read(sys.argv[1], 'fasta')
	Sequence_2 = SeqIO.read(sys.argv[2], 'fasta')

	seq1 = Sequence_1.seq
	seq2 = Sequence_2.seq

	#print("Sequence 1 : ")
	#print(seq1)
	#print("Sequence 2 : ")
	#print(seq2)
	S1_1 = Seq("X")
	S2_1 = Seq("X")
	
	S1_2 = Seq("GGCTGAC")
	S2_2 = Seq("GATC")
	
	S1 = S1_1 + S1_2
	S2 = S2_1 + S2_2

	#M(0,0) = 0
	#g = 3 ; sub = 3 ; id = 0
	g = 3
	sub = 3
	iden = 0


	listeI = []
	cpt_Liste_I = 0
	cpti = 0
	cptj = 1
	v2 = g
	for base2 in S2 : #S2 = "GATC" 
		if cpti == 0 : # premiere ligne
			listeJ = []
			v = 0
			cpt = 0
			for base1 in S1 : #S1 = "GGCTGAC"
				listeJ.append(int(v))
				cpt = cpt + 1
				v = cpt * g 
			listeI.append(listeJ)
		if cpti > 0 : #de la deuxieme a la derniere ligne 
			listeJ = []
			cpt = 0
			cpt_Liste_J = 0
			for base1 in S1 : #S1 = "GGCTGAC"
				if cpt == 0 :
					listeJ.append(int(v2)) #valeur de la premiere case, dependant de g uniquement et de l'indice
				x = 1
				if cpt > 0 :
					Liste_backtracking = []
					x=0
					a = listeI[cpt_Liste_I-1][cpt_Liste_J] + sub
					b = listeI[cpt_Liste_I-1][cpt_Liste_J-1]
					c = listeJ[cpt_Liste_J-1] + sub #/!\ listeJ pas encore ajoutee a listeI
					if base2 != base1 : #si on a une substitution, sinon b ne change pas
						b =  b + 3  
					if a <= b and a <= c : #si deux egaux !!! 
						x = a
					if b <= a and b <= c :
						x = b
					if c <= a and c <= b :
						x = c
					listeJ.append(x)
				cpt_Liste_J = cpt_Liste_J + 1
				cpt = cpt + 1
			listeI.append(listeJ)
		cpti = cpti + 1
		v2 = cptj * g 
		cptj = cptj + 1
		cpt_Liste_I = cpt_Liste_I + 1

			

	#ListeI : matrice remplie
	for liste in listeI :
		print(liste)	


	cpt1 = len(listeI)
	cpt2 = len(listeJ)
	"""print("***cpt1***")
	print(cpt1)
	print("***cpt2***")
	print(cpt2)
	print(S1[cpt2-1]) #C
	print(S2[cpt1-1]) #C
	print(S1[cpt2-2]) #A
	print(S2[cpt1-2]) #T"""

	liste_alignement = []
	liste = []
	"""liste.append(S1[cpt2-1])
	liste.append(S2[cpt1-1])
	liste_alignement.append(liste)"""
	
	while cpt1 > 1 and cpt2 > 1 : 
		liste = []
		base_S1 = S1[cpt2-1]
		base_S2 = S2[cpt1-1]
		a = listeI[cpt1-2][cpt2-1] + sub
		b = listeI[cpt1-2][cpt2-2]
		c = listeI[cpt1-1][cpt2-2] + sub
		#print("**base**")
		#print(base_S1)
		#print(base_S2)
		if base_S1 != base_S2 :
			b = listeI[cpt1-2][cpt2-2] + sub
		if a <= b and a <= c : 
			#print("**a**")
			liste.append(S2[cpt1-1])
			liste.append("-")
			cpt1 = cpt1 - 1
		if c <= a and c <= b and c != a :
			#print("**c**")
			liste.append("-")
			liste.append(S1[cpt2-1])
			cpt2 = cpt2 - 1
		if b <= a and b <= c and b != a and b != c:
			#print("**b**")
			liste.append(S1[cpt2-1])
			liste.append(S2[cpt1-1])
			cpt1 = cpt1 - 1
			cpt2 = cpt2 - 1
		"""print("***************a***************")
		print(a)
		print("***************b***************")
		print(b)
		print("***************c***************")
		print(c)"""
		liste_alignement.append(liste)
		#cpt1 = cpt1 - 1
		#cpt2 = cpt2 - 1

	print(liste_alignement)



else :
	print("Il faut deux sequences fasta en arguments.")
