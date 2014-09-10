from twisted.internet import defer

def got_results(res):
    print "We got ", res

print "One deferred"
d1 = defer.Deferred()
d = defer.DeferredList([d1])

print "adding callback"
d.addCallback(got_results)

print "Firing d1"
d1.callback('d1 result')
