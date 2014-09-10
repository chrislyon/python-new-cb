
# ----------------------
# Processeur Simpliste
# ----------------------

"""
    But :
    Permettre l'execution d'ordre du style

    LABEL <ETIQUETTE>
    PRINT <VALEUR>
    INPUT <VALEUR> <VAR>
    <VAR> = <VALEUR>
    LOOK <TABLE> <VALEUR>
    CHECK <CONDITION>
    <ETIQUETTE> IF TRUE
    <ETIQUETTE> IF FALSE

    <VAR> : Variable locale
    <VAR> : Variable Globale
    <VAR> : Variable Session
"""

import sys
import shlex
import pdb

class Processor():

    def __init__(self):
        self.exec_ptr = 0
        self.valid = False
        self.debug = False
        self.verbose = False

        self.prog = []
        self.instructions = []

        self.var = {}
        self.etiq = {}
        self.cmds = {}

        self.stdin = None
        self.stdout = None

        self.err_flag = False
        self.err_no = 0
        self.err_msg = ""

        self.make_cmds()

    def load(self, instructions ):
        """ Chargement du prog 
            On en profite pour virer 
            les lignes vides et les commentaires
            les espaces de debut et fin
        """
        self.instructions = instructions
        for i in instructions:
            l = i.rstrip()
            l = l.lstrip()
            if l.startswith('#'):
                continue
            if len(l) == 0:
                continue
            self.prog.append(l)

    def status(self):
        """
        Retourne l'etat de la machine
        """
        return self.err_flag, self.err_no, self.err_msg

    def error( self, code=None, msg=None ):
        """
        En cas d'erreur 
        """
        self.err_flag = True
        self.err_msg = msg
        self.err_no = code

    def check(self):
        """
        Verification du prog
        """
        self.valid  = False
        OK = True
        n = 0
        for l in self.prog:
            n += 1
            try:
                i = [ x for x in shlex.shlex(l) ]
                if self.verbose:
                    print "%04d : %-50s : %s" % (n, l, i)

                ## Si j'ai LABEL alors je stocke dans le dico
                if l.startswith('LABEL'):
                    self.etiq[i[1]] = n
            except:
                self.error( msg = "Err lig %s : %s" % (n, l) )
                OK = False
                break
        self.valid = OK

    def exec_i(self, instr):
        """
            Execution d'une ligne 
        """
        i = [ x for x in shlex.shlex(instr)]
        if i[0] in self.cmds:
            try:
                self.cmds[i[0]]( i[1:] )
            except:
                self.error(" Err Inst %s " % i)
        else:
            self.error( "Instr inex : %s " % i)


    def run(self):
        """
            Run = execution du programme est sorti
            sur certain cas de figure
        """
        if not self.valid:
            self.error( msg="PROG NOT VALID")
        else:
            for i in self.prog:
                self.exec_i(i)
                if self.stdout:
                    self.pr()
    def pr(self):
        print "P: %s" % self.stdout
        self.stdout = None

    def next(self):
        """
        A venir le but est de pouvoir lancer ligne par ligne
        """
        pass


    def make_cmds(self):
        """
            Le dictionnaire des commandes instructions
        """
        self.cmds = {
            'LABEL' : self.do_NOOP,
            'PRINT' : self.do_PRINT,
            'LET'   : self.do_LET,
        }

    ## ----------------
    ## Les commandes 
    ## ----------------
    def do_NOOP(self, args):
        """
            La plus facile = pass en python
        """
        if self.verbose:
            print "DO NOOP %s" % args

    def do_PRINT(self, args):
        """
            Commande PRINT : PRINT <VAR> ou PRINT <VALEUR>
        """
        if self.verbose:
            print "PRINT %s" % args
        if args[0] in self.var:
            v = self.var[args[0]]
        else:
            v = " ".join(args)
        self.stdout = v

    def do_LET(self, args):
        """
            Commande LET : Affectation de variable
        """

        if self.verbose:
            print "LET %s" % args

        if args[1] != '=':
            self.error( msg = 'LET : syntaxe incorrecte' )
        else:
            e = ''
            for i in args[2:]:
                if i in self.var:
                    e += "%s" % self.var[i]
                else:
                    e += "%s" % i
            try:
                self.var[args[0]] = eval(e)
            except:
                self.error("LET : syntaxe eval %s " % e)

    def do_DEF(self, args):
        """
            Commande par defaut affiche juste les arguments
        """
        print "DO DEF %s " % args

## -----
## TEST
## -----
def test():

    P = Processor()
    P.verbose = True

    if sys.argv[1]:
        try:
            f = open(sys.argv[1])
            PRG = f.readlines()
        except:
            print "Erreur fichier"
            sys.exit(1)
    else:
        PRG = [
            "LABEL DEBUT",
            "LET V = 'UNE CHAINE'",
            "LET V1 = 123",
            "INPUT 'Prompt a afficher' DOSSIER",
            "LOOK FIC_DOSSIER DOSSIER",
            "DEBUT IF FALSE",
            "CHECK V1 > V2",
            "PRINT 'HELLO WORLD'",
            "END",
            "",
        ]

    P.load( PRG )
    P.check()
    print "*** START RUNNING ***"
    P.run()
    print "*** END RUNNING ***"
    print "Status de Fin :" , P.status()
    print "LABEL         : %s " % P.etiq
    print "VAR           : %s " % P.var
    print "stdin         : %s " % P.stdin
    print "stdout        : %s " % P.stdout
    

if __name__ == '__main__':
    test()
