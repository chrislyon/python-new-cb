#!/usr/bin/env python
# -*- coding: utf-8 -*-
## -----------------------------------
## Essai de recreer CODBAR en python
## -----------------------------------


import pudb

ETAPE_INIT		= 0
ETAPE_DOSSIER	= 1
ETAPE_OPERATION	= 2
ETAPE_BOBINE	= 3
ETAPE_MAJ 		= 4
ETAPE_MAX		= 5

class POSTE(object):
	def __init__(self):
		self.pid = 0					#Id Unique
		self.name = ""					#Nom du poste
		self.pch = ""					#Poste de Charge

		self.etape = 0					#Etape de la transaction

		self.dossier = 0				#No Dossier en cours

		self.user = ""					#User operation en cours
		self.oper = ""					#Operation en cours
		self.machine = ""				#Machine en cours

		self.d_dossier = 0				#Dernier Dossier
		self.d_user = ""				#Dernier user
		self.d_oper = ""				#Derniere operation
		self.d_machine = ""				#Derniere machine

		self.MODE_ADMIN = False			#Mode ADMIN (shutdown)
		self.MODE_MULTI = False			#Mode MULTI => scenerio
		self.MULTI_DOSSIER = []			#Dossier(s) mode Multi
		self.MULTI_OPER = ""			#Operation sur mode Multi
		self.historic = []				#Historic des commandes
		self.term = ""					#Type de Terminal
		self.BOBINE_SAISIE = ""			#Bobine a saisir ?
		self.BOBINE_MODIF = False		#Bobine a modifier
		self.NUMBO = []					#No de Bobine
		self.NB_BOB_SAISIE = 0			#Nb de bobine(s) saisie(s)
		self.NBFOLIO = 0				#Nb de Feuillet dossier

	def raz(self):
		## 
		self.d_dossier = self.dossier
		self.d_user = self.user
		self.d_oper = self.oper
		self.d_machine = self.machine
		# Historique ...
		## Raz
		self.dossier = 0
		self.user = ""
		self.oper = ""
		self.machine = ""
		self.etape = 0

	def mise_a_jour(self):
		return "MISE A JOUR OK"

	def calc_prompt(self, NL=True):
		if self.etape == 0:
			p = "DOSSIER :"
		elif self.etape == 1:
			p = "OPERATION :"
		elif self.etape == 2:
			p = "BOBINE :"
		else:
			p = "DOSSIER.:"

		R = "[ %s ]" % p
		if NL:
			R += "\n"
		return R

	def verif_dossier(self, dossier):
		self.dossier = dossier
		self.next_etape()
		return 'OK'

	def verif_oper(self, oper):
		self.user = oper[:3]
		self.oper = oper[3]
		self.machine = oper[4:]
		self.next_etape()
		return 'OK'

	def verif_bobine(self, bobine):
		self.next_etape()
		return 'OK'

	## -------------------------------------------------
	## Determine comment on passe d'une etape a l'autre
	## -------------------------------------------------
	def next_etape(self):
		## Calcule de l'étape
		if self.dossier == 0:
			self.etape = ETAPE_DOSSIER
			return
		else:
			if self.oper == "":
				self.etape = ETAPE_OPERATION
				return

		## Si j'ai une operation et que je dois 
		## saisir une bobine
		if self.oper and self.BOBINE_SAISIE:
			self.etape = ETAPE_BOBINE
			return
		else:
			self.ETAPE = ETAPE_MAJ


	def scenario(self, cmd):
		MSG = ''
		## calcule de l'etape
		self.next_etape()
		## Gestion
		if self.etape == ETAPE_INIT:
			self.raz()
		elif self.etape == ETAPE_DOSSIER:
			## On verifie le dossier
			MSG = self.verif_dossier(cmd)
		elif self.etape == ETAPE_OPERATION:
			## On verifie l'operation
			MSG = self.verif_oper(cmd)
		elif self.etape == ETAPE_BOBINE:
			if self.BOBINE_SAISIE:
				## Si besoin saisie de la bobine
				MSG = self.verif_bobine(cmd)
		elif self.etape == ETAPE_MAJ:
			MSG = self.mise_a_jour()
			self.etape = ETAPE_INIT
		else:
			MSG = 'ERREUR ETAPE INCONNUE : %s ' % cmd
		rself.pr()
		return MSG

	def pr(self):
		return "Dos=%s Etape=%s oper=%s User=%s Mach=%s Folio=%s Bobines=%s" % \
			(self.dossier, self.etape, self.oper, self.user, self.machine, self.NBFOLIO, self.NUMBO)

def cli_log(msg):
	print "CLI: %s " % msg

def srv_log(msg):
	print "SRV: %s " % msg


## ===================================================================================================

## ------------------------
## recup de la commande
## ------------------------
def get_cmd():
	r =  raw_input('>')
	return r.upper()

## --------------------------
## Execution de la commande
## --------------------------
def do_cmd(cmd):
	global EXIT, MULTI
	srv_log( "do_cmd %s " % cmd )

	RETOUR = 'CMD_OK'

	if cmd in ( "EXIT", "QUIT" ):
		EXIT = True
	elif cmd == "MULTI":
		pass
	elif cmd == "NOMULTI":
		pass
	elif cmd == "SHUTDOWN":
		pass
	elif cmd == "WHO":
		pass
	elif cmd == "ANNUL":
		pass
	elif cmd == "AFFICH":
		pass
	elif cmd == "STATUS":
		pass
	elif cmd == "GLOBAL":
		pass
	elif cmd == "ENCOURS":
		pass
	elif cmd == "HISTORIC":
		pass
	elif cmd == "PARAM":
		pass
	elif cmd == "PCH":
		pass
	else:
		RETOUR = P.scenario(cmd)

	srv_log(RETOUR)
	return RETOUR

## =========================
## Boucle principale
## =========================
EXIT=False
MULTI=False

srv_log( "DEBUT" )

P = POSTE()


while not EXIT:
	cli_log(P.calc_prompt(NL=False))
	cmd = get_cmd()
	R = do_cmd(cmd)

srv_log( "FIN" )
