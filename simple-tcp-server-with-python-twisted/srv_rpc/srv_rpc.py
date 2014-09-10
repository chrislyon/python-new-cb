from txjsonrpc.web import jsonrpc
from twisted.web import server
from twisted.internet import reactor

class Math(jsonrpc.JSONRPC):
    """
    An example object to be published.
    """
    def jsonrpc_add(self, a, b):
        """
        Return sum of arguments.
        """
        return a + b

reactor.listenTCP(7080, server.Site(Math()))
reactor.run()
