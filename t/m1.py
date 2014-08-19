#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
##
##

# Operande

## Registre
## REGISTRE	0-9
## STATUS	True/False
## VARIABLE
## CONSTANTE

## 			INIT
## $DEBUT
## 			RAZ VAR
##			RAZ STATUS
##			RAZ REGISTRE
## $DOSSIER
##			PRINT "DOSSIER"
##			READ 
##			CALL VERIF_DOSSIER
##			JMP_FALSE $DOSSIER
## $OPERATION
##			PRINT "OPERATION"
##			READ
##			CALL VERIF_OPER
##			JMP_FALSE $OPERATION
## 
##			TEST CONSTANTE SAISIE_BOBINE
##			JMP_FALSE SUITE
## $BOBINE
##			PRINT "BOBINE"
##			READ
##			CALL VERIF_BOBINE
##			JMP_FALSE $BOBINE
## $SUITE
##			CALL MAJ
##			GOTO DEBUT

import datetime
import shlex
import pdb

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
WARN = 100
WARN_WAITING_DATA = WARN
WARN += 1
WARN_END_OF_PROG = WARN
WARN += 1
WARN_PRINTING = WARN

ERR = 1000
ERR_OP_INEXISTANTE = ERR
ERR += 1
ERR_PARAM_INEXISTANTE = ERR
ERR += 1
ERR_ETIQ_INEXISTANTE = ERR
ERR += 1
ERR_NO_PROG = ERR
ERR += 1
ERR_PARAM_OBLIGATOIRE = ERR
ERR += 1
ERR_PARAM_INCORRECT = ERR

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
			'STATUS', 'TEST', 'INIT'
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

	def raz_registre(self):
		for x in range(0,9):
			self.registres['REG%0d' % x] = ''

	def raz_status(self):
		self.status = False
		self.erreur = 0
		self.errlig = 0

	def mach_init(self):
		self.raz_registre()
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
			if self.erreur:
				print "SYNTAXE ERREUR %s %s" % (self.erreur, self.errlig)

	def check_line(self, op):
		op.ok = True
		if op.name not in self.OPERANDE:
			self.erreur = ERR_OP_INEXISTANTE
			self.errlig = op.no
		else:
			if op.name == 'INIT':
				pass
			elif op.name == 'READ':
				pass
			elif op.name in ('$', 'ETIQ'):
				if not op.param1:
					self.erreur = ERR_PARAM_OBLIGATOIRE
					self.ok = False
			elif op.name == 'CALL':
				pass
			elif op.name in ('GOTO', 'JMP_FALSE', 'JMP_TRUE'):
				if not op.param1:
					self.erreur = ERR_PARAM_OBLIGATOIRE
					self.ok = False
				if op.param1 not in self.etiq.keys():
					self.erreur = ERR_ETIQ_INEXISTANTE
					self.ok = False
			elif op.name == 'PRINT':
				if not op.param1:
					self.erreur = ERR_PARAM_OBLIGATOIRE
					self.ok = False
			elif op.name == 'RAZ':
				if not op.param1:
					self.erreur = ERR_PARAM_OBLIGATOIRE
					self.ok = False

	def liste_prog(self):
		for l in self.prog:
			print l

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
			self.erreur = WARN_END_OF_PROG
			self.errlig = 0

	def execute(self):
		if self.prog:
			op = self.prog[self.cursor-1]
			print "Executing : %s " % op

			if op.name == 'INIT':
				pass
			elif op.name == 'READ':
				pass
			elif op.name in ('$', 'ETIQ'):
				pass
			elif op.name == 'RAZ':
				if op.param1 == 'VAR':
					pass
				elif op.param1 == 'STATUS':
					self.raz_status()
				elif op.param1 == 'REGISTRE':
					self.raz_registre()
				else:
					self.etat = STOPPED
					self.erreur = ERR_PARAM_INCORRECT
					self.errlig = op.no
					op.ok = False
			elif op.name == 'PRINT':
				self.etat = PRINTING
				self.erreur = ERR_PARAM_INCORRECT
				self.errlig = op.no
				self.data_out = op.param1
			elif op.name == 'CALL':
				if op.param1:
					## On change le cursor
					pass
				else:
					self.erreur = ERR_PARAM_INEXISTANT
			elif op.name == 'GOTO':
					pass
			elif op.name == 'JMP_FALSE':
					pass
			elif op.name == 'TEST':
					pass
			else:
				self.erreur = ERR_OP_INEXISTANTE
		else:
			self.erreur = ERR_NO_PROG

	def tick(self, data = None):
		#pdb.set_trace()
		if data:
			pass
			## que faire des données
		while not self.erreur:
			self.inc_cursor()
			self.etat = RUNNING
			self.execute()
			if self.erreur and self.etat == RUNNING:
				print "Erreur %s %s" % (self.erreur, self.errlig)
				print "> %s " % self.prog[self.errlig]
			if self.etat == PRINTING:
				print ">%s" % self.data_out

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
def test():
	log('Debut')
	M = Machine('TEST')
	log('Set Prog')
	#set_prog(M.prog)
	set_prog_fic('TEST1.txt', M.prog)
	log('Init')
	M.mach_init()
	if M.erreur:
		M.liste_prog()
	log('Boucle principale : ')
	for x in range(0,9):
		M.tick()
		if M.erreur:
			M.liste_prog()
			print M
			
	log('Fin')

if __name__ == '__main__':
	test()
