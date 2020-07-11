#!/usr/bin/env python3

# API pour réaliser une recherche sur NCBI via Entrez

from Bio import SeqIO
from Bio import Entrez

def EntrezFct(gene, mutant, db) :

    # demande d'adresse courriel pour requete entrez :

    Entrez.email = "default@email.com" #Pour ne pas avoir à remplir a chaque test, j'ai mis une adresse générique

    # print("Please, could you give an email address ?")
    # email = str(input())
    # print(email)
    #
    # Entrez.email = email

    # Entrez parameters : pour la séquence de référence.
    # db = "nucleotide" # ou argument
    organism = "\"Arabidopsis thaliana\"" # ou argument
    prop = "biomol_mrna" # prevoir conditionnelle en cas de proteine
    # gene = "NRT2" #args
    # gene = "SEX1"
    # mutant = "nrt2.5"

    #Le gène WT :

    request = Entrez.esearch(db = db, term = organism + "[orgn] AND "+ prop + " [PROP] AND " + gene + "[Gene Name]", retmax = 1)
    res = Entrez.read(request)
    # print(organism + "[orgn] AND "+ prop + " [PROP] AND " + gene + "[Gene Name]")
    # print(res["Count"])
    # print(res["IdList"])
    # print(res["Description"])
    with Entrez.efetch(
        db=db, rettype="fasta", retmode="text", id=res["IdList"]
        ) as handle:
            seq_record = SeqIO.read(handle, "fasta")
    print(seq_record)
    print(len(seq_record.seq))

    seq1 = seq_record

    handle.close()

    # le gène muté :

    request = Entrez.esearch(db = db, term = organism + "[orgn] AND "+ prop + " [PROP] AND " + mutant + "[Gene Name]", retmax = 1)
    res = Entrez.read(request)
    # print(organism + "[orgn] AND "+ prop + " [PROP] AND " + mutant + "[Gene Name]")
    # print(res["Count"])
    # print(res["IdList"])
    # print(res["Description"])
    with Entrez.efetch(
        db=db, rettype="fasta", retmode="text", id=res["IdList"][0]
        ) as handle:
            seq_record2 = SeqIO.read(handle, "fasta")
    print(seq_record2)
    print(len(seq_record2.seq))

    seq2 = seq_record2

    handle.close()

    return seq1, seq2