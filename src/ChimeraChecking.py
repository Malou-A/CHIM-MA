#!/usr/bin/python 3
import argparse
import platform
import sys
import statistics as stat
############################## ARGPARSE PART ##################################
usage = 'Tool to detect chimeric sequences, the program will compare sequences\
		of less abundance with higher abundance sequences. Beginning and end of \
		a sequence will be compared, if threshold similarity is fulfilled, the sequence will\
		be classified as a chimera sequence. The user may choose threshold for similarity,\
		and the minimum proportion of the parent sequences.\
		Default is set to 100% identical regions, with the minimum proportion 10/90'
parser = argparse.ArgumentParser(description=usage)
parser.add_argument(
	'-v',
	'--version',
	action = 'version',
	version = '%(prog)s 1.0'
	)
parser.add_argument(
	'-i',
	dest = 'infile',
	metavar = 'INFILE',
	type = argparse.FileType('r'),
	required = True
	)
parser.add_argument(
	'-n',
	'--nochimeras',
	dest = 'nochimera',
	metavar = 'OUTFILE',
	type = argparse.FileType('w'),
	required = True
	)
parser.add_argument(
	'-c',
	'--chimeras',
	dest = 'chimeras',
	metavar = 'OUTFILE',
	type = argparse.FileType('w'),
	required = True
	)
parser.add_argument(
	'-s',
	dest = 'seqregion',
	type = float,
	help = 'starting region for checking similarity of sequences (default 0.1 (10%% of sequence length))',
	default = 0.1
	)
parser.add_argument(
	'-t',
	dest = 'threshold',
	type = float,
	help = 'Treshold for similarity of sequences (default = 1.0)',
	default = 1.0
	)

args = parser.parse_args()

###############################################################################
Inputfile = args.infile
chimfile = args.chimeras
nochimfile = args.nochimera
thresh = args.threshold


sequences = []
Ids = []
for line in Inputfile:
	if line.startswith('>'):   # Storing the sequences and IDs to lists
		ID = line
		Ids.append(ID)
	else:
		line = line.rstrip()
		sequences.append(line)

Seq_length = stat.mean(len(x) for x in sequences)
s_thresh = int(round(args.seqregion*Seq_length))  #Calculating the length of the first region of comparison w.r.t the chosen threshold

def compare(seq1,seq2):
    count = 0.00
    for i in range(len(seq1)):			# Function do determine similarity of 2 sequences or 2 sequence regions
        if seq1[i]==seq2[i]:
            count += 1
    return(count/len(seq1))

def countfunction_forw(seqlist, seqID):
	countlist = []
	for seq in seqlist:
		count = 0
		countindex = 1
		for j in range(len(seq)):
			try:
				if seq[j] == seqID[j]:		# Function to calculate similarity for sequences in the forward list
					count += 1
				if count/countindex < thresh: # After each nucleotide, the current similarity is checked against the threshold
					countlist.append(count)	  # to determine wether to break the function or not.
					break
				countindex += 1
			except:
				countlist.append(count)
				break
	return(countlist)


def countfunction_rew(seqlist, seqID): # Same as above but for the reverse sequence.
	countlist = []
	for seq in seqlist:
		count = 0
		countindex = 1
		for j in range(1,len(seq)+1):
			try:
				if seq[-j] == seqID[-j]:
					count += 1
				if count/countindex < thresh:
					countlist.append(count)
					break
				countindex +=1
			except:
				countlist.append(count)
				break
	return(countlist)

def valfor(forw_counts,rew_counts):
	for val in forw_counts:				# Adding values in the two countlists together and
		for r_vals in rew_counts:		# determining if the sequence is chimeric or not
			if (Seq_length - (val+r_vals)) < 1: # Overlapping allowed, but not shorter regions than seq length
					return(True)
	return(False)


chimerasadded = []
database = []
databaseids = []
for i in range(len(sequences)):						# Here, each sequence is analyzed one by one
	chim_forw_IDs = []								# If the sequence is not chimeric, it will be added
	chim_forw_sequences = []						# To the databaselist. Each sequence is compared to the sequences
	chim_rew_IDs = []								# in the database, except the first two.
	chim_rew_sequences = []
	for j in range(len(database)):
			if len(sequences[i])< Seq_length-(Seq_length*0.3):  # If the sequence is shorter or longer than average, it will also
				chimfile.write('{}{}\n'.format(Ids[i],sequences[i]))# be considered an artifact (chimeric).
				break
			if len(sequences[i])> Seq_length+(Seq_length*0.3):
				chimfile.write('{}{}\n'.format(Ids[i],sequences[i]))
				break
			seq1f = sequences[i][:s_thresh]
			seq2f = database[j][:s_thresh]
			seq1r = sequences[i][-s_thresh:]  # First regions of sequence assigned
			seq2r = database[j][-s_thresh:]
			treshf = compare(seq1f,seq2f)	  # Comparing the regions with the comparefunction
			treshr = compare(seq1r,seq2r)
			if treshf >= thresh:			  # If threshold is fulfilled, sequence stored for further analysis
				chim_forw_sequences.append(database[j])
				chim_forw_IDs.append(databaseids[j])
			if treshr >= thresh:
				chim_rew_sequences.append(database[j])
				chim_rew_IDs.append(databaseids[j])
	if len(chim_rew_IDs) > 0 and len(chim_forw_IDs) > 0: # If matches found in both beginning and end of sequence, further analysis is done
		forw_counts = countfunction_forw(chim_forw_sequences, sequences[i])
		rew_counts = countfunction_rew(chim_rew_sequences, sequences[i])
		if valfor(forw_counts, rew_counts) == True:  #Classification step
			chimfile.write('{}{}\n'.format(Ids[i],sequences[i]))
		else:
			database.append(sequences[i])
			databaseids.append(Ids[i]) # If not classified as chimera, add sequence to database, and write to file.
			nochimfile.write('{}{}\n'.format(Ids[i],sequences[i]))
	else:
		database.append(sequences[i])
		databaseids.append(Ids[i])
		nochimfile.write('{}{}\n'.format(Ids[i],sequences[i]))
