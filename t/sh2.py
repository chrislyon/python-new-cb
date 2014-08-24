

import shlex

f = open('src/PRINT.txt')
f = open('src/LET.txt')

line = '-' * 30

n=0
for l in f.readlines():
	n += 1
	l = l.strip()
	print "%02d : %s" % (n, l)
	print line
	s1 = shlex.shlex(l)
	print "OPERANDE:%s" % s1.read_token()
	for s2 in s1:
		s = shlex.shlex(s2)
		for t in s:
			print "Argument : %s " % t
	print line
