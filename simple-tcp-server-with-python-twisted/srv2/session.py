

##
## QQ chose ne focntionne pas
##

import os, sys, traceback
import datetime
import pudb

RUNNING = 1
WAITING = 2
PRINTING = 3
FINISHED = 4
STOPPED = 5

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
		l = [ "RUNNING", "WAITING", "PRINTING", "FINISHED", "STOPPED" ]
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
		if self.etape == 0:
			self.raz()
			self.etape = 1
		elif self.etape == 1:
			self.std_out = "Dossier : "
			self.etape = 2
			raise Printing
		elif self.etape == 2:
			self.etape = 3
			raise Waiting
		elif self.etape == 3:
			if self.std_in == 'QUIT':
				self.etape = 5
			else:
				self.std_out = "TEST DOSSIER %s " % self.std_in
				self.etape = 0
				raise Printing
		elif self.etape == 4:
			self.etape = 0
		elif self.etape == 5:
			raise Finished

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
	while not EXIT:
		s.tick()
		if s.get_ETAT() == WAITING:
			print "WAITING"
			r = raw_input('in= >')
			s.set_INPUT(r)
		elif s.get_ETAT() == PRINTING:
			print "out=[%s]" % s.get_OUTPUT()
			s.clear_OUTPUT()
		elif s.get_ETAT() == FINISHED:
			print "FINISHED => ", s
			EXIT = True
		elif s.get_ETAT() == STOPPED:
			print "STOPPED => ", s.get_ERROR()
			EXIT = True
		else:
			print "Erreur ETAT inconnue"
			EXIT = True
	log('Fin Boucle')
	log("=== FIN ===")

if __name__ == '__main__':
	test()
