##
##
##

import pdb

class Program_Ligne():
	def __init__(self):
		self.etiq = ""
		self.No = 0
		self.prompt = ''
		self.test = ''
		self.action = ''
		self.done = False
		self.status = 0
		self.stop = False

	def __str__(self):
		fmt =  "Etiq=%-10s No=%02d prompt=%10s test=%10s action=%10s done=%5s"
		d = (self.etiq,self.No,self.prompt,self.test,self.action,self.done)
		return fmt % d

class Session():
	def __init__(self, name):
		self.name = name
		## Parametre de la session
		self.sai_bobine = False
		## Data ##
		self.dossier = 0
		self.oper = ''
		self.bobine = ''
		self.numbo = []
		## Scenario
		self.scenario = []

		## Param
		self.param = None
		self.prompt = ''

	def init_scenario(self):
		for x in self.scenario:
			x.done = False

	def load_scenario(self, prg):
		self.scenario = prg

	def liste_scenario(self):
		for l in self.scenario:
			print l

	def __str__(self):
		return 'Session : %s ' % self.name

	def raz(self):
		print "RAZ"
		return True

	def verif_dossier(self):
		print "Verif dossier"
		if self.param:
			## Verif du dossier en fonction du parametre
			## sinon c'est pas bon
			print "MAJ DOSSIER"
			self.dossier = self.param
		if self.dossier == 0:
			return False
		else:
			return True

	def verif_oper(self):
		print "Verif oper"
		if self.oper == 0:
			return False
		else:
			return True

	def verif_bobine(self):
		print "Verif bobine"
		return True
	
	def mise_a_jour(self):
		print "Mise a jour"
		self.init_scenario()
		return True

	def sai_bob(self):
		print "Saisie Bobine"
		return self.sai_bobine

	def do_it(self, data=None):
		for x in self.scenario:
			print "=>%s" % x
			self.param = data
			if not x.done:
				if x.test:
					st = eval(x.test)
				else:
					st = True
				if st:
					if x.prompt:
						self.prompt = x.prompt
					if x.action:
						x.done = eval(x.action)
						if x.done:
							continue
					else:
						x.done = True
					if x.stop:
						break

def get_cmd():
	r = raw_input('>')
	return r.upper()

def test():
	A = Session('TEST')

	s = []
	## Ligne 1
	l = Program_Ligne()
	l.etiq = "DEBUT"
	l.No = 0
	s.append(l)
	## Ligne 2
	l = Program_Ligne()
	l.etiq = "INIT"
	l.No = 1
	l.action = 'self.raz()'
	s.append(l)
	## Ligne 3
	l = Program_Ligne()
	l.etiq = "DOSSIER"
	l.No = 2
	l.prompt = 'Dossier : '
	l.action = 'self.verif_dossier()'
	l.stop = True
	s.append(l)
	## Ligne 4
	l = Program_Ligne()
	l.etiq = "OPERATION"
	l.No = 3
	l.prompt = 'Operation : '
	l.action = 'self.verif_oper()'
	l.stop = True
	s.append(l)
	## Ligne 5
	l = Program_Ligne()
	l.etiq = "BOBINE"
	l.No = 4
	l.prompt = 'Bobine : '
	l.test = 'self.sai_bob()'
	l.stop = True
	l.action = 'self.verif_bobine()'
	s.append(l)
	## Ligne 6
	l = Program_Ligne()
	l.etiq = "MAJ_BASE"
	l.No = 5
	l.action = 'self.mise_a_jour()'
	s.append(l)


	A.load_scenario(s)
	#A.liste_scenario()

	# Boucle principale
	EXIT = False
	pdb.set_trace()
	A.do_it()
	while not EXIT:
		print A.prompt
		cmd = get_cmd()
		if cmd == 'EXIT':
			EXIT = True
		print 'Resultat : ', A.do_it(cmd)

if __name__ == '__main__':
	test()
