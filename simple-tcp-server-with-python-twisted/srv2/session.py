

## ---------------------------
## Classe de session
## Autrement dit le scenario
## ---------------------------

import os, sys, traceback
import datetime
import pudb

NB = 1
RUNNING = NB
NB+=1
WAITING = NB
NB+=1
PRINTING = NB
NB+=1
ERR_VERIF = NB
NB+=1
FINISHED = NB
NB+=1
STOPPED = NB

## -------------------------
## Exception / erreur
## -------------------------
class Err(Exception):
	"""
	La base de mes erreurs
	"""
	def __init__(self, raison="<vide>"):
		Exception.__init__(self, raison)
		self.raison = raison

	def __str__(self):
		return "Err : %s " % self.raison

class Printing(Exception):
	"""
	il y a des donnees a sortir
	"""
	def __init__(self, raison="<vide>"):
		Exception.__init__(self, raison)
		self.raison = raison

	def __str__(self):
		return "Printing : %s " % self.raison

class Waiting(Exception):
	"""
	Attente de donnees en entree
	"""
	def __init__(self, raison="<vide>"):
		Exception.__init__(self, raison)
		self.raison = raison

	def __str__(self):
		return "Waiting : %s " % self.raison

class Err_Verif(Exception):
	"""
	Erreur sur verification des donnees
	"""
	def __init__(self, raison="<vide>", etape=0):
		Exception.__init__(self, raison)
		self.raison = raison
		self.etape = etape

	def __str__(self):
		return "Err_Verif : %s " % self.raison

class Stopped(Exception):
	"""
	Session Stop
	"""
	def __init__(self, raison="<vide>"):
		Exception.__init__(self, raison)
		self.raison = raison

	def __str__(self):
		return "Stopped : %s " % self.raison

class Finished(Exception):
	"""
	Session termine
	"""
	def __init__(self, raison="<vide>"):
		Exception.__init__(self, raison)
		self.raison = raison

	def __str__(self):
		return "Finished : %s " % self.raison

## --------------------------
## la classe de base session
## --------------------------
class Session(object):

	def __init__(self, name):
		self.name = name
		self.ETAT = ""			# Etat de la session
		self.ERREUR = 0			# Erreur 
		self.ERR_DESC = ""		# Description de l'erreur
		self.std_in = None		# Entree standard
		self.std_out = None		# Sortie Standard
		self.user_input = None

		self.etape = 0

	def __str__(self):
		return "%s : Etat = %s / Err = %s / ErrDesc = %s " % (self.name, self.str_ETAT(), self.ERREUR, self.ERR_DESC)

	def str_ETAT(self):
		l = [ "RUNNING", "WAITING", "PRINTING", "ERR_VERIF", "FINISHED", "STOPPED" ]
		try:
			return l[self.ETAT-1]
		except:
			return "ETAT INCONNUE %s" % self.ETAT

	def raz(self):
		"""
			Remise a zero
		"""
		self.ETAT = ""
		self.ERREUR = 0
		self.ERR_DESC = ""
		self.user_input = None
		self.std_in = None
		self.std_out = None
		self.etape = 0


	def scenario(self):
		raise Finished

	def tick(self):
		"""
			Boucle d'execution
		"""
		EXIT = False
		while not EXIT:
			self.ETAT = RUNNING
			try:
				if self.user_input:
					self.std_in = self.user_input
					self.user_input = None
				## On continue
				self.scenario()
			except Printing:
				self.ETAT = PRINTING
				EXIT = True
			except Waiting:
				self.ETAT = WAITING
				EXIT = True
			except Err_Verif as e:
				self.ETAT = ERR_VERIF
				self.ERREUR = e.etape
				self.ERR_DESC = e.raison
				EXIT = True
			except Finished:
				self.ETAT = FINISHED
				EXIT = True
			except:
				self.ETAT = STOPPED
				print "Erreur :"
				print "-"*60
				traceback.print_exc(file=sys.stdout)
				print "-"*60
				EXIT = True
			else:
				pass

		#print "%s : Etape=%s ETAT=%s" % (self.name, self.etape, self.str_ETAT())

	## --------------------------------
	## Interface commune de sessions
	## tick() en fait partie
	## --------------------------------
	def get_ETAT(self):
		return self.ETAT

	def set_INPUT(self, data):
		self.user_input = data

	def get_OUTPUT(self):
		return self.std_out

	def clear_OUTPUT(self):
		self.std_out = None

	def get_ERROR(self):
		if self.ERREUR:
			return "%s : %s" % (self.ERREUR, self.ERR_DESC)
		else:
			return None

