class A(object):
    TOTO = 1
    TITI = 2

    def pr(self):
        print "pr_A"
        print "Self.TOTO = ", self.TOTO
        print "A.TITI = ", A.TITI

class B(A):
    TOTO=4
    def pr(self):
        print "pr_B"
        print "Self.TOTO = ", self.TOTO
        print "A.TITI = ", A.TITI
        print "B.TOTO = ", B.TOTO
        print "B.TITI = ", B.TITI


if __name__ == '__main__':
    a = A()
    b = B()
    a.pr()
    b.pr()

