#!/usr/bin/python

import argparse

############################## ARGPARSE PART ##################################
usage = 'A program to compare ID names in two fasta files.\
        It will return the number of matches found in the reference file as true\
        positives and the number of ids not found in the reference file as false negatives. '
parser = argparse.ArgumentParser(description=usage)

parser.add_argument(
	'-i',
	dest = 'infile',
	metavar = 'INFILE',
	type = argparse.FileType('r'),
	required = True
	)
parser.add_argument(
	'-r',
	dest = 'referencefile',
	metavar = 'REFERENCE FILE',
	type = argparse.FileType('r'),
	required = True
	)
args = parser.parse_args()


import sys
Inputfile = args.infile
referencefile = args.referencefile

refIds = set()
for line in Inputfile:
    if line.startswith('>'):
            refIds.add(line)



TruePositive = 0
FalsePositive = 0
for line in referencefile:
    if line.startswith('>'):
        if line in refIds:
            TruePositive += 1
        else:
            FalsePositive += 1


print('True positives: {}\n False positives: {}'.format(TruePositive,FalsePositive))
