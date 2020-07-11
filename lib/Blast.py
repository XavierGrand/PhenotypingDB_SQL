#!/usr/bin/env python3

from Bio.Blast import NCBIWWW
from Bio import SeqIO
from Bio.Blast import NCBIXML

def blast(seq_record) : # seq_record) :

    print("\nStart Blast...")
    print("Please wait...")

    filename = "./Resultats/" + seq_record.id + "_Blast_nucleotide.xml"

    ### Blast NCBI online :

    result_handle = NCBIWWW.qblast("blastn", "nt", seq_record.format('fasta'))
    with open(filename, 'w') as save_file:
        blast_results = result_handle.read()
        save_file.write(blast_results)
    save_file.close()

    ### Human message :

    print("Blast is complete.")
    print("\nParsing blast results.")
    print("Please wait...")

    ### Parsing Blast results :

    fh = open(filename)
    blastRecord = NCBIXML.read(fh)

    print("All results are saved in '" + filename + "' file.\n")

    print("\nHow many results would you print ?") # Cas de nombre trop grand pas géré
    print("Type a number and press Enter.")

    nbres2print = int(input())

    if (nbres2print > 0):
        print("\nBest Blast result(s) :")
        print("Query : " + blastRecord.query)
        print("Query length : " + str(blastRecord.query_length))

        for i in range(nbres2print):
            print("\nHit n°" + str(i + 1))
            print("Subject : " + str(blastRecord.alignments[i].title))
            print("Subject length : " + str(blastRecord.alignments[i].length))
            # print(str(blastRecord.alignments[0].hsps[0]))
