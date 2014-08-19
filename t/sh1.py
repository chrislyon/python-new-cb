

import shlex

f = open('TEST1.txt')

line = '-' * 30

n=0
for l in f.readlines():
	n += 1
	l = l.strip()
	print "%02d : %s" % (n, l)
	print line
	s = shlex.split(l)
	for t in s:
		print t
	print line
