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

    def __init__(self):
        self.etape = 0
        self.libel = {}
        self.saisie = {}
        self.f_check = {}

    def reponse(self, args ):
        verif = self.f_check[self.etape]
        if verif:
            return verif( args )
        else:
            return True
            
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
        if self.etape > 4:
            self.valid()
            self.start()
            return True
        else:
            return False

## ---------------------
## Classe Specifique
## ---------------------
class Session_MP(Session):
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
        self.f_check[2] = None
        self.f_check[3] = None
        self.f_check[4] = None

    def start(self):
        self.etape = 0

    def valid(self):
        print "\t\t Validation"

    def verif_dossier(self, args ):
        print "CHECK DOSSIER %s " % args
        if not args:
            print "Dossier incorrecte"
            return False
        else:
            return True

## -----------------------
## La Procedure de TEST
## -----------------------
def test():
    s = Session_MP()
    QUIT = False
    while not QUIT:
        running = True
        while running:
            prompt = s.prompt()
            if s.saisie_user():
                r = raw_input("> %s " % prompt)
                if r == "QUIT":
                    QUIT = True
                    break
                if not s.reponse(r):
                    continue
            else:
                print prompt
            running = not s.End_Of_Session()
    else:
        print "Fin de session ..."

if __name__ == '__main__':
    test()
