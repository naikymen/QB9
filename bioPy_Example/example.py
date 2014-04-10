# coding=utf-8
__author__ = 'naikymen'
from Bio import Seq
from Bio import SeqIO
from Bio import Entrez
from Bio.Blast import NCBIWWW

#Entrez usage example
Entrez.email = "nico.fruta@gmail.com"
handle = Entrez.efetch(db="nucleotide", id="57240072", rettype="gb", retmode="text")
print(handle.readline().strip(), "\n")

#Bioseq usage example
my_seq = Seq.Seq('CATGTAGACTAG')  # create a sequence object

#print out some details about it
print("seq %s is %i bases long" % (my_seq, len(my_seq)))
print("reverse complement is %s" % my_seq.reverse_complement())
print("protein translation is %s" % my_seq.translate())