#!/usr/bin/env python

from datetime import datetime

#Projet HMSN204 : Grand Xavier, Vargas Jessica, Salson Marine, M1 BCD

#Ce programme contient une fonction permettant l'alignement par paire exact et global de deux sequences, selon la methode de Needleman & Wunsch (1970).
#L'alignement se fait en utilisant le principe de la programmation dynamique, 
#et passe par l'elaboration d'une matrice comportant les scores des sous-alignements intermediaires.


#les fonctions minimum ou maximum ci-dessous sont utilisees lors du remplissage de la matrice de scores (ligne 80).
#Selon la methode utilisee, de distance ou de similarite, l'une ou l'autre de ses fonctions est utilisee.

def minimum(a, b, c) : 
	mini = 0
	if a <= b and a <= c : 
		mini = a
	if b <= a and b <= c :
		mini = b
	if c <= a and c <= b :
		mini = c
	return mini

def maximum(a, b, c) : 
	maxi = 0
	if a >= b and a >= c : 
		maxi = a
	if b >= a and b >= c :
		maxi = b
	if c >= a and c >= b :
		maxi = c
	return maxi

#******************************************************
#************** fonction alignement : *****************
#******************************************************

#La fonction prend 7 parametres :

# 1. et 2. : les deux sequences a aligner en chaine de caractere (sequence WT et sequence mutee)
# 3. 4. et 5. : les valeurs utilisees pour les penalites d'identite, de substitution et de gap, respectivement
# 6. les termes maxi ou mini en string, selon si une methode de distance (fonction minimum, mini en string), ou de similarite (fonction maximum, maxi en string) est utilisee
# 7. la liste, initialisee a l'exterieur, qui sera remplie et modifiee par la fonction et qui correspondra a la matrice de scores des sous-alignements intermediaires.
# Passer cette liste en parametre permet ensuite d'y acceder et de pouvoir l'afficher.

# La fonction alignement retourne une liste de tuples, qui correspond a l'alignement des deux sequences.

