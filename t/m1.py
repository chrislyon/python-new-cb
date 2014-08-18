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

import pdb

class Operande(object):
	def __init__(self, name):
		self.name = name
		self.no = 0
		self.param1 = ''
		self.param2 = ''

	def __str__(self):
		return 'OP:%s %0d %s %s' % \
			( self.no, self.name, self.param1, self.param2)
ERR = 1
ERR_OPER_INEXISTANTE = ERR
ERR += 1
ERR_PARAM_INEXISTANTE = ERR
ERR += 1
ERR_ETIQ_INEXISTANTE = ERR
ERR += 1
ERR_NO_PROG = ERR
ERR += 1

class Machine(object):

	def __init__(self, name):
		self.name = name
		self.registres = {}
		self.status = False
		self.variables = {}
		self.constantes = {}
		self.erreur = 0

		self.cursor = 0
		self.prog = []

		self.etiq = {}

		self.OPERANDE = [
			'$', 'ETIQ',
			'CALL',
			'JMP_FALSE', 'JMP_TRUE', 'GOTO'
			'CONSTANTE', 'VAR', 'VARIABLE', 'REGISTRE', 
			'PRINT', 'RAZ',
			'STATUS', 'TEST'
		]

	def __str__(self):
		R = 'MACH:%s status=%s erreur=%s' % (self.name, self.status, self.erreur)
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
		return R

	def mach_init(self):
		for x in range(0,9):
			self.registres['REG%0d' % x] = ''
		self.variables = {}
		self.status = False
		self.erreur = 0
		self.errlig = 0
		self.cursor = 0
		self.check_prog()

	def check_prog(self):
		## Numerotation + recup des etiquettes
		for op in self.prog:
			n =+ 1
			op.no = n
			if op.name in ('$', 'ETIQ'):
				self.etiq[op.param1] = op.no

		## Verification syntaxe
		for op in self.prog:
			self.check_line(op)

	def check_line(self, op):
		if op.name not in self.OPERANDE:
			self.erreur = ERR_OPER_INCONNU
		else:
			if op.name == 'INIT':
				pass
			elif op.name in ('$', 'ETIQ'):
				if not op.param1:
					self.erreur = ERR_ETIQ_INEXISTANTE
			elif op.name == 'CALL':
				pass
			elif op.name in ('GOTO', 'JMP_FALSE', 'JMP_TRUE'):
				if op.param1 not in self.etiq.keys():
					self.erreur = ERR_ETIQ_INEXISTANTE
			elif op.name == 'PRINT':
				pass	
			elif op.name == 'RAZ':
				pass


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

	def execute(self):
		if self.prog:
			op = self.prog[self.cursor]

			if op.name in ('INIT', 'READ'):
				if op.name == 'INIT':
					self.init()

				if op.param1:
					## on stocke l'etique + no ligne
					pass
				else:
					self.erreur = ERR_PARAM_INEXISTANT
			elif op == 'CALL':
				if op.param1:
					## On change le cursor
					pass
				else:
					self.erreur = ERR_PARAM_INEXISTANT
			elif op == 'GOTO':
					pass
			elif op == 'JMP_FALSE':
					pass
			elif op == 'PRINT':
					pass
			elif op == 'RAZ':
					pass
			elif op == 'TEST':
					pass
			else:
				self.erreur = ERR_OP_INEXISTANTE
		else:
			self.erreur = ERR_NO_PROG

	def tick(self, data = None):
		if data:
			pass
			## que faire des données
		self.inc_cursor()
		self.execute()

def test():
	M = Machine('TEST')
	M.mach_init()
	#pdb.set_trace()
	M.tick()
	print M

if __name__ == '__main__':
	test()
