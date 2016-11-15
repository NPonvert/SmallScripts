ssignamedict = {}
nsignamedict = {}
namedict = {}
zipdict = {}
import re
with open('lyratasphs.txt', 'r') as file:
	with open('lyrdiflistc.txt', 'a') as outfile:
		with open('signalp.txt', 'r') as sigfile:
			with open('figfile.txt', 'a') as figfile:
				for line in sigfile:
					signame = re.findall('Name=([\w]{2}\_[\d]*.\d)', line)
					yes = re.findall('Name=[\w]{2}\_[\d]*.\d	SP=\'(YES)\' Cleavage site between pos. [\d]* and [\d]*', line)
					no = re.findall('Name=[\w]{2}\_[\d]*.\d	SP=\'(NO)\'', line)
					sigpos = re.findall('Name=[\w]{2}\_[\d]*.\d	SP=\'YES\' Cleavage site between pos. ([\d]*) and [\d]*', line)
					if signame:
						if yes:
							key = str(signame).replace('[','').replace("'","").replace(']','')
							ssignamedict[key] = sigpos
						if no:
							key = str(signame).replace('[','').replace("'","").replace(']','')
							nsignamedict[key] = 'none'
					
				print ssignamedict
				print nsignamedict
				for line in file:			
					if '>' in line:
						spname = line[1:-1]
					else:
						clist = []
						lenlist = []
						clist.append(1)
						for a,b in list(enumerate(list(line))):
							if b =='C':
								clist.append(a + 1)
						clist.append(len(line))
						namedict[spname] = clist
				for key,val in namedict.iteritems():
					for spkey,spval in ssignamedict.iteritems():
						if key == spkey:
							keylist = []
							keylist.append(1)
							keylist.append(int(str(spval).replace('[','').replace("'","").replace(']','')))
							for i in val:
								if float(i) > float(str(spval).replace('[','').replace("'","").replace(']','')):
									keylist.append(i)
							diflist = [j-i for i, j in zip(keylist[:-1], keylist[1:])]
							print key, '\t', val, '\t', str(spval).replace("'",""), '\t', keylist, '\t', diflist, '\t', len(keylist) - 1
							figure = []
							for a,b in zip(keylist,diflist):
								figure.append(a)
								figure.append('-' * int(b/10))
							figure[2] = 'S',figure[2]
							figure.append(val[-1])
							print figure
							print str(figure).replace('[','').replace("'","").replace(']','').replace(",","").replace(" ",".").replace("..",".")
							outfile.write('{}_{}_{}_{}_{}_{}\n'.format(key,val,str(spval).replace("'",""),keylist,[j-i for i, j in zip(keylist[:-1], keylist[1:])],len(keylist)-1))
							figfile.write('{}_{}\n'.format(key,str(figure).replace('[','').replace("'","").replace(']','').replace(",","").replace(" ",".").replace("..",".")))
					for npkey,npval in nsignamedict.iteritems():
						if key == npkey:
							keylist = []
							for i in val:
								keylist.append(i)
							diflist = [j-i for i, j in zip(keylist[:-1], keylist[1:])]
							figure = []
							for a,b in zip(keylist,diflist):
								figure.append(a)
								figure.append('-' * int(b/10))
							figure.append(val[-1])
							print figure
							print str(figure).replace('[','').replace("'","").replace(']','').replace(",","").replace(" ",".").replace("..",".")
							outfile.write('{}_{}_{}_{}_{}_{}\n'.format(key,val,str(spval).replace("'",""),keylist,[j-i for i, j in zip(keylist[:-1], keylist[1:])],len(keylist)-1))
							figfile.write('{}_{}\n'.format(key,str(figure).replace('[','').replace("'","").replace(']','').replace(",","").replace(" ",".").replace("..",".")))
