# Import necessities

import xlrd
from collections import defaultdict

#Define Colors

class color:
   RED = '\033[91m'
   GREEN = '\033[92m'
   END = '\033[0m'

#make dictionaries of colored letters

gdict = {"A":color.GREEN + "A" + color.END,"C":color.GREEN + "C" + color.END,"G":color.GREEN + "G" + color.END,"T":color.GREEN + "T" + color.END}
bdict = {"A":color.RED + "A" + color.END,"C":color.RED + "C" + color.END,"G":color.RED + "G" + color.END,"T":color.RED + "T" + color.END}

#make the list to which guides will be appended

guidelist = []
guidedict = defaultdict(int)

#Get CRISPR guide excel doc from user

excel = raw_input('\nPlease enter the location of your CRISPR guide excel doc: ')
print '\nThank you\n'

#Open the above excel file

book = xlrd.open_workbook(excel)
sheet = book.sheet_by_index(0)

#Define number of supplied guides

for i in range(1, sheet.nrows):
	guidelist.append(sheet.cell(i,2).value)

#Enumerate and read through guide, compile a list of scores for each guide, and rewrite guide with colored letters

print 'Guide\t\t\tScore'

for i in guidelist:
	i = i.upper()
	scorelist = []
	relist = []
	for j,x in enumerate(list(i)):
		if j == 0:
			if x == 'G':
				scorelist.append(3)
				relist.append(gdict[x])
			else:
				scorelist.append(-6)
				relist.append(bdict[x])
		if j == 1:
			relist.append(x)
		if j == 2:
			if x == 'C':
				scorelist.append(-2)
				relist.append(bdict[x])
			else:
				relist.append(str(x))
		if j == 3:
			if x == 'G':
				scorelist.append(1)
				relist.append(gdict[x])
			else:
				relist.append(x)
		if j == 4:
			if x == 'G':
				scorelist.append(1)
				relist.append(gdict[x])
				continue
			if x == 'A':
				scorelist.append(1)
				relist.append(gdict[x])
				continue
			else:
				relist.append(x)
		if j == 5:
			if x == 'G':
				scorelist.append(1)
				relist.append(gdict[x])
			else:
				relist.append(x)
		if j == 6:
			if x == 'G':
				scorelist.append(1)
				relist.append(gdict[x])
				continue
			if x == 'T':
				scorelist.append(-2)
				relist.append(bdict[x])
				continue
			else:
				relist.append(x)
		if j == 7:
			relist.append(str(x))
		if j == 8:
			if x == 'A':
				scorelist.append(1)
				relist.append(gdict[x])
			else:
				relist.append(x)
		if j == 9:
			if x == 'A':
				scorelist.append(1)
				relist.append(gdict[x])
			else:
				relist.append(x)
		if j == 10:
			if x == 'A':
				scorelist.append(1)
				relist.append(gdict[x])
				continue
			if x == 'T':
				scorelist.append(-2)
				relist.append(bdict[x])
				continue
			else:
				relist.append(x)
		if j == 11:
			if x == 'A':
				scorelist.append(1)
				relist.append(gdict[x])
			else:
				relist.append(x)
		if j == 12:
			relist.append(x)
		if j == 13:
			if x == 'T':
				scorelist.append(1)
				relist.append(gdict[x])
				continue
			if x == 'G':
				scorelist.append(-2)
				relist.append(bdict[x])
				continue
			else:
				relist.append(x)
		if j == 14:
			if x == 'A':
				scorelist.append(1)
				relist.append(gdict[x])
			else:
				relist.append(x)
		if j == 15:
			if x == 'A':
				scorelist.append(1)
				relist.append(gdict[x])
			else:
				relist.append(x)
		if j == 16:
			if x == 'G':
				scorelist.append(1)
				relist.append(gdict[x])
				continue
			if x == 'T':
				scorelist.append(-2)
				relist.append(bdict[x])
				continue
			else:
				relist.append(x)
		if j == 17:
			if x == 'C':
				scorelist.append(1)
				relist.append(gdict[x])
				continue
			if x == 'T':
				scorelist.append(-2)
				relist.append(bdict[x])
				continue
			else:
				relist.append(x)
		if j == 18:
			if x == 'G':
				scorelist.append(1)
				relist.append(gdict[x])
				continue
			if x == 'T':
				scorelist.append(-2)
				relist.append(bdict[x])
				continue
			else:
				relist.append(x)
		if j == 19:
			if x == 'G':
				scorelist.append(1)
				relist.append(gdict[x])
				continue
			if x == 'T':
				scorelist.append(-2)
				relist.append(bdict[x])
				continue
			if x == 'C':
				scorelist.append(-2)
				relist.append(bdict[x])
				continue			
			else:
				relist.append(x)
	guidedict[''.join(relist)] = sum(scorelist)
for i in sorted(guidedict, key=guidedict.get, reverse=True):
	print i, '\t', guidedict[i]

		