# CC-BY-NC-3.0

import json
from twisted.protocols.basic import LineReceiver
from twisted.internet import defer

class Request(object):
	def __init__(self,protocol,method):
		self.protocol = protocol
		self.method = method
	def __call__(self,*args,**kwargs):
		return self.protocol.callRemote(self.method,*args,**kwargs)
	def notify(self,*args,**kwargs):
		return self.protocol.notifyRemote(self.method,*args,**kwargs)

class Response(Exception):
	def __init__(self,value=None):
		self.value = value
	def format(self,ctx):
		return {'jsonrpc':'2.0','response':self.value,'id':ctx}

class ProtocolException(Exception):
	def __init__(self,code,message,data=None):
		self.code = int(code)
		self.message = unicode(message)
		self.data = data
	def __repr__(self):
		return 'ProtocolException(%d,%s,%s)'%(self.code,repr(self.message),repr(self.data))
	def format(self,ctx=None):
		e = {'code':self.code,'message':self.message}
		if self.data is not None:
			e['data'] = self.data
		return {'jsonrpc':'2.0','error':e,'id':ctx}
	@staticmethod
	def stringify(self,ex):
		return json.dumps({'jsonrpc':'2.0','error':{'code':-32000,'message':ex.__class__.__name__,'data':str(ex)},'id':None},separators=(',',':'))
class ParseError(ProtocolException):
	def __init__(self,message='Parse error.',data=None):
		ProtocolException.__init__(self,-32700,message,data)
class InvalidRequest(ProtocolException):
	def __init__(self,message='Invalid request.',data=None):
		ProtocolException.__init__(self,-32600,message,data)
class MethodNotFound(ProtocolException):
	def __init__(self,message='Method not found.',data=None):
		ProtocolException.__init__(self,-32601,message,data)
class InvalidParams(ProtocolException):
	def __init__(self,message='Invalid parameters.',data=None):
		ProtocolException.__init__(self,-32602,message,data)
class InternalError(ProtocolException):
	def __init__(self,message='Internal error.',data=None):
		ProtocolException.__init__(self,-32603,message,data)
class PythonError(ProtocolException):
	def __init__(self,ex):
		ProtocolException.__init__(self,-32000,ex.__class__.__name__)

class Protocol(LineReceiver):
	delimiter = '\n'
	def __init__(self):
		self._buffer = None
		self._request = {}
		self._deferred = {}
	def lineReceived(self,line):
		try:
			try:
				data = json.loads(line)
			except ValueError:
				data = (None,)
				raise ParseError()
			res = defer.maybeDeferred(self.jsonReceived,data)
			res.addCallback(self.sendJson)
		except ProtocolException,ex:
			self.sendJson(ex.format(None))
	def jsonReceived(self,data):
		if isinstance(data,dict):
			data_id = None
			try:
				if data.get('jsonrpc',None) != '2.0':
					raise InvalidRequest()
				if 'method' in data:
					if 'id' in data:
						data_id = data['id']
						if not (isinstance(data_id,basestring) or isinstance(data_id,float) or isinstance(data_id,int) or data_id is None):
							data_id = None
							raise InvalidRequest()
					else:
						data_id = False
					data_method = data['method']
					if not isinstance(data_method,basestring):
						raise InvalidRequest()
					try:
						fn = getattr(self,'jsonrpc_'+data_method)
					except AttributeError:
						raise MethodNotFound()
					if 'params' in data:
						data_params = data['params']
						if isinstance(data_params,list):
							try:
								response = fn(*data_params)
							except Error,ex:
								raise PythonError(ex)
						elif isinstance(data_params,dict):
							try:
								response = fn(**data_params)
							except Error,ex:
								raise PythonError(ex)
						else:
							raise InvalidRequest()
					else:
						try:
							response = fn()
						except Error,ex:
							raise PythonError(ex)
					if data_id is not False:
						raise Response(response)
				elif 'response' in data:
					if 'error' in data or 'id' not in data:
						raise InvalidRequest()
					data_id = data['id']
					try:
						deferred = self._deferred[data_id]
						del self._deferred[data_id]
					except KeyError:
						return
					deferred.callback(data['response'])
				elif 'error' in data:
					if 'response' in data or 'id' not in data:
						raise InvalidRequest()
					data_id = data['id']
					try:
						deferred = self._deferred[data_id]
						del self._deferred[data_id]
					except KeyError:
						return
					deferred.errback(data['error'])
			except (Response,ProtocolException),ex:
				if data_id is not False:
					return ex.format(data_id)
		elif isinstance(data,list):
			@defer.inlineCallbacks
			def runall():
				responses = []
				for request in data:
					if isinstance(request,dict):
						response = yield defer.maybeDeferred(self.jsonReceived,request)
						if response is not None:
							responses.append(response)
				defer.returnValue(responses)
			return runall()
	def sendJson(self,data):
		if isinstance(data,dict) or isinstance(data,list):
			self.sendLine(json.dumps(data,separators=(',',':')))
	def callRemote(self,_method,*args,**kwargs):
		largs = len(args)
		lkwargs = len(kwargs)
		if largs > 0 and lkwargs > 0:
			raise TypeError('cannot use both positional and named parameters')
		elif largs > 0:
			params = args
		elif lkwargs > 0:
			params = kwargs
		else:
			params = None
		d = defer.Deferred()
		try:
			ctx = max(self._deferred)+1
		except ValueError:
			ctx = 0
		o = {'jsonrpc':'2.0','method':_method,'id':ctx}
		if params is not None:
			o['params'] = params
		self._deferred[ctx] = d
		if isinstance(self._buffer,list):
			self._buffer.append(o)
		else:
			self.sendJson(o)
		return d
	def notifyRemote(self,_method,*args,**kwargs):
		largs = len(args)
		lkwargs = len(kwargs)
		if largs > 0 and lkwargs > 0:
			raise TypeError('cannot use both positional and named parameters')
		elif largs > 0:
			params = args
		elif lkwargs > 0:
			params = kwargs
		else:
			params = None
		o = {'jsonrpc':'2.0','method':_method}
		if params is not None:
			o['params'] = params
		if isinstance(self._buffer,list):
			self._buffer.append(o)
		else:
			self.sendJson(o)
		return self
	def beginQueue(self):
		self.endQueue()
		self._buffer = []
		return self
	def endQueue(self):
		if isinstance(self._buffer,list):
			self.sendJson(self._buffer)
		self._buffer = None
		return self
	def __getattr__(self,key):
		if key.startswith('_'):
			raise AttributeError('%s instance has no attribute \'%s\''%(self.__class__.__name__,key))
		try:
			return self._request[key]
		except KeyError:
			self._request[key] = Request(self,key)
			return self._request[key]