def alignement(sequence1, sequence2, penaliteIdentite, penaliteSubstitution, penaliteGap, methode, matrice) :

	# ************* 1. Elaboration de la matrice : ************** 

	#La matrice est une liste de listeS :
	#elle est passee en argument, et doit donc etre initialisee a l'exterieur de la fonction,
	#et elle est remplie ligne par ligne.
	#Pour chaque ligne de la matrice, une nouvelle liste est cree, nommee ligne.
	#Le remplissage de la premiere ligne, ne depend que de la valeur de la penalite de gap et du numero de colonne :
	ligne = [] #premiere ligne de la matrice
	cpt = 0 #le compteur cpt correspond a chaque numero de colonne de la matrice, il n'est utilise que pour la premiere ligne
	#ce compteur permet de remplir la premiere ligne, en fonction de la penalite de gap et de l'indice de la colonne
	ligne.append(cpt * penaliteGap) 
	for base_1 in sequence1 : #remplissage du reste de la premiere ligne
		cpt = cpt + 1
		ligne.append(cpt * penaliteGap)
	matrice.append(ligne) #la liste_j, correspondant ici a la premiere ligne de la matrice, est ajoutee a cette derniere
	cpt_ligne = 1 #le compteur cpt_ligne correspond a chaque numero de LIGNE de la matrice, ici, la ligne 0 est deja remplie, cpt_ligne commence donc a 1
	for base_2 in sequence2 : #parcours de la sequence2, et remplissage de chaque ligne
		ligne = [] #nouvelle ligne de la matrice a remplir, d'indice cpt_ligne
		ligne.append(cpt_ligne * penaliteGap) #remplissage du premier element de la ligne : celui-ci ne depend que de l'indice de la ligne et de la penalite de gap
		cpt_colonne = 0 #cpt_colonne correspond a chaque numero de COLONNE de la matrice
		for base_1 in sequence1 : #remplissage du reste de la ligne, en parcourant la sequence1
			valeur = 0 #cette variable correspond a la valeur qui sera ajoutee a la liste ligne a chaque position
			#trois possibilite de valeur sont testees : dans une methode par distance, la valeur minimale est conservee, dans une methode par similarite, la valeur maximale est conservee
			if base_2 != base_1 : #si les deux bases sont differentes (cas d'une substitution)
				valeur_1 = matrice[cpt_ligne-1][cpt_colonne] + penaliteSubstitution
			else : #si les deux bases sont identiques
				valeur_1 = matrice[cpt_ligne-1][cpt_colonne] + penaliteIdentite
			valeur_2 = matrice[cpt_ligne-1][cpt_colonne + 1] + penaliteGap
			valeur_3 = ligne[cpt_colonne] + penaliteGap
			if methode == "maxi" :
				valeur = maximum(valeur_1, valeur_2, valeur_3) 
			elif methode == "mini" :
				valeur = minimum(valeur_1, valeur_2, valeur_3) 
			ligne.append(valeur) #la ligne en cours, correspondant a la liste ligne, est remplie au fur et a mesure que la sequence1 est parcourue
			cpt_colonne = cpt_colonne + 1
		matrice.append(ligne) #la ligne correspondant a la liste ligne est ajoutee a la matrice, a chaque base de la sequence2 parcourue
		cpt_ligne = cpt_ligne + 1 

	# 2.************* Etape de backtracking : ***************** 

	#Le backtracking permet de recuperer l'alignement des sequences en fonction des valeurs presentent dans la matrice realisee precedemment
	
	liste_alignement = [] #cette liste contiendra l'ensemble des positions de l'alignement des deux sequences
	cpt_sequence1 = len(sequence1) #les compteurs cpt_sequence permettent de parcourir les sequences en partant de leur fin
	cpt_sequence2 = len(sequence2)
	while not (cpt_sequence1 == 0 and cpt_sequence2 == 0) : #tant que les totalites des deux sequences ne sont pas parcourues
		position = [] #cette liste comprendra deux elements (tuples) correspondant a une position de l'alignement deux a deux (ex: ['A' 'A'] ou ['-' 'G']) 
		valeur = 0 #valeur correspondra a la valeur choisie entre les trois valeurs testees lors du backtracking
		base_sequence1 = sequence1[cpt_sequence1-1] #base_sequence permet d'avoir acces a la base en cours lors du parcours de la matrice
		base_sequence2 = sequence2[cpt_sequence2-1]
		valeur1 = matrice[cpt_sequence2-1][cpt_sequence1] + penaliteGap
		valeur2 = matrice[cpt_sequence2-1][cpt_sequence1-1]
		valeur3 = matrice[cpt_sequence2][cpt_sequence1-1] + penaliteGap
		if base_sequence1 != base_sequence2 :
			valeur2 = valeur2 + penaliteSubstitution
		else :
			valeur2 = valeur2 + penaliteIdentite
		if methode == "maxi" :
			valeur = maximum(valeur1, valeur2, valeur3) 
		elif methode == "mini" :
			valeur = minimum(valeur1, valeur2, valeur3)
		if valeur == valeur1 :
			position.append("-")
			position.append(base_sequence2)
			cpt_sequence2 = cpt_sequence2 - 1
		elif valeur == valeur2 :
			position.append(base_sequence1)
			position.append(base_sequence2)
			cpt_sequence1 = cpt_sequence1 - 1
			cpt_sequence2 = cpt_sequence2 - 1
		elif valeur == valeur3 :
			position.append(base_sequence1)
			position.append("-")
			cpt_sequence1 = cpt_sequence1 -1
		liste_alignement.append(position) #la position est ajoutee a la liste contenant l'alignement
	return liste_alignement #la fonction alignement retourne une liste de tuples correspondant a l'alignement des deux sequences


#Fonctions matrice et backtracking, correspondant aux deux etapes separees de la fonction alignement : 

