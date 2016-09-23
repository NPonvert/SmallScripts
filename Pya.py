#import necessities
print '\nImporting necessities...'
import os
import shutil
import re
import xlrd
from Bio import Entrez
Entrez.email = "nathaniel_ponvert@brown.edu"
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
print '\nDone'

#define sheets for Brontes
print '\nDefining sheets for Brontes...\n'
wubook = xlrd.open_workbook("/users/NPonvert/Desktop/LabSupplies/DataFiles/WuestWAVG.xls")
wusheet = wubook.sheet_by_index(0)
swbook = xlrd.open_workbook("/users/NPonvert/Desktop/LabSupplies/DataFiles/swansondif.XLS")
swsheet = swbook.sheet_by_index(0) 
print 'Done\n'

#File for Arges
arges = 'ARGES.TXT'
with open(arges, 'w') as mkfile:
	mkfile.write('Value error calls from SteropesBrontes:\n')

#check test hits against ctrl hits

book = xlrd.open_workbook('/users/NPonvert/Desktop/ThiCOIPTrip/Pya13results/RESULTS.xlsx')
sheet = book.sheet_by_index(0)

thione, thitwo, thithree, wat = ([] for i in range(4))
for i in range(1, sheet.nrows):
	thione.append(sheet.cell(i,0).value)
	thitwo.append(sheet.cell(i,1).value)
	thithree.append(sheet.cell(i,2).value)
	wat.append(sheet.cell(i,3).value)
	wat.append(sheet.cell(i,4).value)
	wat.append(sheet.cell(i,5).value)
onetwothree = []
onetwo = []
twothree = []
onethree = []


with open('onethree.txt', 'a+') as file:
	for i in thione:
		if i in thithree:
			if i not in wat:
				if i not in onethree:
					onethree.append(i)
	for i in onethree:	
		file.write('\n{}'.format(i))

#make a directory for the unique hit and navigate into it	
for i in onethree:
	name = []
	try:
		name_handle = Entrez.efetch(db="protein", id='%s' % i, rettype="gb", retmode="text")
	except Exception:
		continue
	name = []
	result = name_handle.read()
	result = result.replace('\n','')
	product = re.findall('.*\/product="(.+?)"', result, re.MULTILINE)
	product = str(product).replace(' ','')
	atnum = re.findall('\/[lg][oe][cn][ue][s]?[\_]?[t]?[a]?[g]?=".*\_*([Aa][RrTt][Aa\d][LlGg][Yy]?[Dd\d]{0,5}[Rr]?[Aa]?[Ff]?[Tt]?\_?[\d]{0,10})"', result)
	name.append(atnum)
	name.append(product)
	name = str(name).replace('[','').replace(']','').replace('(','').replace(')','').replace('\'','').replace(', ','_').replace(' ','_')
	print '\t{} is unique.'.format(name)		
	print '\tMaking a directory for {}...'.format(name)
   	os.makedirs(name)
	print '\tDone'
	print '\tMoving to directory {}...'.format(name)
	os.chdir(name)
	print '\tDone'

#begin Steropes
	print '\nStarting Steropes...\n'

#Summary File
	SUMMARYFILE = "%s.txt" % name
	with open(SUMMARYFILE, 'w') as file:
		file.write(Entrez.efetch(db="protein", id='%s' % i, rettype="gb", retmode="text").read())

#blast SPH hit and make xml file for hits
	print '\tBLASTing {}...'.format(name)
	blastout = "%s.txt" % i
	try:
		result_handle = NCBIWWW.qblast('blastp', 'nr', '%s' % i, 'FALSE', entrez_query="txid3702[ORGN]")
	except Exception:
		print '\n\t{} requires Arges.\n'.format(i)			
		os.chdir('..')
		with open(arges, 'a') as file:
			file.write('\n{}'.format(str(i)))
		shutil.rmtree(i)
		continue
	try:
		blast_records = NCBIXML.parse(result_handle)
	except Exception:
		continue
	print '\tDone'
	print '\tWriting hits to xml...'
	with open(blastout, 'a') as file:
		for record in blast_records:
			for alignment in record.alignments:
				for hsp in alignment.hsps:
					file.write('\n{}'.format(str(alignment.title)))
					file.write('\t{}'.format(str(hsp.expect)))
					perc = float(hsp.identities) / float(hsp.align_length)
					file.write('\t{}'.format(perc))
					file.write('\t{}'.format(str(hsp.identities)))
					file.write('\t{}'.format(str(hsp.align_length)))
	print '\tDone\n'

