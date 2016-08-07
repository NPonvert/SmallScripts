Coding = raw_input('Please enter a DNA sequence: ')
Coding = Coding.upper().replace(' ','')
class color:
   RED = '\033[91m'
   GREEN = '\033[92m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
print '\nYour sequence is:', '"{}"'.format(Coding), '\n'
codon_dict = {"TTT":"F", "TTC":"F", "TTA":"L", "TTG":"L",
       "UCU":"S", "UCC":"S", "UCA":"S", "UCG":"S",
       "TAT":"Y", "TAC":"Y", 
       "TAA":color.RED + color.BOLD + "stop" + color.END, 
       "TAG":color.RED + color.BOLD + "stop" + color.END,
       "TGT":"C", "TGC":"C", 
       "TGA":color.RED + color.BOLD + "stop" + color.END, 
       "TGG":"W",
       "CTT":"L", "CTC":"L", "CTA":"L", "CTG":"L",
       "CCT":"P", "CCC":"P", "CCA":"P", "CCG":"P",
       "CAT":"H", "CAC":"H", "CAA":"Q", "CAG":"Q",
       "CGT":"R", "CGC":"R", "CGA":"R", "CGG":"R",
       "ATT":"I", "ATC":"I", "ATA":"I", "ATG":"M",
       "ACT":"T", "ACC":"T", "ACA":"T", "ACG":"T",
       "AAT":"N", "AAC":"N", "AAA":"K", "AAG":"K",
       "AGT":"S", "AGC":"S", "AGA":"R", "AGG":"R",
       "GTT":"V", "GTC":"V", "GTA":"V", "GTG":"V",
       "GCT":"A", "GCC":"A", "GCA":"A", "GCG":"A",
       "GAT":"D", "GAC":"D", "GAA":"E", "GAG":"E",
       "GGT":"G", "GGC":"G", "GGA":"G", "GGG":"G",}
Complementdict = { 'A':'T', 'C':'G', 'G':'C', 'T':'A', }
Complement = []
for elem in reversed(Coding):
	Complement.append(Complementdict[elem])
Complement = ''.join(Complement)
print "The reverse complement of your sequence is:", '"{}"'.format(Complement), "\n"
Translation, Codons, Codonp, Num, Per = ({} for i in range(5))
Letters = ['A','C','G','T','N']
Numbers = [0,1,2]
for letter in Letters:
	Num[letter] = Coding.count(letter)
	Per[letter] = "%.1f" % (100 * Coding.count(letter) / len(Coding))
print 'Your sequence is', len(Coding), 'nucleotides long.'
for i in Letters:
	print 'Your sequence contains\t\t', Num[i], '\t({}%)\t'.format(Per[i]), i, "'s."
for n,x in [('coding', Coding), ('complement',Complement)]:
	for key in Numbers:
		Codons[key] = []
		for i in range(key, len(x), 3):
			Codonp[key] = x[i:i+3]
			Codons[key].append(Codonp[key])
	for a,b in Codons.iteritems():
		Translation[a] = []
		if ('ATG' in b):
			print '\nYour sequence contains a start codon at position', ((b.index('ATG') * 3) + 1), 'on the', n, 'strand in frame', a, '\n'
			for i in b[b.index('ATG'):]:
				if (i not in codon_dict):
					continue
				else:
					Translation[a].append(codon_dict[i])
					continue
			print 'The translation of your sequence from the above start codon is as follows:\n', ''.join(Translation[a]), '\n'
		else:
			print 'There are no start codons on the', n,' strand of your sequence in frame', a, '.\n'	
