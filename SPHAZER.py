#Import necessities
import os
import re
from Bio import Entrez
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
Entrez.email = "nathaniel_ponvert@brown.edu"

#Initial stuff
SPHdict = {}
genomes = ['txid3702[ORGN]','txid59689[ORGN]','txid4081[ORGN]','txid39947[ORGN]','txid13333[ORGN]','txid3218[ORGN]']
#genomes = ['txid3702[ORGN]']
#Read fasta to dictionary
with open('SPHlist.txt') as file:
	for line in file:
		line = line.strip()
		if line.startswith('>'):
			key = line
			SPHdict[key] = ''
		else:
			SPHdict[key] = SPHdict[key] + line

#Read through genomes
for a in genomes:
	
#make a directory for each genome
	os.makedirs(a)
	os.chdir(a)
	outfile = "%s.fas" % a
#iterate through dictionary items	
	for key,val in SPHdict.iteritems():
		
#blast each dictionary item against the current genome	
		print '\tBlasting', key, 'against', a
		blastout = "%s.txt" % a
		try:
			result_handle = NCBIWWW.qblast('blastp', 'nr', '%s' % val, 'FALSE', entrez_query='%s' % a)
		except Exception:
			continue
		try:
			blast_records = NCBIXML.parse(result_handle)
		except Exception:
			continue

#write results to blast hit table
		with open(blastout, 'a') as file:
			for record in blast_records:
				if record.alignments:
					record.alignments.sort(key = lambda align: -max(hsp.score for hsp in align.hsps))
					file.write('\n{}'.format(str(record.alignments[0])))
					print record.alignments[0]		

#make a final dictionary and assorted key list
		outdict = {}
		outlist1 = []
		
#read blast hit table and append HitID and identity values to new list		
		with open(blastout) as file:
			for line in file:
				HitID = re.findall('^gi\|\d*\|\w*\|(.{5,20}?)\|',line)
				Ident = re.findall('\|.(\d*[.]{1}[\d]{3})', line)
				if HitID:
					if HitID not in outlist1:
						outlist1.append(HitID)
		print '\n{}\n'.format(outlist1)
	
#read through new list	
	for i in outlist1:
		print i

#make new fasta for each HitID		
		var = str(i).replace('[','').replace(']','').replace("'","")
		print var
		try:
			l1 = Entrez.efetch(db="protein", id=var, rettype="fasta", retmode="text")
		except Exception:
			pass
		with open(outfile, 'a') as file:
			file.write(l1.read())
		with open(outfile) as file:	
			for line in file:
				if '>' in line:
					line = line.replace(' ','')
	os.chdir('..')
		
		
# 		print l1.read()
# 		for line in l1:
# 			if '>' in line:
# 				outdict[var] = ''
# 			else:
# 				line = line.replace('\n','')
# 				outdict[var] = outdict[var] + line
# 	print outdict
# 	
# #Write fasta to file	
# 	outfile = "%s.TXT" % a
# 	with open(outfile, 'w') as file:
# 		for i in outdict.keys():
# 			print i
# 			file.write('\n>{}\n'.format(i))
# 			file.write('{}\n'.format(SPHdict[i]))
# 	os.chdir('..')
# 		

		