def matrice(sequence1, sequence2, penaliteIdentite, penaliteSubstitution, penaliteGap, methode) :
	matrice = []
	liste_j = [] 
	cpt = 0 
	liste_j.append(cpt * penaliteGap) 
	for base_1 in sequence1 :
		cpt = cpt + 1
		liste_j.append(cpt * penaliteGap)
	matrice.append(liste_j) 
	cpt_i = 1 
	for base_2 in sequence2 : 
		liste_j = [] 
		liste_j.append(cpt_i * penaliteGap) 
		cpt_j = 0 
		for base_1 in sequence1 : 
			valeur = 0 
			if base_2 != base_1 : 
				valeur_1 = matrice[cpt_i-1][cpt_j] + penaliteSubstitution
			else : 
				valeur_1 = matrice[cpt_i-1][cpt_j] + penaliteIdentite
			valeur_2 = matrice[cpt_i-1][cpt_j + 1] + penaliteGap
			valeur_3 = liste_j[cpt_j] + penaliteGap
			if methode == "maxi" :
				valeur = maximum(valeur_1, valeur_2, valeur_3) 
			elif methode == "mini" :
				valeur = minimum(valeur_1, valeur_2, valeur_3)
			liste_j.append(valeur) 
			cpt_j = cpt_j + 1
		matrice.append(liste_j)
		cpt_i = cpt_i + 1 
	return matrice

def backtracking(sequence1, sequence2, penaliteIdentite, penaliteSubstitution, penaliteGap, methode, matrice) :
	liste_alignement = [] 
	cpt_sequence1 = len(sequence1) 
	cpt_sequence2 = len(sequence2)
	while not (cpt_sequence1 == 0 and cpt_sequence2 == 0) : 
		position = []  
		valeur = 0 
		base_sequence1 = sequence1[cpt_sequence1-1] 
		base_sequence2 = sequence2[cpt_sequence2-1]
		valeur1 = matrice[cpt_sequence2-1][cpt_sequence1] + penaliteGap
		valeur2 = matrice[cpt_sequence2-1][cpt_sequence1-1]
		valeur3 = matrice[cpt_sequence2][cpt_sequence1-1] + penaliteGap
		if base_sequence1 != base_sequence2 :
			valeur2 = valeur2 + penaliteSubstitution
		else :
			valeur2 = valeur2 + penaliteIdentite
		if methode == "maxi" :
			valeur = maximum(valeur1, valeur2, valeur3) 
		elif methode == "mini" :
			valeur = minimum(valeur1, valeur2, valeur3)
		if valeur == valeur1 :
			position.append("-")
			position.append(base_sequence2)
			cpt_sequence2 = cpt_sequence2 - 1
		elif valeur == valeur2 :
			position.append(base_sequence1)
			position.append(base_sequence2)
			cpt_sequence1 = cpt_sequence1 - 1
			cpt_sequence2 = cpt_sequence2 - 1
		elif valeur == valeur3 :
			position.append(base_sequence1)
			position.append("-")
			cpt_sequence1 = cpt_sequence1 -1
		liste_alignement.append(position) 
	return liste_alignement

#Fonctions permettant de renvoyer le resultats de l'alignement dans un fichier dont on peut choisir le nom :

#Le parametre 7 n'est plus une matrice vide, mais le nom du fichier dans lequel le resultat de l'alignement est ecrit

