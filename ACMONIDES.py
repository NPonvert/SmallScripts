#import necessities

import re
import xlrd
from Bio import Entrez
from itertools import permutations
Entrez.email = "nathaniel_ponvert@brown.edu"
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML


#define sheets of expression data
wubook = xlrd.open_workbook("/users/NPonvert/Desktop/LabSupplies/DataFiles/WuestWAVG.xls")
wusheet = wubook.sheet_by_index(0)
swbook = xlrd.open_workbook("/users/NPonvert/Desktop/LabSupplies/DataFiles/swansondif.XLS")
swsheet = swbook.sheet_by_index(0) 

#Get Uniprot Number from user

name = raw_input('\nPlease enter the UNIProt ID of your protein: ')
print '\nThank you'

#BLAST entered protein against Arabidopsis genome

print '\nBLASTing {} ...'.format(name)
blastout = "%s.txt" % name
try:
	result_handle = NCBIWWW.qblast('blastp', 'nr', '%s' % name, entrez_query="txid3702[ORGN]")
except Exception:
	pass
try:
	blast_records = NCBIXML.parse(result_handle)
except Exception:
	pass
print '\n\tDone'

#Write hits to table

print '\nWriting hits to table...'
with open(blastout, 'a') as file:
	for record in blast_records:
		for alignment in record.alignments:
			record.alignments.sort(key = lambda align: -max(hsp.score for hsp in align.hsps))
			for hsp in alignment.hsps:
				file.write('\n{}'.format(str(alignment.title)))
				file.write('\t{}'.format(str(hsp.expect)))
				perc = float(hsp.identities) / float(hsp.align_length)
				file.write('\t{}'.format(perc))
print '\n\tDone'

#Define unique files

infile = "%s.txt" % name
outfile = 'RAWOUTPUT.TXT'
outfile1 = 'COLUMBIALONLY.TXT'
outfile2 = 'HEATTREECALLS.TXT'
outfile3 = 'SYNHITS.TXT'
outdict = {}

#Build synergid hits file

with open(outfile3, 'w') as mkfile:
	mkfile.write('synergid expressed loci:')
	
#Read through hits

with open(infile) as file:
	for line in file:
		HitID = re.findall('^gi\|\d*\|\w*\|(.{5,20}?)\|', line)
		Ident = re.findall('.+[\t]([\S]{0,5})', line)
		
#Identify Hits		
		
		if HitID:
			print '\nHit: {}'.format(str(HitID).replace('[','').replace(']','').replace("'",""))
			
#Build lists for accumulated expression data
			
			outlist = []
			outlist2 = []
			
#Fetch entrez file for hit			
			
			VAR = str(HitID).replace('[','').replace(']','').replace("'","")
			try:
				handle = Entrez.efetch(db="protein", id=VAR, rettype="gb", retmode="text")	
			except Exception:
				pass
			
#Identify species, ecotype, and atnumber of hit. Append them to list			
			
			for line in handle:
				species = re.findall('"taxon:([\d]+)"', line)
				atnum = re.findall('\/[lg][oe][cn][ue][s]?[\_]?[t]?[a]?[g]?=".*\_*([Aa][RrTt][Aa\d][LlGg][Yy]?[Dd\d]{0,5}[Rr]?[Aa]?[Ff]?[Tt]?\_?[\d]{0,10})"', line)
				eco = re.findall('/ecotype="(.?)\s*.*"', line)
				if atnum:
					if atnum not in outlist:
						outlist.append(atnum)
				if species:
					outlist.append(species)
				if eco:	
					outlist.append(eco)
				outlist = sorted(outlist)
			outlist.append(HitID)
			outlist.append(Ident)
			
#Find ATnumber in list and determine if columbia ecotype			
			
			for i in outlist:
				atnumber = re.findall('[Aa][Tt]\d[Gg][\d]{5}', str(i))
				if atnumber:
					if 'C' in str(outlist):
						
