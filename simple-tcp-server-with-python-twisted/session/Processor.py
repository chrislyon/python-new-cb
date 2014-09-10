
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

import shlex

class Processor():

    def __init__(self):
        self.exec_ptr = 0
        self.prog = []

    def load(self, instructions ):
        """ Chargement du prog """
        self.prog = instructions

    def check(self):
        """
        """
        for i in self.prog:
            print "%-50s : %s" % (i, shlex.split(i))

    def run(self):
        """
            Run = execution du programme est sorti
            sur certain cas de figure
        """
        RUNNING = True
        print "DEBUT DU PROG"
        while RUNNING:
            instr = self.prog[self.exec_ptr]
            if instr.startswith("PRINT"):
                d = instr.split(' ')
                print d[1:]
            elif instr.startswith("END"):
                RUNNING = False
            self.exec_ptr += 1
        print "FIN DU PROG"

    def next(self):
        pass

##
## TEST
##
def test():

    P = Processor()

    PRG1 = [
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

    P.load( PRG1 )
    P.check()
    #P.run()
    

if __name__ == '__main__':
    test()