def alignement_fichier_sortie(sequence1, sequence2, penaliteIdentite, penaliteSubstitution, penaliteGap, methode, nomFichier) :

	print("\nStart alignment...")
	print("Please wait...")

	date = datetime.now()
	matrice = []
	liste_j = [] 
	cpt = 0 
	liste_j.append(cpt * penaliteGap) 
	for base_1 in sequence1 : 
		cpt = cpt + 1
		liste_j.append(cpt * penaliteGap)
	matrice.append(liste_j) 
	cpt_i = 1  
	for base_2 in sequence2 : 
		liste_j = [] 
		liste_j.append(cpt_i * penaliteGap) 
		cpt_j = 0 
		for base_1 in sequence1 : 
			valeur = 0 
			if base_2 != base_1 : 
				valeur_1 = matrice[cpt_i-1][cpt_j] + penaliteSubstitution
			else : 
				valeur_1 = matrice[cpt_i-1][cpt_j] + penaliteIdentite
			valeur_2 = matrice[cpt_i-1][cpt_j + 1] + penaliteGap
			valeur_3 = liste_j[cpt_j] + penaliteGap
			if methode == "maxi" :
				valeur = maximum(valeur_1, valeur_2, valeur_3) 
			elif methode == "mini" :
				valeur = minimum(valeur_1, valeur_2, valeur_3)
			liste_j.append(valeur) 
			cpt_j = cpt_j + 1
		matrice.append(liste_j)
		cpt_i = cpt_i + 1 
	liste_alignement = [] 
	cpt_sequence1 = len(sequence1) 
	cpt_sequence2 = len(sequence2)
	while not (cpt_sequence1 == 0 and cpt_sequence2 == 0) : 
		position = []  
		valeur = 0
		base_sequence1 = sequence1[cpt_sequence1-1] 
		base_sequence2 = sequence2[cpt_sequence2-1]
		valeur1 = matrice[cpt_sequence2-1][cpt_sequence1] + penaliteGap
		valeur2 = matrice[cpt_sequence2-1][cpt_sequence1-1]
		valeur3 = matrice[cpt_sequence2][cpt_sequence1-1] + penaliteGap
		if base_sequence1 != base_sequence2 :
			valeur2 = valeur2 + penaliteSubstitution
		else :
			valeur2 = valeur2 + penaliteIdentite
		if methode == "maxi" :
			valeur = maximum(valeur1, valeur2, valeur3) 
		elif methode == "mini" :
			valeur = minimum(valeur1, valeur2, valeur3)
		if valeur == valeur1 :
			position.append("-")
			position.append(base_sequence2)
			cpt_sequence2 = cpt_sequence2 - 1
		elif valeur == valeur2 :
			position.append(base_sequence1)
			position.append(base_sequence2)
			cpt_sequence1 = cpt_sequence1 - 1
			cpt_sequence2 = cpt_sequence2 - 1
		elif valeur == valeur3 :
			position.append(base_sequence1)
			position.append("-")
			cpt_sequence1 = cpt_sequence1 -1
		liste_alignement.append(position) 
	identite = 0
	substitution = 0
	gap = 0
	for position in liste_alignement :
		if position[0] == position[1] :
			identite = identite + 1
		elif position[0] != position[1] and position[0] != '-' and position[1] != '-' :
			substitution = substitution + 1
		elif position[0] == "-" or position[1] == "-" :
			gap = gap + 1
	identite = (identite*100/len(liste_alignement))#nombre de positions identiques sur le nombre de positions total de l'alignement
	substitution = (substitution*100/len(liste_alignement))#nombre de positions avec substitution sur le nombre de positions total de l'alignement
	gap = (gap*100/len(liste_alignement))#nombre de positions avec gap sur le nombre de position total de l'alignement
	with open(nomFichier, "w") as fichier :
		fichier.write(str(date))
		fichier.write("\n\n********Resultats de l'alignement********\n\n\n")
		fichier.write("Sequence 1 : "+sequence1+"\nLongueur sequence 1 : "+str(len(sequence1))+" nucleotides\n\n"+"Sequence 2 : "+sequence2+"\nLongueur sequence 2 : "+str(len(sequence2))+" nucleotides\n\n")
		fichier.write("Penalite d'identite : "+str(penaliteIdentite)+"\nPenalite de substitution : "+str(penaliteSubstitution)+"\nPenalite de gap : "+str(penaliteGap)+"\n\n")
		if methode == "mini" :
			fichier.write("Methode de distance\n\n")
		elif methode == "maxi" :
			fichier.write("Methode par similarite\n\n")
		fichier.write("*****************************************\n\n")
		fichier.write("Score de l'alignement : "+str(matrice[len(sequence2)][len(sequence1)])+"\n\n")
		fichier.write("Pourcentage d'identite : "+str(identite)+" % \n")
		fichier.write("Pourcentage de substitution : "+str(substitution)+" % \n")
		fichier.write("Pourcentage de gap : "+str(gap)+" % \n\n")
		fichier.write("*****************************************\n\n")
		fichier.write("Alignement : \n\n")
		nombre_de_positions = len(liste_alignement)
		compteur_affichage = 1
		while (compteur_affichage < nombre_de_positions) : 
			valeur_entree = compteur_affichage
			fichier.write("seq1\n")
			fichier.write(str(valeur_entree)+"\n")
			while (compteur_affichage%30 != 0 and compteur_affichage < nombre_de_positions) :
				fichier.write(str(liste_alignement[compteur_affichage-1][0])+" ")
				compteur_affichage = compteur_affichage +1
			compteur_affichage = valeur_entree
			fichier.write("\n")
			while (compteur_affichage%30 != 0 and compteur_affichage < nombre_de_positions) :
				fichier.write(". ")
				compteur_affichage = compteur_affichage +1
			compteur_affichage = valeur_entree
			fichier.write("\n")
			while (compteur_affichage%30 != 0 and compteur_affichage < nombre_de_positions) :
				fichier.write(". ")
				compteur_affichage = compteur_affichage +1
			compteur_affichage = valeur_entree
			fichier.write("\n")
			while (compteur_affichage%30 != 0 and compteur_affichage < nombre_de_positions) :
				fichier.write(str(liste_alignement[compteur_affichage-1][1])+" ")
				compteur_affichage = compteur_affichage +1
			fichier.write("\nseq2\n\n\n")
			compteur_affichage = valeur_entree + 30
	fichier.close()
	print("Alignement is done.\nResults are saved in '" + nomFichier + "' file.")

