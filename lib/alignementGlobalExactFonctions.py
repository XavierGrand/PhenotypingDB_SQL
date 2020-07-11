#!/usr/bin/env python

#Projet HMSN204 : Grand Xavier, Vargas Jessica, Salson Marine, M1 BCD

#Ce programme contient une fonction permettant l'alignement par paire exact et global de deux sequences, selon la methode de Needleman & Wunsch (1970).
#L'alignement se fait en utilisant le principe de la programmation dynamique, 
#et passe par l'elaboration d'une matrice comportant les scores des sous-alignements intermediaires.


#les fonctions minimum ou maximum ci-dessous sont utilisees lors du remplissage de la matrice de scores (ligne 79).
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
# 3. 4. et 5. : les valeurs utilisees des penalites d'identite, de substitution et de gap, respectivement
# 6. la fonction utilisee lors de la creation de la matrice, selon si une methode de distance (fonction minimum), ou de similarite (fonction maximum) est utilisee
# 7. la liste, initialisee a l'exterieur, qui sera remplie et modifiee par la fonction et qui correspondra a la matrice de scores des sous-alignements intermediaires.
# Passer cette liste en parametre permet ensuite d'y acceder et de pouvoir xl'afficher.

# La fonction alignement retourne une liste de tuples, qui correspond a l'alignement des deux sequences.

def alignement(sequence1, sequence2, penaliteIdentite, penaliteSubstitution, penaliteGap, methode, matrice) :

	# ************* 1. Elaboration de la matrice : ************** 

	#La matrice est une liste de listeS :
	#elle est passee en argument, et doit donc etre initialisee a l'exterieur de la fonction,
	#et elle est remplie ligne par ligne.
	#Pour chaque ligne de la matrice, une nouvelle liste est cree, nommee liste_j.
	#Le remplissage de la premiere ligne, ne depend que de la valeur de la penalite de gap et du numero de colonne :
	liste_j = [] #la liste_j est la premiere ligne de la matrice
	cpt = 0 #le compteur cpt correspond a chaque numero de colonne de la matrice, il n'est utilise que pour la premiere ligne
	#ce compteur permet de remplir la premiere ligne, en fonction de la penalite de gap et de l'indice de la colonne
	liste_j.append(cpt * penaliteGap) 
	for base_1 in sequence1 : #remplissage du reste de la premiere ligne
		cpt = cpt + 1
		liste_j.append(cpt * penaliteGap)
	matrice.append(liste_j) #la liste_j, correspondant ici a la premiere ligne de la matrice, est ajoutee a cette derniere
	cpt_i = 1 #le compteur cpt_i correspond a chaque numero de LIGNE de la matrice, ici, la ligne 0 est deja remplie, cpt_i commence donc a 1
	for base_2 in sequence2 : #parcours de la sequence2, et remplissage de chaque ligne
		liste_j = [] #la liste_j est la ligne de la matrice a l'indice i
		liste_j.append(cpt_i * penaliteGap) #remplissage du premier element de la ligne : celui-ci ne depend que de l'indice de la ligne et de la penalite de gap
		cpt_j = 0 #le compteur cpt_j correspond a chaque numero de COLONNE de la matrice
		for base_1 in sequence1 : #remplissage du reste de la ligne, en parcourant la sequence1
			valeur = 0 #cette variable correspond a la valeur qui sera ajoutee a la liste liste_j a chaque position
			#trois possibilite de valeur sont testees : dans une methode par distance, la valeur minimale est conservee, dans une methode par similarite, la valeur maximale est conservee
			if base_2 != base_1 : #si les deux bases sont differentes (cas d'une substitution)
				valeur_1 = matrice[cpt_i-1][cpt_j] + penaliteSubstitution
			else : #si les deux bases sont identiques
				valeur_1 = matrice[cpt_i-1][cpt_j] + penaliteIdentite
			valeur_2 = matrice[cpt_i-1][cpt_j + 1] + penaliteGap
			valeur_3 = liste_j[cpt_j] + penaliteGap
			valeur = methode(valeur_1, valeur_2, valeur_3) #methode correspond soit a la fonction minimum, soit maximum
			liste_j.append(valeur) #la ligne en cours, correspondant a la liste_j, est remplie au fur et a mesure que la sequence1 est parcourue
			cpt_j = cpt_j + 1
		matrice.append(liste_j) #la ligne correspondant a la list_j est ajoutee a la matrice, a chaque base de la sequence2 parcourue
		cpt_i = cpt_i + 1 

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
		valeur = methode(valeur1, valeur2, valeur3) #selon la methode choisie, la fonction minimum, ou maximum est utilisee
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
			valeur = methode(valeur_1, valeur_2, valeur_3)
			liste_j.append(valeur) 
			cpt_j = cpt_j + 1
		matrice.append(liste_j)
		cpt_i = cpt_i + 1 
	return matrice

