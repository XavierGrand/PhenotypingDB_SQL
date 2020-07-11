#!/usr/bin/env python3

from Bio import SeqIO

def translate(seq_record) :

    nuc = 0
    nbATG = 0
    nbStop = 0
    noCDS = 0
    listATG = []
    listStop = []
    listCDS = []

    while(nuc+2 <= len(seq_record.seq)): # pas plus long que la seq complete
            if (seq_record.seq[nuc] == 'A' and seq_record.seq[nuc+1] == 'T' and seq_record.seq[nuc+2] == 'G'): #Trouver le 1er ATG
                listATG.append(nuc)
                nbATG += 1
                # print(nuc+1) #Le +1 est du au fait que l'on compte de 0 en info... A stoquer dans une liste
                nuc += 1
            else :
                nuc += 1

    for atg in listATG :
        noCDS += 1
        nuc = atg + 3
        while(not((seq_record.seq[nuc] == 'T' and seq_record.seq[nuc+1] == 'A' and seq_record.seq[nuc+2] == 'A') or
                (seq_record.seq[nuc] == 'T' and seq_record.seq[nuc+1] == 'G' and seq_record.seq[nuc+2] == 'A') or
                (seq_record.seq[nuc] == 'T' and seq_record.seq[nuc+1] == 'A' and seq_record.seq[nuc+2] == 'G'))) :
                nuc += 3
        listCDS.append(seq_record.seq[atg:nuc+3])
        listStop.append(nuc+1)

    print("La séquence contient " + str(nbATG) + " codons Start.")
    print(listCDS)
    print(listStop)

    for cds in listCDS :
        print(cds.translate(table='Standard', stop_symbol='*'))