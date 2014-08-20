#!/usr/bin/env python
# -*- coding: utf-8 -*-

## ---------------------------
## MACHINEVIRTUELLE en PYTHON
## ---------------------------

import sys, traceback
import datetime
import shlex
import pdb


class Err(Exception):
	def __init__(self, raison="<vide>", nolig=0):
		self.raison = raison
		self.nolig = nolig

	def __str__(self):
		return "%s : %s " % (self.nolig, self.raison)

class Printing(Exception):
	def __init__(self, raison="<vide>", nolig=0):
		self.raison = raison
		self.nolig = nolig

	def __str__(self):
		return "%s : %s " % (self.nolig, self.raison)

class Waiting(Exception):
	def __init__(self, raison="<vide>", nolig=0):
		self.raison = raison
		self.nolig = nolig

	def __str__(self):
		return "%s : %s " % (self.nolig, self.raison)

class EndOfProg(Exception):
	def __init__(self, raison="<vide>", nolig=0):
		self.raison = raison
		self.nolig = nolig

	def __str__(self):
		return "%s : %s " % (self.nolig, self.raison)


class Operande(object):
	def __init__(self, name=''):
		self.name = name
		self.no = 0
		self.param1 = ''
		self.param2 = ''
		self.ok = False

	def __str__(self):
		return '%03d : OP:%-10.10s : %-5.5s : %s %s' % \
			( self.no, self.name, self.ok, self.param1, self.param2)
ETAT = 1
STOPPED  = ETAT
ETAT += 1
CHECKING  = ETAT
ETAT += 1
RUNNING  = ETAT
ETAT += 1
WAITING  = ETAT
ETAT += 1
PRINTING = ETAT
ETAT += 1
FINISHED = ETAT

