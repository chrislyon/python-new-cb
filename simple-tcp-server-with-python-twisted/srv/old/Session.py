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

class Session(object):
    """
        Classe de base pour un session
    """
    def __init__(self):
        self.etape = 0                          # Etape en cours
        self.prompt = "<vide>"          # Prompt a afficher
        self.reponse = None                     # Reponse de l'utilisateur
        self.error = None
        self.EXIT = False                       # Fin du scenario
        self.saisie = False


    ## Les Prompts
    PR_ETAPE1  = 101

    ## Les Messages 
    VALID_OK    = 1000
    EXIT_ANNUL  = 1001

    ## Les Messages d'erreurs
    ERR_ETAPE   = 2000
    ERR_ETAPE1  = 2001

    lib_err = {
        VALID_OK:"VALIDATION BASE DE DONNEES : OK",
        EXIT_ANNUL:" ANNULATION DE LA TRANSACTION ",
        ERR_ETAPE:"Erreur ETAPE Scenario",
        ERR_ETAPE1:"Erreur pour TEST",
        PR_ETAPE1:'Saisir un chiffre entre 1 et 5: ',
    }

    def lib(self, err):
        """
            Retourne les libelles
        """
        return self.lib_err[err]

    # --------------------------
    # Scenario par defaut 
    # 0 : Init
    # 1 : Saisie Valeur
    # 2 : Fin 

    INIT        = 0
    ETAPE_1     = 1
    VERIF       = 2 
    VALIDATION  = 3

    def s_next(self):
        """
        Scenario par defaut
        => Ici pour test
        """
        if not self.EXIT:
            if self.etape == self.INIT:
                self.prompt = ""
                self.error = None
                self.saisie = False
                self.etape += 1

            elif self.etape == self.ETAPE_1:
                self.prompt = self.lib(self.PR_ETAPE1)
                self.saisie = True
                #self.error = None
                self.etape += 1

            elif self.etape == self.VERIF:
                self.saisie = False
                ## Verification 
                ## qui est dans reponse
                ## si c'est bon on incremente self.etape
                try:
                    r = int(self.reponse)
                except:
                    r = 0

                if r >= 1 and r <= 5:
                    self.error = None
                    self.etape += 1
                else:
                    self.error = self.ERR_ETAPE1
                    self.etape -= 1
                

            elif self.etape == self.VALIDATION:
                ## Validation on ecrit le tout
                ## si c'est bon
                self.error = self.VALID_OK
                self.etape = self.INIT
            else:
                ## On repart au debut
                self.error = self.ERR_ETAPE
                self.etape = self.INIT
        else:
            ## Exit
            self.saisie = False
            self.prompt = ""
            self.error = self.EXIT_ANNUL


        return self.EXIT, self.saisie, self.prompt, self.error

    def set_reponse(self, rep):
        """
        Traitement de la reponse
        """
        self.reponse = rep
        if rep in ('ANNUL', 'QUIT'):
            self.EXIT = True

        self.s_next()

    def __str__(self):
        """
            Pour debug
        """
        return "Etape : %s / Rep = %s / Sai = %s / Err = %s " % (self.etape, self.reponse, self.saisie, self.error )


## -------------------
## Classe MP
## -------------------

