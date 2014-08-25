#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
## ---------------------------
## MACHINEVIRTUELLE en PYTHON
## ---------------------------
"""

import os, sys, traceback
import datetime
import shlex
import pdb


## -------------------------
## Exception / erreur
## -------------------------
class Err(Exception):
	"""
	La base de mes erreurs
	"""
	def __init__(self, raison="<vide>", nolig=0):
		Exception.__init__(self, raison)
		self.raison = raison
		self.nolig = nolig

	def __str__(self):
		return "%s : %s " % (self.nolig, self.raison)

class Printing(Exception):
	"""
		La machine veut afficher qq chose
	"""
	def __init__(self, raison="<vide>", nolig=0):
		Exception.__init__(self, raison)
		self.raison = raison
		self.nolig = nolig

	def __str__(self):
		return "%s : %s " % (self.nolig, self.raison)

class Waiting(Exception):
	"""
		La machine attend une donnée
	"""
	def __init__(self, raison="<vide>", nolig=0):
		Exception.__init__(self, raison)
		self.raison = raison
		self.nolig = nolig

	def __str__(self):
		return "%s : %s " % (self.nolig, self.raison)

class EndOfProg(Exception):
	"""
		On est arrivé au bout
	"""
	def __init__(self, raison="<vide>", nolig=0):
		Exception.__init__(self, raison)
		self.raison = raison
		self.nolig = nolig

	def __str__(self):
		return "%s : %s " % (self.nolig, self.raison)


## ------------------------
## Une operation / tick 
## ------------------------
class Operande(object):
	"""
		Une operation
	"""
	def __init__(self):
		self.name = ''
		self.nolign = 0
		self.param1 = ''
		self.param2 = ''
		self.param3 = ''
		self.param4 = ''
		self.param5 = ''
		self.params = None
		self.status = False

	def __str__(self):
		return '%03d : OP:%-10.10s : %-5.5s : %s %s %s %s %s' % \
			(self.nolign, self.name, self.status, \
			self.param1, self.param2, self.param3, self.param4, self.param5 )
ETAT = 1
STOPPED = ETAT
ETAT += 1
CHECKING = ETAT
ETAT += 1
RUNNING = ETAT
ETAT += 1
WAITING = ETAT
ETAT += 1
PRINTING = ETAT
ETAT += 1
FINISHED = ETAT

class Machine(object):
	"""
	LA MACHINE VIRTUELLE SUPER BASIC
	"""
	def __init__(self, name):
		self.name = name
		self.registres = {}
		self.status = False
		self.etat = STOPPED
		self.variables = {}
		self.constantes = {}
		self.erreur = 0
		self.errlig = 0

		self.data_out = None
		self.data_in = None

		self.cursor = 0
		self.prog = []

		self.etiq = {}

		self.OPERANDE = [
			'$', 'ETIQ', 'LET',
			'CALL',
			'JMP_FALSE', 'JMP_TRUE', 'GOTO',
			'CONSTANTE', 'VAR', 'VARIABLE', 'REGISTRE',
			'PRINT', 'RAZ',
			'READ',
			'STATUS', 'TEST', 'INIT', 'END'
		]

	def __str__(self):
		ret = 'MACH:%s ' % self.name
		ret += 'status=%s ' % self.status
		ret += 'erreur=%s ' % self.erreur
		ret += 'errlig=%s' % self.errlig
		ret += '\n'
		ret += 'Registres    : \n'
		for i in sorted(self.registres.items()):
			ret += '%s = %s\n' % i
		ret += '\n'
		ret += 'Variable(s)  : \n'
		for k, v in self.variables.items():
			ret += 'VAR %s = %s\n' % (k, v)
		ret += '\n'
		ret += 'Constante(s) : \n'
		for k, v in self.constantes.items():
			ret += 'CONST %s = %s\n' % (k, v)
		ret += '\n'
		ret += 'Etiquette(s) : \n'
		for k, v in self.etiq.items():
			ret += 'ETIQ %s = %s\n' % (k, v)
		ret += '\n'
		return ret

	def raz_registres(self):
		""" Remise a zero des regitres """
		for i in range(0, 10):
			self.registres['R%d' % i] = ''

	def raz_status(self):
		""" Remise a zero des status """
		self.status = False
		self.erreur = 0
		self.errlig = 0

	def mach_init(self):
		""" init de la vm """
		self.raz_registres()
		self.variables = {}
		self.status = False
		self.erreur = 0
		self.errlig = 0
		self.cursor = 0
		self.check_prog()

	## -------------------------------
	## VERIFICATION AVANT EXECUTION
	## -------------------------------
	def check_prog(self):
		""" Verif Prog """
		self.etat = CHECKING
		## Numerotation + recup des etiquettes
		num_lig = 0
		for op in self.prog:
			num_lig += 1
			op.nolign = num_lig
			if op.name in ('$', 'ETIQ'):
				self.etiq[op.param1] = op.nolign
		## Verif si END a la fin
		#if self.prog[-1].op.name != 'END':
		#	p = Operande()
		#	p.name = 'END'
		#	self.prog.append(p)


		## Verification syntaxe
		for op in self.prog:
			#if op.name == 'GOTO':
			#	pdb.set_trace()
			self.check_line(op)

	def check_line(self, op):
		""" Verif d'une ligne """
		op.status = False
		if op.name not in self.OPERANDE:
			raise Err("Instruction inexistante", op.nolign)
		else:
			if op.name in ('$', 'ETIQ'):
				if not op.param1:
					raise Err("Parametre obligatoire", op.nolign)
			elif op.name == 'LET':
				pass
			elif op.name == 'CALL':
				if not op.param1:
					raise Err("Function obligatoire", op.nolign)
			elif op.name in ('GOTO', 'JMP_FALSE', 'JMP_TRUE'):
				if not op.param1:
					raise Err("Parametre obligatoire", op.nolign)
				if op.param1 not in self.etiq.keys():
					raise Err("Etiquette inexistante", op.nolign)
			elif op.name == 'PRINT':
				if not op.param1:
					raise Err("Parametre obligatoire", op.nolign)
			elif op.name == 'RAZ':
				if not op.param1:
					raise Err("Parametre obligatoire", op.nolign)
		##
		op.status = True

	def liste_prog(self):
		""" Listing du programme """
		for l in self.prog:
			print l

	## -------------------------------
	## Gestion du cursor d'execution
	## -------------------------------
	def inc_cursor(self):
		""" incremente le cursor d'execution """
		n = self.cursor
		n += 1
		self.set_cursor(n)

	def dec_cursor(self):
		""" decremente le cursor d'execution """
		n = self.cursor
		n -= 1
		self.set_cursor(n)

	def set_cursor(self, n):
		""" affecte le cursor d'execution """
		self.cursor = n
		if n > 0 and n < len(self.prog):
			self.cursor = n
		else:
			self.etat = STOPPED
			raise EndOfProg("Set Cursor", 0)

	## ------------
	## Affectation
	## ------------
	def affectation(self, op):
		#pdb.set_trace()
		""" Affectation """
		if op.param1 == '%':
			RLeft = op.param2
		else:
			raise Err("Affectation incorrecte", op.nolign)
		## op.param3 = '='
		if op.param4 == '%':
			## Affectation de registe
			Valeur = self.registres[op.param5]
		else:
			## Valeur en dur
			Valeur = op.param4
		self.registres[RLeft] = Valeur

	##-------------------------
	## Le processeur
	##-------------------------
	def execute(self):
		"""
			Execution d'un operation 
		"""
		if self.prog:
			op = self.prog[self.cursor-1]
			print "Executing : %s " % op

			if op.name == 'INIT':
				pass
			elif op.name == 'END':
				pass
			elif op.name == 'LET':
				self.affectation( op )
			elif op.name in ('$', 'ETIQ'):
				pass
			elif op.name == 'READ':
				if self.data_in:
					self.registres[op.param1] = self.data_in
					self.data_in = None
				else:
					self.etat = WAITING
					raise Waiting("READ", op.nolign)
			elif op.name == 'RAZ':
				if op.param1 == 'VAR':
					pass
				elif op.param1 == 'STATUS':
					self.raz_status()
				elif op.param1 == 'REGISTRE':
					self.raz_registres()
				else:
					self.etat = STOPPED
					op.status = False
					raise ("Parametre incorrect", op.nolign)
			elif op.name == 'PRINT':
				self.etat = PRINTING
				if op.param1 == '%':
					self.data_out = self.registres[op.param2]
				else:
					self.data_out = op.param1
				raise Printing("PRINT", op.nolign)
			elif op.name == 'CALL':
				if op.param1:
					## On change le cursor
					pass
				else:
					raise Err(raison="Parametre inexistant", nolig=op.nolign)
			elif op.name == 'GOTO':
				c = self.etiq[op.param1]
				self.set_cursor(c)
			elif op.name == 'JMP_FALSE':
				pass
			elif op.name == 'TEST':
				pass
			else:
				raise Err(raison="Operation inconnue", nolig=op.nolign)
		else:
			raise EndOfProg('Execute', 0)

	## -----------------------------
	## Execution d'une instruction
	## -----------------------------
	def tick(self, data=None):
		"""
			Boucle d'execution
		"""
		EXIT = False
		user_input = data
		while not EXIT:
			try:
				if not user_input:
					self.inc_cursor()
				else:
					self.data_in = user_input
					user_input = None
				## On continue
				self.etat = RUNNING
				self.execute()
			except Printing:
				self.etat = PRINTING
				EXIT = True
			except Waiting:
				self.etat = WAITING
				EXIT = True
			except EndOfProg:
				self.ETAT = STOPPED
				EXIT = True
			except:
				print "Erreur :"
				print "-"*60
				traceback.print_exc(file=sys.stdout)
				print "-"*60
				EXIT = True

