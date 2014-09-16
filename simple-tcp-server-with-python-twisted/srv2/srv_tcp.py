## --------------------------------
## Serveur TCP Simple Avec Twisted
## --------------------------------

##
## Origine : un exemple simple de server avec TWISTED
##

""" Simple TCP Server en Python """

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver

from optparse import OptionParser
import datetime
import time

from Sessions import Sessions
import session as S

import pdb


## ---------------
## Le protocole 
## ---------------
class MyServer(LineReceiver):
    """
    MyServer = Une instance de cette classe est un session 
    son but est de rapporter transmettre les echanges utilisateurs/serveurs
    mais aussi de gerer les evenements Debut / Fin de session
    il ne gerent que les commandes de bases : 
    => LIST
    => SHUTDOWN
    => QUIT
    => HELP (et encore)
    """
    ## =================================
    ## Quelques reponses None = defaut
    ## PING = PONG
    ## =================================
    answers = {
        #'':'',
        'PING' : 'PONG',
        None : '<defaut>'
    }

    def log(self, msg):
        """ log : affiche des infos sur le serveur en provenance du client """
        cli = "CLI %s:%s" % self.transport.client
        self.factory.log(cli, msg)

    def connectionMade(self):
        """ Creation de la session """
        self.factory.cnx.create_session(self)
        self.log("Connexion ... %s " % self)
        self.sendLine("Bienvenue ...\n ENTREE pour demarrer la session")
        ## Pour demarrer
        ##self.sendLine(self.factory.cnx.prompt(self))


    def connectionLost(self, reason):
        """ Fermeture de la session """
        self.log("Fin de connexion ...")
        ## Effacement de la session
        self.factory.cnx.remove_session(self)

    def lineReceived(self, line):
        """ Reception d'une ligne et gestion de la commande """
        self.log("=>[%s]" % line)
        if line == "SHUTDOWN":
            self.handle_SHUTDOWN()
        elif line == "QUIT":
            self.handle_QUIT()
        elif line == "LIST":
            self.handle_LIST()
        else:
            ## Reponse dans le tableau des reponses
            if self.answers.has_key(line):
                reponse = self.answers[line]
                self.sendLine(reponse)
                self.log("AUTO:%s" % reponse)
            else:
                ## On joue le scenario de la classe Session
				## Ici on envoie la reponse
				#self.factory.cnx.set_reponse(self, line)
				if line.strip():
					EXIT = False
					while not EXIT:
						self.factory.cnx.tick(self)
						ETAT = self.factory.cnx.get_ETAT(self)
						if ETAT == S.WAITING:
							self.factory.cnx.set_INPUT(self,line)
							EXIT = True
						elif ETAT == S.PRINTING:
							rep = self.factory.cnx.get_OUTPUT(self)
							self.log(rep)
							self.sendLine(">%s " % rep)
							self.factory.cnx.clear_OUTPUT(self)
						elif ETAT == S.ERR_VERIF:
							E = self.factory.cnx.get_ERROR(self)
							self.log( "ERREUR => %s " % E )
							self.sendLine(" ERREUR %s " % E)
						elif ETAT == S.FINISHED:
							self.log( "FINISHED " )
							EXIT = True
						elif ETAT == S.STOPPED:
							self.log( "STOPPED => %s " % self.factory.cnx.get_ERROR(self) )
							EXIT = True
						else:
							self.log( "Erreur ETAT inconnue" )
							EXIT = True


    ## -----------------
    ## Fonction Interne
    ## -----------------
    def handle_LIST(self):
        """ commande LIST """
        #pdb.set_trace()
        for v in self.factory.cnx.values():
            self.sendLine(" - %s" % v)

    def handle_QUIT(self):
        """ Commande de fermeture de session """
        reponse = "Ok au revoir ..."
        self.sendLine(reponse)
        self.transport.loseConnection()

    def handle_SHUTDOWN(self):
        """ Commande arret de serveur """
        self.log( "Shutdown demande" )
        self.factory.shutdown()
        

## -----------------------------
## La fabrique
## -----------------------------
class MyFactory(Factory):
    """ La classe fabrique de server """
    protocol = None
    fp = None
    shutdown = False

    def __init__(self, options=None):
        self.options = options
        self.ficlog = options.FICLOG
        self.cnx = Sessions()      # Les sessions

    def startFactory(self):
        """ Demarrage du serveur """
        if self.ficlog:
            self.fp = open(self.ficlog, 'a')
        self.log("SRV", "Init du serveur")

    def stopFactory(self):
        """ Arret du serveur """
        self.log("SRV", "Arret du serveur")
        if self.ficlog:
            self.fp.close()

    ## ----------------------------
    ## Shutdown Utilise cnx
    ## ----------------------------
    def shutdown(self):
        """ Demande de shutdown 
        on coupe la connexion de toutes les sessions
        """
        self.log("SRV", "Shutdown demande ...")
        self.shutdown = True
        for c in self.cnx.all_session():
            c.transport.loseConnection()
        reactor.stop()

    def log(self, origine, msg):
        """ Log => envoi de message sur le fichier de log """
        msg = "%s :  %s \n" % (origine, msg)
        if self.options.VERBOSE:
            print msg,
        if not self.shutdown:
            self.fp.write(msg)

## ----------------------
## Procedure principale
## ----------------------
def main():
    """ Pour Lancement """
    ## -------------------------------
    ## Analyse de la ligne de commande
    ## -------------------------------

    parser = OptionParser( add_help_option=None )

    # La fonction Aide
    parser.add_option( '-h', '--help', action='help', \
                        help="Affiche l'aide et c'est tout")

    parser.add_option('-f', "--fic", dest="FICLOG", 
                        help="Fichier LOG")

    parser.add_option('-v', "--verbose", dest="VERBOSE", \
                        default=True, action="store_true", \
                        help="Mode verbeux stdin")

    (options, args) = parser.parse_args()

    ## ------------------------
    # Magique :)
    ## Creation de la Factory
    ## ------------------------
    factory = MyFactory(options)
    factory.protocol = MyServer

    ## ------------------------
    ## Demarrage du serveur
    ## ------------------------
    reactor.listenTCP(1202, factory)
    reactor.run()

if __name__ == '__main__':
    main()