#Read Wuest data for Columbia Hit						
						
						for i in range(0, wusheet.nrows):
							if wusheet.cell(i,0).value == str(atnumber).replace('[','').replace(']','').replace("'","").upper():
								vals = ('wusy:', wusheet.cell(i,1).value, 'wueg:', wusheet.cell(i,2).value, 'wucc:', wusheet.cell(i,3).value, 'wusp:', wusheet.cell(i,4).value, 'wupo:', wusheet.cell(i,5).value)
								outlist.append(vals)

#Find hits expressed in synergids and write them to new list if applicable

								if wusheet.cell(i,1).value <= 0.05:
									val2 = (wusheet.cell(i,0).value, Ident, 'wsy:', wusheet.cell(i,1).value, 'weg:', wusheet.cell(i,2).value, 'wcc:', wusheet.cell(i,3).value)
									outlist2.append(val2)
									swvals2 = ('diflog:', '{0:.3f}'.format(swsheet.cell(i,3).value), 'difp:', '{0:.3f}'.format(swsheet.cell(i,4).value), 'myb98log:', '{0:.3f}'.format(swsheet.cell(i,6).value), 'myb98p:', '{0:.3f}'.format(swsheet.cell(i,7).value))
									outlist2.append(swvals2)

#Read Swanson data for hit

						for i in range(0, swsheet.nrows):
							if swsheet.cell(i,0).value == str(atnumber).replace('[','').replace(']','').replace("'","").upper():
								swvals = ('diflog:', '{0:.3f}'.format(swsheet.cell(i,3).value), 'difp:', '{0:.3f}'.format(swsheet.cell(i,4).value), 'myb98log:', '{0:.3f}'.format(swsheet.cell(i,6).value), 'myb98p:', '{0:.3f}'.format(swsheet.cell(i,7).value))
								outlist.append(swvals)											

#Define dictionary key as list

			key = str(outlist).replace('[','').replace(']','').replace('(','').replace(')','').replace('\'','').replace(', ','_').replace(' ','_')
			print '\t{}'.format(key)

#Write hit to synergid list if applicable

			related = str(outlist2).replace('u','').replace('[','').replace(']','').replace('(','').replace(')','').replace('\'','').replace(', ','_').replace(' ','_')
			if related != '':
				with open(outfile3, 'r') as readfile:
					if related not in readfile:
						with open(outfile3, 'a') as file:
							file.write('\n{}'.format(str(related)))


#Fetch fasta file for hit

			try:
				l1 = Entrez.efetch(db="protein", id=VAR, rettype="fasta", retmode="text")
			except Exception:
				pass

#Read fasta file append only AA lines as values for keys

			for line in l1:
				if '>' in line:
					outdict[key] = ''
				else:
					line = line.replace('\n','')
					outdict[key] = outdict[key] + line

#Write all hits to bulk output

with open(outfile, 'w') as file:
	for i in outdict.keys():
		file.write('\n>{}\n'.format(i))
		file.write('{}\n'.format(outdict[i]))

#Write columbia hits to Columbia output

with open(outfile1, 'w') as file:
	replist =[]
	for i in outdict.keys():
		atnumber = re.findall('[Aa][Tt]\d[Gg][\d]{5}', str(i))
		atnumber = str(atnumber)
		atnumber = atnumber.upper()
		if atnumber not in replist:
			if '_C_' in i:
				file.write('\n>{}\n'.format(i))
				file.write('{}\n'.format(outdict[i]))
				replist.append(atnumber)
print replist

#Write AT numbers of synergid expressed hits to heatmap entry file

with open(outfile2, 'a') as file:
	for i in outdict.keys():
		atnumber = re.findall('[Aa][Tt]\d[Gg][\d]{5}', i)
		if atnumber:
			if '_C_' in i:
				file.write('\n{}'.format(atnumber).replace('[','').replace(']','').replace("'",""))
		