class Session_MP(Session):

    ## Les Prompts
    PR_DOSSIER  = 101
    PR_OPER     = 102
    PR_BOBINE   = 103

    ## Les Messages 
    VALID_OK    = 1000
    EXIT_ANNUL  = 1001

    ## Les Messages d'erreurs
    ERR_ETAPE   = 2000
    ERR_DOS     = 2001
    ERR_OPER    = 2002

    lib_err = {
        VALID_OK:"VALIDATION BASE DE DONNEES : OK",
        EXIT_ANNUL:" ANNULATION DE LA TRANSACTION ",
        ERR_ETAPE:"Erreur ETAPE Scenario",
        ERR_DOS:"Erreur Dossier inexistant",
        ERR_OPER:"Operation Incorrecte",
        PR_DOSSIER:'No Dossier :',
        PR_OPER:'Operation : ',
        PR_BOBINE:'No Bobine : ',
    }

    # ----------------------------------------
    # 0 : Init
    # 1 : Saisie du dossier
    # 2 : Verification du dossier
    # 3 : Saisie Operation (USER+OP+Etape)
    # 4 : Verification Operation
    # 5 : Saisie Bobine
    # 6 : Verification Bobine
    # 7 : Validation


    INIT            = 0
    DOSSIER         = 1
    VERIF_DOSSIER   = 2
    OPERATION       = 3
    VERIF_OPERATION = 4
    BOBINE          = 5
    VERIF_BOBINE    = 6
    VALIDATION      = 7


    def s_next(self):
        if not self.EXIT:
            if self.etape == self.INIT:
                self.dossier = None
                self.User = None
                self.Oper = None
                self.Op_Etape = None
                self.prompt = "<INIT>"
                self.error = None
                self.saisie = False
                self.etape += 1

            elif self.etape == self.DOSSIER:
                self.prompt = self.lib(self.PR_DOSSIER)
                self.saisie = True
                #self.error = None
                self.etape += 1

            elif self.etape == self.VERIF_DOSSIER:
                self.saisie = False
                ## Verification du dossier
                ## qui est dans reponse
                ## si c'est bon on incremente self.etape
                if self.reponse in ('1200', '1201'):
                    self.error = None
                    self.etape += 1
                else:
                    self.error = self.ERR_DOS
                    self.etape -= 1

            elif self.etape == self.OPERATION:
                self.reponse = None
                self.saisie = True
                self.prompt = self.lib(self.PR_OPER)
                #self.error = None
                self.etape += 1

            elif self.etape == self.VERIF_OPERATION:
                self.saisie = False
                self.prompt = ""
                ## Verification de l'operation
                if self.reponse in ('DIEDRMM', 'DIEFRMM' ):
                    self.error = None
                    self.etape += 1
                else:
                    self.error = self.ERR_OPER
                    self.etape -= 1
                    

            elif self.etape == self.BOBINE:
                self.reponse = None
                self.saisie = True
                self.prompt = self.lib(self.PR_BOBINE)
                self.etape += 1

            elif self.etape == self.VERIF_BOBINE:
                self.saisie = False
                self.etape += 1
                self.prompt = ""
                self.error = None

            elif self.etape == self.VALIDATION:
                ## Validation on ecrit le tout
                ## si c'est bon
                self.error = self.VALID_OK
                self.etape = self.INIT
            else:
                ## On repart au debut
                self.error = self.ERR_ETAPE
                self.etape = self.INIT
        else:
            ## Exit
            self.saisie = False
            self.prompt = ""
            self.error = self.EXIT_ANNUL


        return self.EXIT, self.saisie, self.prompt, self.error

## -------------------
## Classe MP
## -------------------