class Machine(object):

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
			'$', 'ETIQ',
			'CALL',
			'JMP_FALSE', 'JMP_TRUE', 'GOTO',
			'CONSTANTE', 'VAR', 'VARIABLE', 'REGISTRE', 
			'PRINT', 'RAZ',
			'READ',
			'STATUS', 'TEST', 'INIT', 'END'
		]

	def __str__(self):
		R = 'MACH:%s status=%s erreur=%s errlig=%s' % (self.name, self.status, self.erreur, self.errlig)
		R += '\n'
		R += 'Registres    : \n'
		r = self.registres.items()
		r.sort()
		for x in r:
			R += '%s = %s\n' % x
		R += '\n'
		R += 'Variable(s)  : \n'
		for k,v in self.variables.items():
			R += 'VAR %s = %s\n' % (k,v)
		R += '\n'
		R += 'Constante(s) : \n'
		for k,v in self.constantes.items():
			R += 'CONST %s = %s\n' % (k,v)
		R += '\n'
		R += 'Etiquette(s) : \n'
		for k,v in self.etiq.items():
			R += 'ETIQ %s = %s\n' % (k,v)
		R += '\n'
		return R

	def raz_registres(self):
		for x in range(0,9):
			self.registres['REG%0d' % x] = ''

	def raz_status(self):
		self.status = False
		self.erreur = 0
		self.errlig = 0

	def mach_init(self):
		self.raz_registres()
		self.variables = {}
		self.status = False
		self.erreur = 0
		self.errlig = 0
		self.cursor = 0
		self.check_prog()

	def check_prog(self):
		self.etat = CHECKING
		## Numerotation + recup des etiquettes
		n = 0
		for op in self.prog:
			n += 1
			op.no = n
			if op.name in ('$', 'ETIQ'):
				self.etiq[op.param1] = op.no

		## Verification syntaxe
		for op in self.prog:
			#if op.name == 'GOTO':
			#	pdb.set_trace()
			self.check_line(op)

	def check_line(self, op):
		op.ok = False
		if op.name not in self.OPERANDE:
			raise Err("Instruction inexistante", op.no)
		else:
			if op.name in ('$', 'ETIQ'):
				if not op.param1:
					raise Err("Parametre obligatoire", op.no)
			elif op.name == 'CALL':
				if not op.param1:
					raise Err("Function obligatoire", op.no)
			elif op.name in ('GOTO', 'JMP_FALSE', 'JMP_TRUE'):
				if not op.param1:
					raise Err("Parametre obligatoire", op.no)
				if op.param1 not in self.etiq.keys():
					raise Err("Etiquette inexistante", op.no)
			elif op.name == 'PRINT':
				if not op.param1:
					raise Err("Parametre obligatoire", op.no)
			elif op.name == 'RAZ':
				if not op.param1:
					raise Err("Parametre obligatoire", op.no)
		##
		op.ok = True

	def liste_prog(self):
		for l in self.prog:
			print l

	## -------------------------------
	## Gestion du cursor d'execution
	## -------------------------------
	def inc_cursor(self):
		n = self.cursor
		n += 1
		self.set_cursor(n)

	def dec_cursor(self):
		n = self.cursor
		n -= 1
		self.set_cursor(n)

	def set_cursor(self, n):
		self.cursor = n
		if n > 0 and n < len(self.prog):
			self.cursor = n
		else:
			self.etat = STOPPED
			raise EndOfProg("End Of Prog", 0)

	##-------------------------
	## Le processeur
	##-------------------------
	def execute(self):
		if self.prog:
			op = self.prog[self.cursor-1]
			print "Executing : %s " % op

			if op.name == 'INIT':
				pass
			elif op.name == 'END':
				pass
			elif op.name == 'READ':
				if self.data_in:
					self.registres[op.param1] = self.data_in
					self.data_in = None
				else:
					self.etat = WAITING
					raise Waiting("READ",op.no)
			elif op.name in ('$', 'ETIQ'):
				pass
			elif op.name == 'RAZ':
				if op.param1 == 'VAR':
					pass
				elif op.param1 == 'STATUS':
					self.raz_status()
				elif op.param1 == 'REGISTRE':
					self.raz_registres()
				else:
					self.etat = STOPPED
					raise ("Parametre incorrect", op.no)
					op.ok = False
			elif op.name == 'PRINT':
				self.etat = PRINTING
				self.data_out = op.param1
				raise Printing("PRINT", op.no)
			elif op.name == 'CALL':
				if op.param1:
					## On change le cursor
					pass
				else:
					raise Err(raison="Parametre inexistant", nolig=op.no)
			elif op.name == 'GOTO':
				c = self.etiq[op.param1]
				self.set_cursor(c)
			elif op.name == 'JMP_FALSE':
					pass
			elif op.name == 'TEST':
					pass
			else:
				raise Err(raison="Operation inconnue", nolig=op.no)
		else:
			raise EndOfProg()

	## -----------------------------
	## Execution d'une instruction 
	## -----------------------------
	def tick(self, data=None):
		EXIT = False
		user_input = data
		while not EXIT:
			if not user_input:
				self.inc_cursor()
			else:
				self.data_in = user_input
				user_input = None
			## On continue
			self.etat = RUNNING
			try:
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
				print("Erreur :")
				print("-"*60)
				traceback.print_exc(file=sys.stdout)
				print("-"*60)
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
			i = shlex.split(l)
			op = Operande()
			op.name = i[0]
			if len(i) >= 2:
				op.param1 = i[1]
			if len(i) == 3:
				op.param1 = i[2]
			p.append(op)
	
## ------------------------
## Petite routine de log
## ------------------------
def log(msg=''):
	now = datetime.datetime.now().time()
	print '%s : %s' % (now,msg)

## --------
## TEST
## --------
def test(fichier):
	log('Debut')
	M = Machine('TEST')
	log('Set Prog')
	set_prog_fic(fichier, M.prog)
	log('Init')
	M.mach_init()
	if M.erreur:
		print "Erreur %s %s : " % (M.erreur, M.errlig)
	log('Boucle principale : ')
	EXIT = False
	while not EXIT:
		M.tick()
		if M.etat == WAITING:
			print "WAITING"
			r = raw_input('>')
			M.tick(r)
		elif M.etat == PRINTING:
			print "[%s]" % M.data_out
		elif M.etat == FINISHED:
			EXIT = True
		else:
			M.liste_prog()
			print M
			
	log('Fin')

if __name__ == '__main__':
	f = 'src/TEST1.txt'
	f = 'src/TEST2.txt'
	test( f )
