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
from UserDict import UserDict
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
    ## A part faire des tests je ne vois pas ce que je peu faire avec ca
    ## =================================
    answers = {
        'HELP' : 'QUIT / SHUTDOWN / LIST',
        'WHO I AM' : 'Bonjour je suis un serveur TCP',
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
        self.sendLine("Bienvenue ...")
        self.sendLine(self.factory.cnx.prompt(self))

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
            if self.answers.has_key(line):
                reponse = self.answers[line]
            else:
                ## Scenario ICI
                reponse = self.factory.cnx.commande(self, line)
                ## Avant ?
                #reponse = self.answers[None]

            ## La reponse
            self.log( "<=[%s]" % reponse )
            self.sendLine(reponse)
            self.sendLine(self.factory.cnx.prompt(self))

    ## -----------------
    ## Fonction Interne
    ## -----------------
    def handle_LIST(self):
        """ commande LIST """
        #pdb.set_trace()
        for v in self.factory.cnx.values():
            self.sendLine(v.liste())

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


## =====================
## Gestion des sessions
## =====================

## ============================
## Notes :
## ============================

# -----------------------------------------------------------------------------------------------------------------------
# Une session = Stocke l'etat des varaibles
# Un scenario :
#   Suite d'instruction du style
#   Question / Reponse  / verifcation / Action
#   Ex:
#   Question - Libelle / reponse attendu (format) / Liste de fonctions de controle / Actions
#   DOSSIER           / No Dossier i             / Existe dans table Dossiers     / Ecrire dans Session
#   OPERATION        / USER+CODE_OP+MACHINE     / 
#                                               Verif user / code op / Machine
#                                               Verif classique (fin / debut)
#                                               Verif coherence                 / Ecrire dans session
#   BOBINE        / No Bobine               / Existe dans table bobine         / Ecrire dans session
#   VALIDATION   / Implicite               / Verif coherence                  / Ecrire dans session + Ecrire dans BDD
# -----------------------------------------------------------------------------------------------------------------------

## -----------------
## Classe Session
## -----------------

class Session():
    """ Classe de session generique 
    A verifier de la genericite 
    """

    def __init__(self):

        self.no = 0
        self.name = ""
        self.session = None
        self.client = None

        self.etape = 0
        self.max_etape = 4
        self.libel = {}
        self.saisie = {}
        self.f_check = {}

    def commande(self, args ):
        r = True
        msg = "<vide>"
        ## ON recupere une fonction de verification
        func_verif = self.f_check[self.etape]
        ## Si elle existe on execute
        if func_verif:
            r, msg = func_verif( args )

        ## Si la verif est bonne (r=True) 
        ## On passe a l'etape suivante
        if r:
            self.End_Of_Session()
        return msg
            
    def liste(self):
        r = ''
        r += '%3s ' % self.no
        r += '%10s ' % self.client
        r += '%20s ' % self.name
        r += '%2s ' % self.etape
        return r

    def saisie_user(self):
        return self.saisie[self.etape]
        
    def prompt(self):
        return self.libel[self.etape]

    def start(self):
        self.etape = 0

    def valid(self):
        pass

    def End_Of_Session(self):
        self.etape += 1
        if self.etape > self.max_etape:
            self.valid()
            self.start()


## ---------------------
## Classe Specifique
## ---------------------
class Session_TEST(Session):
    """ Classe de session specifique  """
    def __init__(self):
        Session.__init__(self)
        self.libel[0] = "DEMARRAGE"
        self.libel[1] = "Dossier :"
        self.libel[2] = "Operation : "
        self.libel[3] = "Bobine : "
        self.libel[4] = "Validation"

        self.saisie[0] = False
        self.saisie[1] = True
        self.saisie[2] = True
        self.saisie[3] = True
        self.saisie[4] = False

        self.f_check[0] = None
        self.f_check[1] = self.verif_dossier
        self.f_check[2] = self.verif_oper
        self.f_check[3] = self.verif_bobine
        self.f_check[4] = None

    def start(self):
        self.etape = 0

    def valid(self):
        return "Validation "

    ## Exemple de fonction verifiante
    ## Doit retourner un Booleen + un message
    def verif_oper(self, args):
        if not args:
            return False, "Operation Obligatoire"
        else:
            return True, ""

    def verif_bobine(self, args):
        if not args:
            return False, "Bobine Obligatoire"
        else:
            return True, ""

    def verif_dossier(self, args ):
        if not args:
            return False, "Dossier Incorrect %s" % args
        else:
            return True, ""

## --------------------------
## Gestion des sessions 
## Creation / effacement
## ensemble 
## --------------------------
class Sessions(UserDict):
    """ Gestion des sessions """
    nb = 0

    def __init__(self):
        UserDict.__init__(self)

    ## Creation de cle (les tuples transport.client mettent la grouille)
    def create_key(self, client):
        """ Creation de cle , les tuples faussent certaines fonctions """
        return "%s:%s" % client

    def create_session(self, New_Instance):
        """ Creation de session """
        Sessions.nb += 1
        ## Ici c'est pas TOP il faudrait transmettre 
        ## la classe en parametre
        s = Session_TEST()
        s.no = Sessions.nb
        s.name = "Session %s" % s.no
        s.client = self.create_key(New_Instance.transport.client)
        s.session = New_Instance
        self[s.client] = s
        ## Demarrage 
        s.start()

    def remove_session(self, s):
        """ Retrait de session """
        k = self.create_key(s.transport.client)
        del self[k]

    def all_session(self):
        """ retourne les sessions pour SHUTDOWN """
        return [ x.session for x in self.values() ]

    def prompt(self, instance):
        cle = self.create_key(instance.transport.client)
        return self[cle].prompt()

    def commande(self, instance, reponse):
        cle = self.create_key(instance.transport.client)
        return "%s" % self[cle].commande(reponse)


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
    reactor.listenTCP(1201, factory)
    reactor.run()

if __name__ == '__main__':
    main()
