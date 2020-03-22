#!/usr/bin/python
from random import randint
import random
import sys
import argparse

############################## ARGPARSE PART ##################################
usage = 'This program will create a set of imaginary sequences of choosen length\
        and out of these sequences create chimera sequences. Choices to be made are\
        the length of the sequences (all sequences will be the same length), the \
        minimum similarity (the chosen value will represent the least similar sequences,\
        but also allowing for more similar sequences by chance), and how many sequences\
        to be generated. If you want chimeric sequences, add how many percentages of the\
        sequences that should be chimeric, or leave option blanc for no chimera sequences.'
parser = argparse.ArgumentParser(description=usage)
parser.add_argument(
	'-v',
	'--version',
	action = 'version',
	version = '%(prog)s 1.0'
	)
parser.add_argument(
	'-o',
	dest = 'outfile',
	metavar = 'OUTFILE',
	type = argparse.FileType('w'),
	required = True
	)
parser.add_argument(
    '-c',
    dest = 'chimerafile',
    metavar = 'OUTFILE',
    type = argparse.FileType('w'),
    help = 'Name an outputfile if you want a separate file with only chimeras.'
    )
parser.add_argument(
	'-n',
	dest = 'sequences',
    type = int,
	default = 100,
    help = 'Choose how many sequences you want to generate (default 100)'
	)
parser.add_argument(
	'-l',
    type = int,
	dest = 'length',
    help = 'Set length of the sequences (default = 253)',
	default = 253
	)
parser.add_argument(
	'-p',
	dest = 'percentage',
	type = float,
	help = 'How many percentages should be chimeric sequences, choose value between 0 and 1 (default = 0)',
	default = 0
	)
parser.add_argument(
	'-s',
	dest = 'similarity',
	type = float,
	help = 'Similarity of sequences, choose a value between 0-1 (default = 0)',
	default = 0
	)

args = parser.parse_args()


################################################################################

Seq_length = args.length
Sequences = args.sequences
Chimera_count  = int(round(args.percentage*Sequences))
similarity = args.similarity
outfile = args.outfile
chimerafile = args.chimerafile
Insertions = int(round((Seq_length*(1-similarity))/2))

# Creating a random generated sequence
# and make a list of desired number of the sequence
Nucleotides = ['A','C','G','T']
seq = ''
for i in range(Seq_length):
    seq += random.choice(Nucleotides)
seq = list(seq)

proportions = [.1,.2,.3,.4,.5,.6,.7,.8,.9]

seq_dict={}
sizelist = random.sample(xrange(1,Sequences*200),Sequences+Chimera_count+1)
sizelist.sort(reverse = True)
index = 1
for i in range(Sequences):
    ID = '>ID_{};size={}'.format(i+1,sizelist[index])
    current_sequence = seq[:]
    for j in range(Insertions):
        pos = randint(0,len(current_sequence)-1)
        nuc = random.choice(Nucleotides)
        current_sequence[pos]=nuc
    seq_dict[ID]=''.join(current_sequence)
    outfile.write('{}\n{}\n'.format(ID,''.join(current_sequence)))
    index += 1
for i in range(Chimera_count):
    ID1 = random.choice(seq_dict.keys())
    ID2 = random.choice(seq_dict.keys())
    if ID1==ID2:
        while ID1 == ID2:
            ID2 = random.choice(seq_dict.keys())
    prop = random.choice(proportions)
    seq1 = seq_dict[ID1]
    seq2 = seq_dict[ID2]
    seq_len = len(seq1)
    slice_pos = int(round(seq_len*prop))
    seq1 = seq1[:slice_pos]
    seq2 = seq2[slice_pos:]
    chim_seq = seq1+seq2
    chim_ID = '>Chim_ID_{}'.format(i)
    outfile.write('{}size={}\n{}\n'.format(chim_ID,sizelist[index],chim_seq))
    if args.chimerafile:
        chimerafile.write('{}size={}\n{}\n'.format(chim_ID,sizelist[index],chim_seq))
    index +=1
