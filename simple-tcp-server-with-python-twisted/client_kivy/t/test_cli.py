from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic

from message import Message

class Client(basic.LineReceiver):

    delimiter = '\r\n'
    d = None

    # Internal
    def lineReceived(self, data):
        if data:
            print "r=[%s]" % data
            if self.d is None:
                print "d is none"
                return 
            d, self.d = self.d, None
            d.callback(data)
        
    def command(self, cmd):
        print "Commande : %s " % cmd
        if cmd == "MACH":
            M = Message()
            M.msg_status = Message.OK
            M.msg_info = "REQ LIST"
            M.msg_data = "MACHINE"
            self.sendLine(str(M.to_json())+self.delimiter)
        elif cmd == "OPER":
            M = Message()
            M.msg_status = Message.OK
            M.msg_info = "REQ LIST"
            M.msg_data = "OPERATOR"
            self.sendLine(str(M.to_json())+self.delimiter)
        else:
            self.sendLine(str(cmd))
        self.d = defer.Deferred()
        return self.d

    # public API
    def get_MACHINE(self): 
        def get_Message(msg):
            print 'get_Message :', msg
            return msg
        return self.command("MACH").addCallback(get_Message)

    def get_OPER(self): 
        return self.command("OPER")

    # User code, this is actually the main()
    @defer.inlineCallbacks
    def connectionMade(self):
        ## Il faut virer le message de bienvenu
        #yield self.command("")
        #yield self.command("")
        yield self.command("")
        print "=== MACHINE === "
        print (yield self.get_MACHINE())
        print "=== OPER === "
        print (yield self.get_OPER())
        print "=== PING === "
        r = self.command("PING")
        print (yield r)
        r = self.command("PING")
        print (yield r)
        reactor.stop()


factory = protocol.ClientFactory()
factory.protocol = Client
reactor.connectTCP("localhost", 1202, factory)
reactor.run()
