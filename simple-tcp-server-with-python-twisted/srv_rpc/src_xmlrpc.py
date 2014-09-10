from twisted.web import xmlrpc, server

class Example(xmlrpc.XMLRPC):
    """An example object to be published."""
    
    def xmlrpc_echo(self, x):
        """Return all passed args."""
        return x
    
    def xmlrpc_add(self, a, b):
        """Return sum of arguments."""
        return a + b


def main():
    from twisted.internet.app import Application
    app = Application("xmlrpc")
    r = Example()
    app.listenTCP(7080, server.Site(r))
    return app

application = main()

if __name__ == '__main__':
    application.run(save=0)
