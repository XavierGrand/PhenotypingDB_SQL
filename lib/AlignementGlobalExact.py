#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from Bio.Seq import Seq
from Bio import SeqIO

#projet HMSN204 : Grand Xavier, Vargas Jessica, Salson Marine

#programme d'alignement par paire exact et global de deux sequences

# parser = ArgumentParser()
# parser.add_argument("seq1", help="Input Sequence 1.")
# parser.add_argument("seq2", help="Input Sequence 2.")
# parser.add_argument("cons", help="Identity score")
# parser.add_argument("sub", help="Substitution score")
# parser.add_argument("gap", help="Gap score")
#
# args = parser.parse_args()

sequence1 = "GGCTGAC" #A passer en arguments
sequence2 = "GATC" #A passer en arguments
penaliteSubstitution = 2 #A passer en arguments
penaliteIdentite = -1 #A passer en arguments
penaliteGap = -1 #A passer en arguments

# seq1 = args.seq1 #A passer en arguments
# seq2 = args.seq2 #A passer en arguments
# cons = args.cons #A passer en arguments
# gap = args.sub #A passer en arguments
# sub = args.gap #A passer en arguments

#1. elaboration d'une matrice en utilisant le principe de programmation dynamique 


#2. etape de backtracking