#Fonctions permettant de renvoyer le resultats de l'alignement dans un fichier dont on peut choisir le nom :

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
		valeur = methode(valeur1, valeur2, valeur3)
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

def alignement_fichier_sortie(sequence1, sequence2, penaliteIdentite, penaliteSubstitution, penaliteGap, methode, nomFichier) :
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
			valeur = methode(valeur_1, valeur_2, valeur_3) 
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
		valeur = methode(valeur1, valeur2, valeur3) 
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
		fichier.write("\n\n********Resultats de l'alignement********\n\n\n")
		fichier.write("Sequence 1 : "+sequence1+"\nLongueur sequence 1 : "+str(len(sequence1))+" nucleotides\n\n"+"Sequence 2 : "+sequence2+"\nLongueur sequence 2 : "+str(len(sequence2))+" nucleotides\n\n")
		fichier.write("Penalite d'identite : "+str(penaliteIdentite)+"\nPenalite de substitution : "+str(penaliteSubstitution)+"\nPenalite de gap : "+str(penaliteGap)+"\n\n")
		if methode == minimum :
			fichier.write("Methode de distance\n\n")
		elif methode == maximum :
			fichier.write("Methode par similarite\n\n")
		fichier.write("*****************************************\n\n")
		fichier.write("Score de l'alignement : "+str(matrice[len(sequence2)][len(sequence1)])+"\n\n")
		fichier.write("Pourcentage d'identite : "+str(identite)+" % \n")
		fichier.write("Pourcentage de substitution : "+str(substitution)+" % \n")
		fichier.write("Pourcentage de gap : "+str(gap)+" % \n\n")
		fichier.write("*****************************************\n\n")
		fichier.write("Alignement : \n\n")
		fichier.write("seq1\n")
		for position in liste_alignement :
			fichier.write(str(position[0])+" ")
		fichier.write("\n")
		for position in liste_alignement :
			fichier.write(". ")
		fichier.write("\n")
		for position in liste_alignement :
			fichier.write(". ")
		fichier.write("\n")
		for position in liste_alignement :
			fichier.write(str(position[1])+" ")
		fichier.write("\nseq2\n\n")
	return liste_alignement


# Exemples d'utilisation de la fonction alignement :

# deux elements sont accessibles :
 
# 1. la MATRICE de scores : elle correspond a une liste initialisee en dehors de la fonction, et passee en dernier parametre
# cette liste est remplie lors de l'execution de la fonction, et est affichable de la maniere realisee aux lignes 215 et 237

# 2. la liste correspondant a l'ALIGNEMENT des deux sequences : cette liste est retournee par la fonction, et correspond a une liste de tuples
# afin de rendre l'alignement lisible, celle-ci doit etre affichee de la maniere realisee aux lignes 211 et 233

#test 1 :

print("\nTest 1, page 30 du CM, methode de similarite :\n")
seq1 = "ACGGCTATC" 
seq2 = "ACTGTAATG" 
penIdentite = 2 
penSubstitution = -1 
penGap = -1 
matrice_1 = []

