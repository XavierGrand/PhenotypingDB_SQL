# Project_HMSN204
Version : 1.0.0

5th may 2020.

## Authors:
Xavier Grand, Marine Salson & Jessica Vargas,
Master SNS parcours BCD 2019-2020,
Faculté des Sciences, Université de Montpellier.

## Summary:
The executable programs aim to respond to the instructions of an educational project included in the module HMSN204.
The project is dedicated to the development of a program to create, manage and request a data base.
It contains phenotyping data of *Arabidopsis thaliana* WT and mutant plants, produced by Master BFP students.
The program is divided in two operational elements :

  * MainCreationDB.py is designed to create and request the relational database
  * MainSequenceAnalyzer.py allows to performe sequence traitments

## Technologies
  - Developed in python 3.6.9
  - It is an EDUCATIONAL project, it is better to use professional software

## Installation

Source code is available on repository at :

``
https://gitlab.info-ufr.univ-montp2.fr/e20140041678/projet_HMSN204.git
``

## Usage

### Creation DB :

    usage: MainCreationDB.py [-h] [-cr] [-rqex] [-rq] inputFile dbname
    
    positional arguments:
      inputFile             Phenotyping results in csv file properly formated in
                            ./Datasets/ folder. ex : 'Data_Projet_Entete.csv'

      dbname                Name of the Data Base
    
    optional arguments:
      -h, --help            show this help message and exit
      -cr, --create         To create the Data Base, manager only
      -rqex, --requestexample
                            To send example requests on existing Data Base
      -rq, --request        To send a request on existing Data Base

### Sequence Analyzer :

    usage: MainSequenceAnalyzer.py [-h] [-al] [-bl] gene mutant db
    
    positional arguments:
      gene          Wild type gene name. ex : 'NRT2'
      mutant        Mutant name. ex : 'nrt2.5'
      db            Database to request : 'nucleotide' or 'protein'
    
    optional arguments:
      -h, --help    show this help message and exit
      -al, --align  To perform WT versus mutant sequences
      -bl, --blast  To Blast mutant sequence on NBCI Blastn portal

## To do

 - Improvement of the database structure
 - Tests to be carried out on larger volume of data
 - Optionnal parameters

# License

**Free Software, open source.**