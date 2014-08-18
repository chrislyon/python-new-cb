class OrderedEnum(Enum):
     def __ge__(self, other):
         if self.__class__ is other.__class__:
             return self.value >= other.value
         return NotImplemented
     def __gt__(self, other):
         if self.__class__ is other.__class__:
             return self.value > other.value
         return NotImplemented
     def __le__(self, other):
         if self.__class__ is other.__class__:
             return self.value <= other.value
         return NotImplemented
     def __lt__(self, other):
         if self.__class__ is other.__class__:
             return self.value < other.value
         return NotImplemented

class OE(OrderedEnum):
	RAZ = 1
	DOSSIER = 2
	OPERATION = 3
	BOBINE = 4
	MAJ = 5


def test():
	A = OE()

if __name__ == '__main__':
	test()