#######################################################################################################################
### Test ##############################################################################################################
#######################################################################################################################

# #test de la fonction alignement_fichier_sortie :
#
# seq1 = "ACGGCTATCGACTCGTGAGTTTTCCCCCTTTAAGTACGGTATCTTTTATTTTTGCTAACTTAAGTACAGTATCTTTTATCCATCAATCCCTATGCATACCTACATAGAAATAAAAGAATCCAAAGGAATCAATTTTTCTTTATACCAGATAATTTATGGAAAATCTATTTAGCATCTCTAGATATTGGAATCCCTTTCTCGGAAATAAAACTAATAAAGAAGAAGAGACGAGAAGTTAGGGTAGGGAGGCAGGTGTTTTGTCTGTAGTGAAAACGATCAAATATCGTGTCGTAGCACCTCCACTACTTTACACCTTCACCGGGACAGACCCAAAGTTAGGCATAATTAAGAACCCTAGCGTCACATGCACGACACGCCCCCCCCCCTTAAATTTCTCTTTCGTTTGGGTCTCTCTAAAAGGTAGTTGAAAACTAAATTTCCCGGGCACTTTTACACTTCTCCATAAATTCAAACTCTTAACTTTATTTT"
# seq2 = "ACGGCTATCGACTCGTGAGTTTTCCCCCTGGCCGGTTCTTTTATTTTTGCTAACTTAAGTACAGTATCTTTTATCCATCAATCCCTATGCATACCTACATAGAAATAAAAGCCCCCGGGCCCCCTTTAACCCCCCGGTCAATTTTTCTTTATACCAGATATTGGCCAACTATTTAGCATCTCTAGATATTGGAATCCCTTTCTCGGAAATAAAACTAATAAAGAAGAAGAGACGAGAAGTTAGGGTAGGGAGGCAGGTGTTTTGTCTGTAGTGAAAACGATCAAATATCGTGTCGTAGCACCTCCACTACTTTACACCTTCACCGGGACAGACCCAAAGTTAGGCATAATTAAGAACCCTAGCGTCACATGCACGACACGTGCTTTGCGTGCTCGGTAAAACCCGGGCCAAAAAAAAATCATTAAATTTCTCTTTCGTTTGGGTCTCTCTAAAAGGTAGTTGAAAACTAAAACCTCCTACACTTCTCCATAAATTCAGACTCTTAACTTAATTTAAT"
# penIdentite = 2
# penSubstitution = -1
# penGap = -1
#
# #execution de la fonction et creation du fichier :
#
# alignement_fichier_sortie(seq1, seq2, penIdentite, penSubstitution, penGap, "maxi", "resultats_alignement.txt")