## --------------------------
## Exemple de classe de base
## --------------------------
class MP(Session):

	def __init__(self, name):
		 super(MP, self).__init__(name)

	def scenario(self):
		print "ENTREE", self.etape
		INIT = 0
		DOSSIER = 10
		DOSS_VERIF = 15
		OPERATION = 20
		OP_VERIF = 25
		VERIF_AVANT_MAJ = 80
		MAJ_BASE = 90
		if self.etape == INIT:
			self.raz()
			self.etape = DOSSIER
		elif self.etape == DOSSIER:
			## Afichage
			self.std_out = "Dossier : "
			self.etape += 1
			raise Printing
		elif self.etape == DOSSIER+1:
			## Attente de saisie
			self.etape = DOSS_VERIF
			raise Waiting
		elif self.etape == DOSS_VERIF:
			## Verif du dossiers
			DOSSIERS = ['1000', '1001', '1002', '1003']
			print "verif Dossiers [%s] - %s" % ( self.std_in, DOSSIERS)
			if self.std_in in DOSSIERS:
				self.etape = OPERATION
			else:
				R = "DOSSIER INCONNU %s " % self.std_in
				E = self.etape
				self.etape = DOSSIER
				raise Err_Verif(raison=R, etape=E)
		elif self.etape == OPERATION:
			## Affichage
			self.etape += 1
			self.std_out = "Operation :"
			raise Printing
		elif self.etape == OPERATION+1:
			## Attente de saisie
			self.etape = OP_VERIF
			raise Waiting
		elif self.etape == OP_VERIF:
			DATA = self.std_in
			USERS = [ 'ONE', 'TWO' ]
			ACTION = [ 'D', 'F', 'S' 'R' ]
			POSTE = [ 'P01', 'P02', 'P03' ]
			try:
				U = DATA[:3]
				A = DATA[3]
				P = DATA[4:]
			except:
				R = "ERREUR FORMAT %s " % DATA
				E = self.etape
				self.etape = OPERATION
				raise Err_Verif(raison=R, etape=E)
			## Test USERS
			if not U in USERS:
				R = "USER INCONNU %s " % DATA
				E = self.etape
				self.etape = OPERATION
				raise Err_Verif(raison=R, etape=E)
			## Test ACTION
			if not A in ACTION:
				R = "ACTION INCONNUE %s " % DATA
				E = self.etape
				self.etape = OPERATION
				raise Err_Verif(raison=R, etape=E)
			## Test POSTE
			if not P in POSTE:
				R = "POSTE INCONNUE %s " % DATA
				E = self.etape
				self.etape = OPERATION
				raise Err_Verif(raison=R, etape=E)
			## sinon 
			self.etape = VERIF_AVANT_MAJ
		elif self.etape == VERIF_AVANT_MAJ:
			self.etape = MAJ_BASE
		elif self.etape == MAJ_BASE:
			## Ecriture base de donnees
			self.std_out = "MISE A JOUR BASE OK"
			self.etape = INIT
			raise Printing
		elif self.etape == 99:
			raise Finished
		print "SORTIE", self.etape

## ------------------------
## Petite routine de log
## ------------------------
def log(msg=''):
	now = datetime.datetime.now().time()
	print '%s : %s' % (now, msg)

def test():
	log("=== Debut ===")
	s = MP('test')
	print s
	EXIT = False
	log("debut Boucle principale")
	#pudb.set_trace()
	while not EXIT:
		s.tick()
		if s.get_ETAT() == WAITING:
			print "WAITING"
			r = raw_input('in= >')
			s.set_INPUT(r)
		elif s.get_ETAT() == PRINTING:
			print "out=[%s]" % s.get_OUTPUT()
			s.clear_OUTPUT()
		elif s.get_ETAT() == ERR_VERIF:
			print "ERREUR => Etape : %s / %s " % (s.ERREUR, s.ERR_DESC)
		elif s.get_ETAT() == FINISHED:
			print "FINISHED => ", s
			EXIT = True
		elif s.get_ETAT() == STOPPED:
			## Une erreur 
			print "STOPPED => ", s.get_ERROR()
		else:
			print "Erreur ETAT inconnue"
			EXIT = True
	log('Fin Boucle')
	log("=== FIN ===")

if __name__ == '__main__':
	test()
