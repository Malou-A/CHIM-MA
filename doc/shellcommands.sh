#!/bin/sh


# Sort IDs in decending order by abundance (size= large to small)
cat all_derep.fasta|paste - -| sed 's/size=/size=\t/g'| sort -Vrk2| sed 's/size=\t/size=/g'| tr "\t" "\n" > all_derep_sorted.fasta