#Begin Brontes
	print 'Starting Brontes\n'

#Define unique outfiles
	infile = "%s.txt" % i
	print infile
	outfile = 'RAWOUTPUT.TXT'
	outfile1 = 'ATHALONLY.TXT'
	outfile2 = 'HEATTREECALLS.TXT'
	outfile3 = 'SYNHITS.TXT'
	outdict = {}
	with open(outfile3, 'w') as mkfile:
		mkfile.write('synergid expressed loci:')
	with open(infile) as file:
		for line in file:
			HitID = re.findall('^gi\|\d*\|\w*\|(.{5,20}?)\|', line)
			eval = re.findall('.+[\t]([\S]+)\n', line)
			Ident = re.findall('\|.(\d*[.]{1}[\d]{3})', line)
			if HitID:
				print HitID
				outlist = []
				outlist2 = []
				VAR = str(HitID).replace('[','').replace(']','').replace("'","")
				try:
					handle = Entrez.efetch(db="protein", id=VAR, rettype="gb", retmode="text")	
				except Exception:
					pass
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
				outlist.append(eval)
				outlist.append(Ident)
				for i in outlist:
					atnumber = re.findall('[Aa][Tt]\d[Gg][\d]{5}', str(i))
					if atnumber:
						for i in range(0, wusheet.nrows):
							if wusheet.cell(i,0).value == str(atnumber).replace('[','').replace(']','').replace("'","").upper():
								vals = ('wusy:', wusheet.cell(i,1).value, 'wueg:', wusheet.cell(i,2).value, 'wucc:', wusheet.cell(i,3).value, 'wusp:', wusheet.cell(i,4).value, 'wupo:', wusheet.cell(i,5).value)
								outlist.append(vals)
								if wusheet.cell(i,1).value <= 0.05:
									val2 = (wusheet.cell(i,0).value, Ident, 'wsy:', wusheet.cell(i,1).value, 'weg:', wusheet.cell(i,2).value, 'wcc:', wusheet.cell(i,3).value)
									outlist2.append(val2)
									swvals2 = ('diflog:', '{0:.3f}'.format(swsheet.cell(i,3).value), 'difp:', '{0:.3f}'.format(swsheet.cell(i,4).value), 'myb98log:', '{0:.3f}'.format(swsheet.cell(i,6).value), 'myb98p:', '{0:.3f}'.format(swsheet.cell(i,7).value))
									outlist2.append(swvals2)
						for i in range(0, swsheet.nrows):
							if swsheet.cell(i,0).value == str(atnumber).replace('[','').replace(']','').replace("'","").upper():
								swvals = ('diflog:', '{0:.3f}'.format(swsheet.cell(i,3).value), 'difp:', '{0:.3f}'.format(swsheet.cell(i,4).value), 'myb98log:', '{0:.3f}'.format(swsheet.cell(i,6).value), 'myb98p:', '{0:.3f}'.format(swsheet.cell(i,7).value))
								outlist.append(swvals)											
				key = str(outlist).replace('[','').replace(']','').replace('(','').replace(')','').replace('\'','').replace(', ','_').replace(' ','_')
				print key
				related = str(outlist2).replace('u','').replace('[','').replace(']','').replace('(','').replace(')','').replace('\'','').replace(', ','_').replace(' ','_')
				if related != '':
					with open(outfile3, 'r') as readfile:
						if related not in readfile:
							with open(outfile3, 'a') as file:
								file.write('\n{}'.format(str(related)))
				try:
					l1 = Entrez.efetch(db="protein", id=VAR, rettype="fasta", retmode="text")
				except Exception:
					pass
				for line in l1:
					if '>' in line:
						outdict[key] = ''
					else:
						line = line.replace('\n','')
						outdict[key] = outdict[key] + line
	with open(outfile, 'w') as file:
		for i in outdict.keys():
			file.write('\n>{}\n'.format(i))
			file.write('{}\n'.format(outdict[i]))
	with open(outfile1, 'w') as file:
		for i in outdict.keys():
			if '3702' in i:
				file.write('\n>{}\n'.format(i))
				file.write('{}\n'.format(outdict[i]))
	with open(outfile2, 'a') as file:
		for i in outdict.keys():
			atnumber = re.findall('[Aa][Tt]\d[Gg][\d]{5}', i)
			if atnumber:
				file.write('\n{}'.format(atnumber).replace('[','').replace(']','').replace("'",""))
	os.chdir('..')
