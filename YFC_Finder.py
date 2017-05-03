import re
import statistics
dict = {}
with open('YFWxC_THIONIN.txt') as file:
	for line in file:
		line = line.upper()
		if line.startswith('>'):
			key = line[1:]
			print line
			dict[key] = ''
		else:
			dict[key] = dict[key]+line
avg = []
pavg = []
num = []
distlist = []
signamedict = {}
with open('THIONIN_SignalPscores.txt') as sigfile:
	for line in sigfile:
		signame = re.findall('Name=([\w]*[\d]*)	SP=\'YES\' Cleavage site between pos. [\d]* and [\d]*', line)
		sigpos = re.findall('Name=[\w]*[\d]*	SP=\'YES\' Cleavage site between pos. ([\d]*) and [\d]*', line)
		if signame:
			sigkey = str(signame).replace("[","").replace("]","").replace("'","")
			sigkey = sigkey.upper()
			sigpos = str(sigpos).replace("[","").replace("]","").replace("'","")
			signamedict[sigkey] = sigpos
print signamedict
for key,val in dict.iteritems():
	count = []
	postcount = []
	yfwlist = []
	pyfwlist = []
	print '\n', key.replace(">","")
	print val
	for a,b in signamedict.iteritems():
		if key.replace(">","").replace("\n","") == a:
			print 'match', a, 'SS:', b
	for j,x in enumerate(list(val)):
		if x == 'C':
			print list(val)[j-2], list(val)[j-1], x, list(val)[j+1], list(val)[j+2], j+1
			if int(j+1) > int(b):
				count.append(1)
				if j > 2:
					if list(val)[j-2] == 'F' or list(val)[j-2] == 'Y' or list(val)[j-2] == 'W':
						dist = int(j)-int(b)
						print 'DIST:', dist
						yfwlist.append(1)
						distlist.append(dist)
					if list(val)[j+2] == 'F' or list(val)[j+2] == 'Y' or list(val)[j+2] == 'W':
						pyfwlist.append(1)
	num.append(sum(count))
	if sum(count) >0:
		avg.append(float(sum(yfwlist))/float(sum(count)))
		pavg.append(float(sum(pyfwlist))/float(sum(count)))
	else:
		continue
	print '\nPRE:', float(sum(yfwlist))/float(sum(count))
	print '\nPOST:', float(sum(pyfwlist))/float(sum(count))
print '\nAVG_PRE:', float(sum(avg))/float(len(avg))
print 'StdDev_PRE:', statistics.stdev(avg)
print avg
print '\nAVG_POST:', float(sum(pavg))/float(len(pavg))
print 'StdDev_POST:', statistics.stdev(pavg)
print pavg
print '\nAVG_DIST:', sum(distlist)/len(distlist)
print '\nNUM_CYS:', sum(num), '\n'
				
