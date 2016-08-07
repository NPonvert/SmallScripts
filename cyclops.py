import re
from Bio import Entrez
Entrez.email = "nathaniel_ponvert@brown.edu" 
infile = raw_input('infilename: ')
outfile = raw_input('outfilename: ')
outfile1 = raw_input('file for Athaliana only results: ')
outfile2 = raw_input('file for heat tree calls: ')
outdict = {}
with open(infile) as file:
	for line in file:
		if '#' not in line:
			HitID = re.findall('^.{10,30}\tgi\|\d*\|\w*\|(.{5,20}?)\|',line)
			Ident = re.findall('.*\t(\d*[.]{1}[\d]{3})', line)
			if HitID:
				outlist = []
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
				outlist.append(Ident)
				key = str(outlist).replace('[','').replace(']','').replace('(','').replace(')','').replace('\'','').replace(', ','_').replace(' ','_')
				print key
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
