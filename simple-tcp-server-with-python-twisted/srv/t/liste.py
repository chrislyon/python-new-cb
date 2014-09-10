
import pdb

class Vide():
    pass

l = []


o1 = {1:'a'}

o2 = [ 1,2,3 ]

o3 = Vide()
o3.toto = 1
o3.titi = 'abc'

l.append(o1)
l.append(o2)
l.append(o3)


pdb.set_trace()
