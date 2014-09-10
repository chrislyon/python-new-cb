#install_twisted_rector must be called before importing the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()


#A simple Client that send messages to the echo server
from twisted.internet import reactor, protocol, defer
from twisted.protocols.basic import LineReceiver

import pdb

## C'est mieux les lignes
#class EchoClient(protocol.Protocol):
class EchoClient(LineReceiver):

    delimiter = '\r\n'      ## delimiter pour sendLine
    d = None                ## deferred

    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def pr_hex(self, data):
        # Pour debug
        for l in data:
            print "===== %s " % d
            for c in d:
                print hex(ord(c)),
            print

    ## lineReceived appeller par deferred
    def lineReceived(self, line):
        if line:
            if self.d is None:
                return
            d, self.d = self.d, None
            d.callback(line)

    ## --------------------------------------------------
    ## ON reuni ici toutes les commandes pour le serveur
    ## --------------------------------------------------
    def command(self, cmd):
        if cmd == "REQ LIST MACH":
            M = Message()
            M.msg_status = Message.OK
            M.msg_info = "REQ LIST"
            M.msg_data = "MACHINE"
            self.sendLine(str(M.to_json())+self.delimiter)
        elif cmd == "REQ LIST OPER":
            M = Message()
            M.msg_status = Message.OK
            M.msg_info = "REQ LIST"
            M.msg_data = "OPERATOR"
            self.sendLine(str(M.to_json())+self.delimiter)
        else:
            self.sendLine(str(cmd))
        self.d = defer.Deferred()
        return self.d

    ## Lancement de la commande
    @defer.inlineCallbacks
    def do_request(self, cmd):
        print "do_request : %s " % cmd
        yield self.command(cmd)

class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient
    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        self.app.print_message("connection lost")

    def clientConnectionFailed(self, conn, reason):
        self.app.print_message("connection failed")


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button

from message import Message

# A simple kivy App, with a textbox to enter messages, and
# a large label to display all the messages received from
# the server
class TwistedClientApp(App):
    connection = None

    def build(self):
        root = self.setup_gui()
        self.connect_to_server()
        return root

    def setup_gui(self):
        #HautPage
        self.haut = BoxLayout(orientation='vertical', padding=1, spacing=1)
        self.haut.size_hint_y = 0.2
        self.entete = Label(text="<TITRE>")
        self.entete.font_size = 32

        #Contenu
        self.contenu = AnchorLayout(anchor_x="center", anchor_y="center")
        self.contenu.size_hint_y = 0.6

        self.g = GridLayout(cols=2)
        self.g.row_force_default = True
        self.g.row_default_height = 45
        self.g.padding = 4
        self.g.spacing = 4

        ## Machine
        self.L_machine = Label(text = "Machine :")
        self.L_machine.size_hint_x = .30
        self.L_machine.size_hint_y = None
        self.L_machine.height = 10
        self.Z_machine = Spinner()
        self.Z_machine.text = "<MACHINE>"
        self.Z_machine.values = [ "MACH1", "MACH2", "MACH3" ]
        self.g.add_widget( self.L_machine )
        self.g.add_widget( self.Z_machine )
        ## Operateur
        self.L_operator = Label(text = "Operateur :")
        self.L_operator.size_hint_x = .30
        self.L_operator.size_hint_y = None
        self.L_operator.height = 10
        self.Z_operator = Spinner()
        self.Z_operator.text = "<OPERATEUR>"
        self.Z_operator.values = [ "OP1", "OP2", "OP2" ]
        self.g.add_widget( self.L_operator )
        self.g.add_widget( self.Z_operator )
        ## OF
        self.L_of = Label(text = "Ordre de Fab :")
        self.L_of.size_hint_x = .30
        self.L_of.size_hint_y = None
        self.L_of.height = 10
        self.Z_of = TextInput()
        self.Z_of.text = ""
        self.g.add_widget( self.L_of )
        self.g.add_widget( self.Z_of )
        ## Operation
        self.L_oper = Label(text = "Operation :")
        self.L_oper.size_hint_x = .30
        self.L_oper.size_hint_y = None
        self.L_oper.height = 10
        self.Z_oper = TextInput()
        self.Z_oper.text = ""
        self.g.add_widget( self.L_oper )
        self.g.add_widget( self.Z_oper )

        self.contenu.add_widget(self.g)

        #Base de page (Status)
        self.bas = BoxLayout(orientation='horizontal', padding=1, spacing=1)
        self.bas.size_hint_y = 0.1

        self.status = Label( text = "status : " )
        self.status.font_size = 20
        self.status.multiline = False

        #Base de page (Bouton)
        self.bas = BoxLayout(orientation='horizontal', padding=1, spacing=1)
        self.bas.size_hint_y = 0.1
        ## Bouton ENVOI
        self.B_ENVOI = Button()
        self.B_ENVOI.text = "ENVOI"
        self.B_ENVOI.bind(on_press=self.B_pressed)
        self.bas.add_widget( self.B_ENVOI )
        ## Bouton INIT
        self.B_INIT = Button()
        self.B_INIT.text = "INIT"
        self.B_INIT.bind(on_press=self.B_pressed)
        self.bas.add_widget( self.B_INIT )
        ## Bouton Help
        self.B_Help = Button()
        self.B_Help.text = "Help"
        self.B_Help.bind(on_press=self.B_pressed)
        self.bas.add_widget( self.B_Help )
        ## Bouton QUIT
        self.B_QUIT = Button()
        self.B_QUIT.text = "QUIT"
        self.B_QUIT.bind(on_press=self.B_pressed)
        self.bas.add_widget( self.B_QUIT )

        ## On agrege le tout
        self.layout = BoxLayout(orientation='vertical')
        self.layout.padding=5
        self.layout.spacing=5
        self.layout.add_widget(self.haut)
        self.layout.add_widget(self.contenu)
        self.layout.add_widget(self.status)
        self.layout.add_widget(self.bas)
        return self.layout

    def init_data(self):
        # On recupere la liste des operateurs
        # et des machines
        data = self.send_request('REQ LIST MACH')
        for l in data:
            print "l=%s " % l

    def B_pressed(self, instance):
        print "Bouton pressed %s" % instance.text
        if instance.text == "ENVOI":
            print " MACHINE   = %s" % self.Z_machine.text
            print " OPERATEUR = %s" % self.Z_operator.text
            print " ORDRE FAB = %s" % self.Z_of.text
            print " OPERATION = %s" % self.Z_oper.text
        elif instance.text == "INIT":
            self.init_data()
        elif instance.text == "Help":
            pass
        elif instance.text == "QUIT":
            self.stop()
        else:
            print "BOUTON INCONNU"


    def connect_to_server(self):
        #reactor.connectTCP('localhost', 8000, EchoFactory(self))
        reactor.connectTCP('localhost', 1202, EchoFactory(self))
        #reactor.connectTCP('vm-syssrc01-bron.groupe-sra.lan', 1202, EchoFactory(self))

    def on_connection(self, connection):
        self.print_message("connected succesfully!")
        self.connection = connection

    def send_request(self, req):
        #pdb.set_trace()
        return self.connection.protocol.do_request(req)
            

    def send_message(self, *args):
        msg = self.textbox.text
        if msg and self.connection:
            self.connection.write(str(self.textbox.text)+'\r\n')
            self.textbox.text = ""

    def print_message(self, msg):
        self.status.text += msg + "\n"


if __name__ == '__main__':
    TwistedClientApp().run()