if __name__ == '__main__':
	from twisted.internet.protocol import ServerFactory, ClientFactory
	from twisted.internet import reactor
	class EchoServer(ServerFactory):
		class protocol(Protocol):
			def jsonrpc_echo(self,*args):
				largs = len(args)
				if largs == 1:
					print self.factory.__class__.__name__,'receive:',args[0]
					return args[0]
				elif largs > 1:
					print self.factory.__class__.__name__,'receive:',args
					return args
			def jsonrpc_bounce(self,*args):
				print self.factory.__class__.__name__,'bounce'
				self.notifyRemote('echo',*args)
				largs = len(args)
				if largs == 1:
					return args[0]
				elif largs > 1:
					return args
	class EchoClient(ClientFactory):
		class protocol(Protocol):
			end = 'Goodbye!'
			def connectionMade(self):
				@defer.inlineCallbacks
				def runall():
					res = yield self.callRemote('echo','Hello, world!')
					print self.factory.__class__.__name__,'receive:',res
					res = yield self.echo('What a fine day it is.')
					print self.factory.__class__.__name__,'receive:',res
					res = yield self.echo('Who?','What?','When?','Where?','Why?','How?')
					print self.factory.__class__.__name__,'receive:',res
					res = yield self.bounce('Call me back!')
					defer.returnValue(None)
				def callback(res):
					self.beginQueue().bounce.notify('Bounce!').bounce.notify(self.end).endQueue()
				runall().addCallback(callback)
			def connectionLost(self,reason):
				print 'connection lost (protocol)'
			def jsonrpc_echo(self,*args):
				largs = len(args)
				if largs == 1:
					print self.factory.__class__.__name__,'receive:',args[0]
					if args[0] == self.end:
						self.transport.loseConnection()
					return args[0]
				elif largs > 1:
					print self.factory.__class__.__name__,'receive:',args
					return args
		def clientConnectionFailed(self,connector,reason):
			print 'connection failed:',reason.getErrorMessage()
			reactor.stop()
		def clientConnectionLost(self,connector,reason):
			print 'connection lost:',reason.getErrorMessage()
			reactor.stop()
	reactor.listenTCP(8000,EchoServer())
	reactor.connectTCP('localhost',8000,EchoClient())
	reactor.run()
