#import necessities

import re
import xlrd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#define sheets of expression data
book = xlrd.open_workbook("SPH62.xlsx")
sheet = book.sheet_by_index(0)
strainbook = xlrd.open_workbook("VCF_STRAIN_LIST.xlsx")
strainsheet = strainbook.sheet_by_index(0)

outfile1 = 'ecotypes.txt'
outfile2 = 'snpcalls.txt'
altdict = {}
for j in range(9,sheet.ncols):
	altlist = []
	eco = sheet.cell(18,j).value
	for q in range(0, strainsheet.nrows):
		if eco == strainsheet.cell(q,0).value:
			econame = strainsheet.cell(q,1).value
			for i in range(18, sheet.nrows):
				EFF = sheet.cell(i,7).value
				EFF_type = re.search(u"EFF=(.+?)\(.+?[\|].*\|(.+?\/.+?)\|.\.(.+?)\/",EFF)
				if EFF_type:
					key = [EFF_type.group(1),EFF_type.group(2),EFF_type.group(3),'|']
					key = '_'.join(key)
				geno = str(sheet.cell(i,j).value)
				hom_alt = re.search(u"(1\|1)",geno)
				het = re.search('(0\|1)',geno)
				hom_ref = re.search('(0\|0)',geno)
				nocall = re.search('(\.\/\.)',geno)
				if hom_alt:
					altlist.append(key.replace("'","").replace("u",""))
					altdict[econame] = altlist		
with open(outfile1, 'w') as file:
	for k in sorted(altdict, key=lambda k: len(altdict[k]), reverse=True):
		file.write('{}\t{}\t{}\n'.format(k,len(altdict[k]),str(altdict[k]).replace("'","").replace("u","").replace("[","").replace("]","").replace(",","")))
snpdict = {}
for i in range(18, sheet.nrows):
	countlist = []
	EFF = sheet.cell(i,7).value
	EFF_type = re.search(u"EFF=(.+?)\(.+?[\|].*\|(.+?\/.+?)\|.\.(.+?)\/",EFF)
	if EFF_type:
		key = [EFF_type.group(1),EFF_type.group(2),EFF_type.group(3)]
		key = '_'.join(key)
		for j in range(9,sheet.ncols):
			eco = sheet.cell(18,j).value
			for x in range(0, strainsheet.nrows):
				if eco == strainsheet.cell(x,0).value:
					econame = strainsheet.cell(x,1).value
			geno = str(sheet.cell(i,j).value)
			hom_alt = re.search(u"(1\|1)",geno)
			if hom_alt:
				name = [econame, '|']
				name = ''.join(name)
				countlist.append(name)
		snpdict[key] = countlist
with open(outfile2, 'w') as file:
	for u in sorted(snpdict, key=lambda u: len(snpdict[u]), reverse=True):
		file.write('{}\t{}\t{}\n'.format(u,len(snpdict[u]),str(snpdict[u]).replace("'","").replace("u","").replace("[","").replace("]","").replace(",","")))

		