#execution de la fonction :
#alignement(seq1, seq2, penIdentite, penSubstitution, penGap, maximum, matrice_1)

#affichage de l'alignement : 
for position in alignement(seq1, seq2, penIdentite, penSubstitution, penGap, maximum, matrice_1) :
	print position
print("\n")
#affichage de la matrice de scores :
for ligne in matrice_1 :
	print ligne 

#test 2 :

print("\nTest 2, ex1 du TD1, methode de distance :\n")
seq1 = "GGCTGAC" 
seq2 = "GATC" 
penIdentite = 0 
penSubstitution = 3
penGap = 3
matrice_2 = []

#execution de la fonction :
#alignement(seq1, seq2, penIdentite, penSubstitution, penGap, minimum, matrice_2)

#affichage de l'alignement : 
for position in alignement(seq1, seq2, penIdentite, penSubstitution, penGap, minimum, matrice_2) :
	print position
print("\n")
#affichage de la matrice de scores :
for ligne in matrice_2 :
	print ligne

#test de la fonction matrice : 
#print("test fonction matrice :")
#for ligne in matrice(seq1, seq2, penIdentite, penSubstitution, penGap, minimum) :
#	print(ligne)

#test de la fonction backtracking : 
#print("test fonction backtracking :")
#for position in backtracking(seq1, seq2, penIdentite, penSubstitution, penGap, minimum, matrice_2) :
#	print(position)

#test de la fonction alignement_fichier_sortie :

seq1 = "ACGGCTATCGACTCGTGAGTTTTCCCCCTTTAAGTACGGTATCTTTTATTTTTGCTAACTTAAGTACAGTATCTTTTATCCATCAATCCCTATGCATACCTACATAGAAATAAAAGAATCCAAAGGAATCAATTTTTCTTTATACCAGATAATTTATGGAAAATCTATTTAGCATCTCTAGATATTGGAATCCCTTTCTCGGAAATAAAACTAATAAAGAAGAAGAGACGAGAAGTTAGGGTAGGGAGGCAGGTGTTTTGTCTGTAGTGAAAACGATCAAATATCGTGTCGTAGCACCTCCACTACTTTACACCTTCACCGGGACAGACCCAAAGTTAGGCATAATTAAGAACCCTAGCGTCACATGCACGACACGCCCCCCCCCCTTAAATTTCTCTTTCGTTTGGGTCTCTCTAAAAGGTAGTTGAAAACTAAATTTCCCGGGCACTTTTACACTTCTCCATAAATTCAAACTCTTAACTTTATTTT" 
seq2 = "ACGGCTATCGACTCGTGAGTTTTCCCCCTGGCCGGTTCTTTTATTTTTGCTAACTTAAGTACAGTATCTTTTATCCATCAATCCCTATGCATACCTACATAGAAATAAAAGCCCCCGGGCCCCCTTTAACCCCCCGGTCAATTTTTCTTTATACCAGATATTGGCCAACTATTTAGCATCTCTAGATATTGGAATCCCTTTCTCGGAAATAAAACTAATAAAGAAGAAGAGACGAGAAGTTAGGGTAGGGAGGCAGGTGTTTTGTCTGTAGTGAAAACGATCAAATATCGTGTCGTAGCACCTCCACTACTTTACACCTTCACCGGGACAGACCCAAAGTTAGGCATAATTAAGAACCCTAGCGTCACATGCACGACACGTGCTTTGCGTGCTCGGTAAAACCCGGGCCAAAAAAAAATCATTAAATTTCTCTTTCGTTTGGGTCTCTCTAAAAGGTAGTTGAAAACTAAAACCTCCTACACTTCTCCATAAATTCAGACTCTTAACTTAATTTAAT" 
penIdentite = 2 
penSubstitution = -1 
penGap = -1 

#execution de la fonction et creation du fichier :
 
alignement_fichier_sortie(seq1, seq2, penIdentite, penSubstitution, penGap, maximum, "resultats_alignement.txt") 





