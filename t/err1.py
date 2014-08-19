import sys, traceback

class Err(Exception):
	def __init__(self, raison="<vide>", nolig=0):
		self.raison = raison
		self.nolig = nolig

	def __str__(self):
		return "%s : %s " % (self.nolig, self.raison)




	
try:
	raise Err("SYNTAXE")
except:
	print("Exception in user code:")
	print("-"*60)
	traceback.print_exc(file=sys.stdout)
	print("-"*60)
