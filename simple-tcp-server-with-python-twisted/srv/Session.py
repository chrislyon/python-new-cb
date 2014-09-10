##
## 
##

import pdb
import json
from message import Message

class Session(object):
    """
        Classe de base pour un session
    """
    def __init__(self):
        self.etape = 1                          # Etape en cours
        self._prompt = ""                       # Prompt a afficher    
        self.reponse = None                     # Reponse de l'utilisateur
        self._error = None                       # Flag Erreur
        self._resultat = "<vide>"               # Message a afficher
        self.EXIT = False                       # Sortie

    # =============================
    def _compute(self):
        """
        ----------------------------------
            Traitement de la session
        ----------------------------------
        """

        self._resultat = ""
        self._error = False

        if self.etape == 1:
            ## Etape = 1 => je dois saisir un dossier
            if self.reponse:
                ## Verification 
                if self.reponse == "100":
                    ## Ok
                    self._error = False
                    self.etape += 1
                    self._resultat = "DOSSIER OK"
                else:
                    ## Pas Ok
                    self._error = True
                    self._resultat = "Dossier incorrect"
        elif self.etape == 2:
            ## Etape 2 => j'ai un dossier valide
            ## Je demande un operation
            if self.reponse:
                # verification
                if self.reponse == "OP1":
                    ## Ok
                    self._error = False
                    self.etape += 1
                    self._resultat = "OPERATION OK"
                else:
                    ## Pas Ok
                    self._error = True
                    self._resultat = "operation incorrecte"

        ## Etape 3 => DOSSIER + OPER Ok je valide
        ## et je repars pour un tour
        if self.etape == 3:
            self._error = False
            self.etape = 1
            self._resultat = "VALIDATION"

    # =============================
    def set_reponse(self, rep):
        """
        Traitement de la reponse
        """
        self.reponse = rep
        if rep in ('ANNUL', 'QUIT'):
            self._prompt = "SORTIE"
            self._resultat = "SORTIE"
            self.EXIT = True
        else:
            self._compute()

    # =============================
    def resultat(self):
        """
            Retourne le resultat
        """
        if self._resultat:
            p = self._resultat
        else:
            p = "<vide>"
        return "Resultat [%s:%s]" % (self.etape, p)

    # =============================
    def error(self):
        """
        Retourne erreur
        """
        return self._error

    # =============================
    def prompt(self):
        """
            retourne le prompt
        """
        if self.etape <=1:
            p = "No DOSSIER : "
        elif self.etape == 2:
            p = "Operation :"
        else:
            p = "VALIDATION"
        return "[%s:%s]" % (self.etape, p)

    # =============================
    def __str__(self):
        """
            Pour debug
        """
        return "Etape : %s / Rep = %s / Res = %s / Err = %s " % (self.etape, self.reponse, self._resultat, self._error )

## -------------
## Session JSON
## -------------
class Session_JSON(Session):

    def prompt(self):
        return ""

    ## ---------------------------------------------------------------------
    ## Dans reponse soit un ordre (ANNUL / QUIT) ou un Message format json
    ## ---------------------------------------------------------------------
    def _compute(self):
        rep = self.reponse
        if Message.JSON_TAG in rep:
            M = Message()
            M.from_json(rep)
            ## Traitement du message
            self.compute_msg(M)
        else:
            if rep in ("ANNUL", "QUIT"):
                self._error = False
                self.EXIT = True
            else:
                self._error = True
                self._resultat = "COMMANDE INCONNUE"

    def compute_msg(self, Msg):
        Ret = Message()
        Ret.msg_status = Message.OK
        ## demande de liste
        if Msg.msg_info == 'REQ LIST':
            if Msg.msg_data == 'OPERATOR':
                Ret.msg_info = 'SEND LIST OPERATOR'
                Ret.msg_data = [ 'OPER1', 'OPER2', 'OPER3' ]
                self._error = False
            elif Msg.msg_data == 'MACHINE':
                Ret.msg_info = 'SEND LIST MACHINE'
                Ret.msg_data = [ 'MACH1', 'MACH2', 'MACH3' ]
                self._error = False
            else:
                Ret.msg_status = Message.KO
                Ret.msg_info = 'SEND LIST'
                Ret.msg_data = 'FICHIER INCORRECT'
                self._error = True
        ## Autre chose 
        else:
            Ret.msg_info = 'DEMANDE INCONNUE'
            Ret.msg_status = Message.KO
            self._error = True
        self._resultat = Ret.to_json()

    def set_reponse(self,rep):
        self.reponse = rep
        self._compute()

    def resultat(self):
        return self._resultat
        

    

def test():
    pdb.set_trace()

    DEBUG = True

    #s = Session()
    s = Session_GR()

    print "Debut : " , s.prompt()

    EXIT = False
    while not EXIT:
        if DEBUG:
            print " %s " % s

        reponse = raw_input('>')

        if reponse == "REQ LIST OPERATOR":
            M = Message()
            M.msg_status = Message.OK
            M.msg_info = 'REQ LIST'
            M.msg_data = 'OPERATOR'
            reponse = M.to_json()

        if reponse == "REQ LIST MACHINE":
            M = Message()
            M.msg_status = Message.OK
            M.msg_info = 'REQ LIST'
            M.msg_data = 'MACHINE'
            reponse = M.to_json()

        s.set_reponse(reponse)

        if s.error():
            print "ERREUR : %s " % s.resultat()
        else:
            print "> %s " % s.resultat()

        if s.EXIT:
            print "SORTIE ..."
            EXIT = True
        else:
            print s.prompt()

if __name__ == '__main__':
    test()