class Session_MPV2(Session):

    ## Les Prompts
    PR          = 100
    PR_DOSSIER  = PR+1
    PR_OPER     = PR+2
    PR_BOBINE   = PR+3

    ## Les Messages 
    MSG         = 1000
    VALID_OK    = MSG
    EXIT_ANNUL  = MSG+1

    ## Les Messages d'erreurs
    ERR         = 2000
    ERR_ETAPE   = ERR+0
    ERR_DOS     = ERR+1
    ERR_OPER    = ERR+2
    ERR_BOBINE  = ERR+3

    lib_err = {
        VALID_OK:"VALIDATION BASE DE DONNEES : OK",
        EXIT_ANNUL:" ANNULATION DE LA TRANSACTION ",
        ERR_ETAPE:"Erreur ETAPE Scenario",
        ERR_DOS:"Erreur Dossier inexistant",
        ERR_OPER:"Operation Incorrecte",
        ERR_BOBINE:"Bobine inexistante",
        PR_DOSSIER:'No Dossier :',
        PR_OPER:'Operation : ',
        PR_BOBINE:'No Bobine : ',
    }

    # ----------------------------------------
    # 0 : Init
    # 1 : Saisie du dossier
    # 2 : Verification du dossier
    # 3 : Saisie Operation (USER+OP+Etape)
    # 4 : Verification Operation
    # 5 : Saisie Bobine
    # 6 : Verification Bobine
    # 7 : Validation


    INIT            = 0
    DOSSIER         = 1
    VERIF_DOSSIER   = 2
    OPERATION       = 3
    VERIF_OPERATION = 4
    BOBINE          = 5
    VERIF_BOBINE    = 6
    VALIDATION      = 7


    def s_next(self):
        if not self.EXIT:
            if self.etape == self.INIT:
                self.dossier = None
                self.User = None
                self.Oper = None
                self.Op_Etape = None
                self.prompt = self.lib(self.PR_DOSSIER)
                self.error = None
                self.saisie = False
                self.etape += 1

            elif self.etape == self.DOSSIER:
                self.prompt = self.lib(self.PR_DOSSIER)
                self.saisie = True
                #self.error = None
                self.etape += 1

            elif self.etape == self.VERIF_DOSSIER:
                self.saisie = False
                #self.prompt = ""
                ## Verification du dossier
                ## qui est dans reponse
                ## si c'est bon on incremente self.etape
                if self.reponse in ('1200', '1201'):
                    self.error = None
                    self.etape = self.OPERATION
                else:
                    self.error = self.ERR_DOS
                    self.etape = self.DOSSIER

            elif self.etape == self.OPERATION:
                self.reponse = None
                self.saisie = True
                self.prompt = self.lib(self.PR_OPER)
                #self.error = None
                self.etape += 1

            elif self.etape == self.VERIF_OPERATION:
                self.saisie = False
                #self.prompt = ""
                ## Verification de l'operation
                if self.reponse in ('DIEDRMM', 'DIEFRMM' ):
                    self.error = None
                    self.etape = self.BOBINE
                else:
                    self.error = self.ERR_OPER
                    self.etape = self.OPERATION
                    

            elif self.etape == self.BOBINE:
                self.reponse = None
                self.saisie = True
                self.prompt = self.lib(self.PR_BOBINE)
                self.etape = self.VERIF_BOBINE

            elif self.etape == self.VERIF_BOBINE:
                self.saisie = False
                self.prompt = ""
                if self.reponse in ('111', '222', '333'):
                    self.error = None
                    self.etape = self.VALIDATION
                else:
                    self.error = self.ERR_BOBINE
                    self.etape = self.BOBINE

            elif self.etape == self.VALIDATION:
                ## Validation on ecrit le tout
                ## si c'est bon
                self.error = self.VALID_OK
                self.etape = self.INIT
            else:
                ## On repart au debut
                self.error = self.ERR_ETAPE
                self.etape = self.INIT
        else:
            ## Exit
            self.saisie = False
            self.prompt = ""
            self.error = self.EXIT_ANNUL


        return self.EXIT, self.saisie, self.prompt, self.error
               

def test_session():
    #pdb.set_trace()

    DEBUG = False

    ## A choisir
    s = Session()
    #s = Session_MP()
    #s = Session_MPV2()

    EXIT = False
    while not EXIT:
        if DEBUG:
            print " %s " % s

        EXIT, saisie, prompt, error = s.s_next()

        if saisie and not EXIT:
            if DEBUG:
                print "=" * 70
                print " %s " % s
            reponse = raw_input(prompt)
            s.set_reponse(reponse)

        if s.error > 1000 :
            print "ERREUR : %s " % s.lib(s.error)
        elif s.error is not None:
            print "> %s " % s.lib(s.error)

if __name__ == '__main__':
    test_session()
