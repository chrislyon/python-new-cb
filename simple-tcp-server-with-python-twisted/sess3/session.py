##
## 
##

import pdb

class Session(object):
    """
        Classe de base pour un session
    """
    def __init__(self):
        self.etape = 1                          # Etape en cours
        self._prompt = ""                       # Prompt a afficher    
        self.reponse = None                     # Reponse de l'utilisateur
        self.error = None                       # Flag Erreur
        self._resultat = "<vide>"               # Message a afficher
        self.EXIT = False                       # Sortie

    # =============================
    def compute(self):
        """
        ----------------------------------
            Traitement de la session
        ----------------------------------
        """

        self._resultat = ""
        self.error = False

        if self.etape == 1:
            ## Etape = 1 => je dois saisir un dossier
            if self.reponse:
                ## Verification 
                if self.reponse == "100":
                    ## Ok
                    self.error = False
                    self.etape += 1
                    self._resultat = "DOSSIER OK"
                else:
                    ## Pas Ok
                    self.error = True
                    self._resultat = "Dossier incorrect"
        elif self.etape == 2:
            ## Etape 2 => j'ai un dossier valide
            ## Je demande un operation
            if self.reponse:
                # verification
                if self.reponse == "OP1":
                    ## Ok
                    self.error = False
                    self.etape += 1
                    self._resultat = "OPERATION OK"
                else:
                    ## Pas Ok
                    self.error = True
                    self._resultat = "operation incorrecte"

        ## Etape 3 => DOSSIER + OPER Ok je valide
        ## et je repars pour un tour
        if self.etape == 3:
            self.error = False
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
            self.compute()

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
        return "Etape : %s / Rep = %s / Res = %s / Err = %s " % (self.etape, self.reponse, self._resultat, self.error )


def test():
    pdb.set_trace()

    DEBUG = True

    s = Session()

    print "Debut : " , s.prompt()

    EXIT = False
    while not EXIT:
        if DEBUG:
            print " %s " % s

        reponse = raw_input('>')
        s.set_reponse(reponse)

        if s.error:
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