## ------------------------
## Chargement d'un prog
## a partir d'un fichier
## ------------------------
def set_prog_fic(ficname, p):
	with open(ficname) as f:
		ll = f.readlines()
		for l in ll:
			if l.startswith('#'):
				next
			l = l.strip()
			i = shlex.shlex(l)
			op = Operande()
			t = [x for x in i]
			#print t
			op.name = t.pop(0)
			# param 1
			if t:
				d = t.pop(0)
				if d.startswith(("'", '"')):
					op.param1 = shlex.split(d).pop(0)
				else:
					op.param1 = d
			# param 2
			if t:
				d = t.pop(0)
				if d.startswith(("'", '"')):
					op.param2 = shlex.split(d).pop(0)
				else:
					op.param2 = d
			# param 3
			if t:
				d = t.pop(0)
				if d.startswith(("'", '"')):
					op.param3 = shlex.split(d).pop(0)
				else:
					op.param3 = d
			# param 4
			if t:
				d = t.pop(0)
				if d.startswith(("'", '"')):
					op.param4 = shlex.split(d).pop(0)
				else:
					op.param4 = d
			# param 5
			if t:
				d = t.pop(0)
				if d.startswith(("'", '"')):
					op.param5 = shlex.split(d).pop(0)
				else:
					op.param5 = d
			## et si il en reste ?
			if t:
				op.params = t
			p.append(op)

## ------------------------
## Petite routine de log
## ------------------------
def log(msg=''):
	now = datetime.datetime.now().time()
	print '%s : %s' % (now, msg)

## --------
## TEST
## --------
def test(fichier):
	log('Debut')
	M1 = Machine('TEST')
	log('Set Prog')
	set_prog_fic(fichier, M1.prog)
	log('Init')
	M1.mach_init()
	if M1.erreur:
		print "Erreur %s %s : " % (M1.erreur, M1.errlig)
	log('Boucle principale : ')
	EXIT = False
	while not EXIT:
		M1.tick()
		if M1.etat == WAITING:
			print "WAITING"
			r = raw_input('>')
			M1.tick(r)
		elif M1.etat == PRINTING:
			print "[%s]" % M1.data_out
		elif M1.etat == FINISHED:
			EXIT = True
		elif M1.etat == STOPPED:
			EXIT = True
		else:
			M1.liste_prog()
			print M1

	log('Avant la fin')
	print M1
	log('Fin')

if __name__ == '__main__':
	#fic = 'src/TEST1.txt'
	fic = 'src/TEST2.txt'
	if len(sys.argv) > 1:
		if os.path.exists(sys.argv[1]):
			fic = sys.argv[1]
	test(fic)
