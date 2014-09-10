
from UserDict import UserDict
from Session import *

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
        #s = Session()
        s = Session_JSON()
        s.no = Sessions.nb
        s.name = "Session %s" % s.no
        s.client = self.create_key(New_Instance.transport.client)
        s.session = New_Instance
        self[s.client] = s
        ## Prevoir ici un start pour la session

    def remove_session(self, s):
        """ Retrait de session """
        k = self.create_key(s.transport.client)
        del self[k]

    def all_session(self):
        """ retourne les sessions pour SHUTDOWN """
        return [ x.session for x in self.values() ]

    def EXIT(self, instance):
        cle = self.create_key(instance.transport.client)
        return self[cle].EXIT

    def resultat(self, instance):
        cle = self.create_key(instance.transport.client)
        return self[cle].resultat()

    def prompt(self, instance):
        cle = self.create_key(instance.transport.client)
        return self[cle].prompt()

    def error(self, instance):
        cle = self.create_key(instance.transport.client)
        return self[cle].error()

    ## On envoie la reponse
    def set_reponse(self, instance, reponse):
        cle = self.create_key(instance.transport.client)
        #return "%s" % self[cle].commande(reponse)
        self[cle].set_reponse(reponse)
        ## on ne retourne rien tout se trouve dans la session

if __name__ == '__main__':
    S = Sessions()
