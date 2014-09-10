import json

class Message():
	OK  = 0
	ERR = 1

	def __init__(self, status=OK, info="", data=[] ):
		self.msg_status = status
		self.msg_info   = info
		self.msg_data   = data
		self.msg_typ	= '%%JSON%%'

	def to_json(self):
		return json.dumps( {  	'msg_typ':		self.msg_typ,
								'msg_status':	self.msg_status, 
								'msg_info':		self.msg_info, 
								'msg_data':		self.msg_data 
							} )
		
	def from_json(self, j):
		self.__dict__ = json.loads(j)

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return "%s : %s : %s" % (self.msg_status, self.msg_info, self.msg_data)

def test():
	M = Message(status=0, info="SALUT", data=[1,2,3] )

	print "M=",M
	print "M=",M.to_json()

	M2 = Message()
	j = M.to_json()
	M2.from_json(j)
	print "M2=",M2
	print "M2=",M2.to_json()

if __name__ == '__main__':
	test()
