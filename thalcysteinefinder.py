signamedict = {}
namedict = {}
zipdict = {}
fasdict = {}
import re
with open('SPHlista.txt', 'r') as file:
	with open('diflistc.txt', 'a') as outfile:
		with open('SignalPscores.txt', 'r') as sigfile:
			with open('figfile.txt', 'a') as figfile:
				with open('figfas.txt', 'a') as figfas:
					with open('cyssplit.txt','a') as splitfile:
						for line in sigfile:
							signame = re.findall('Name=([\w]*[\d]*)	SP=\'YES\' Cleavage site between pos. [\d]* and [\d]*', line)
							sigpos = re.findall('Name=[\w]*[\d]*	SP=\'YES\' Cleavage site between pos. ([\d]*) and [\d]*', line)
							if signame:
								key = str(signame).replace('[','').replace("'","").replace(']','')
								signamedict[key] = sigpos
							print sigpos
						for line in file:			
							if '>' in line:
								spname = line[1:-1]
								fasdict[spname] = ''
							else:
								fasdict[spname] = fasdict[spname] + line
								alist = []
								clist = []
								lenlist = []
								clist.append(1)
								for a,b in list(enumerate(list(line))):
									if b =='C':
										clist.append(a + 1)
										alist.append('>')
										alist.append(spname)
										alist.append('_')
										alist.append(a + 1)
										alist.append('&')
									else:
										alist.append(b)
								clist.append(len(line))
								namedict[spname] = clist
								splitfile.write(str(alist).replace('[','').replace("'","").replace(']','').replace(',','').replace(' ',''))
						for key,val in namedict.iteritems():
							print key, val
							for spkey,spval in signamedict.iteritems():
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
									print fasdict
									print str(figure).replace('[','').replace("'","").replace(']','').replace(",","").replace(" ",".").replace("..",".")
									outfile.write('{}_{}_{}_{}_{}_{}\n'.format(key,val,str(spval).replace("'",""),keylist,[j-i for i, j in zip(keylist[:-1], keylist[1:])],len(keylist)-1))
									figfile.write('{}_{}\n'.format(key,str(figure).replace('[','').replace("'","").replace(']','').replace(",","").replace(" ",".").replace("..",".")))
