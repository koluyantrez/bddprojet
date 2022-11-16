from rel import Relation
from sqliteEnum import SqliteTypes as sType
from expr import Expression


class Select(Expression):
	#Select(Condition,  Rel)
	#Show all arguments
	# exemple : Select(Eq(’Country’, Cst(’Mali’)), Rel(’CC’)) = S_Country="Mali" (CC)
	
	def __init__(self, ope: Expression, rel: Relation) -> None:
		super().__init__(rel,None,None)
		self.ope=ope
		
		self.newName = "selectAllFrom_" + rel.name+"where"+self.ope 
	
	
	def __checkOpe(self,ope):
		if (len(ope) == 0):
			raise Exception("The length of operation must be greater than 0")
	
	def __checkArgSel(self,key):
		if(not self.rel.args.__contains__(key)):
			raise Exception("The relation "+self.rel.name+" don't have key called \""+key+"\"")
	
class Equals(Select):
	#Equals("Attribut","Value")
	def __init__(self,key: str,val: str,rel: Relation)->None:
		
		self.__checkArgSel(key)
		
		self.rel=super(rel)	#doubt I want the relation from Select
		self.key=key
		self.val=val
		
	
	def __getNewArgs(self) -> dict:
		newArgs = {}

		for k in self.rel.args:
			if (k == self.key and self.rel.argrs[k] == self.val):
				newArgs[k] = self.oldRel.args[k]

		return newArgs

	def __createRelation(self) -> Relation:
		newArgs = self.__getNewArgs()
		# Create the rel
		R = Relation(self.rel.dataBase,self.newName,newArgs)
		# We need to add all tuples to the new rel
		nbOfTup = self.rel.getNbOfTuple()
		self.rel.c.execute("SELECT * FROM " + self.rel.name+"WHERE ...")
		
		for i in range(nbOfTup):
			R.addTuple(self.rel.c.fetchone())
		
		return R
        
        
        


'''
	def __eq(self,key,target)->str:		#equals
		
	def __ne(self,key,arg)->str:		#not equals
		
	def __ge(self)->str:		#greater than or equals
		
	def __gt(self)->str:		#greater than
		
	def __le(self)->str:		#less than or equals
		
	def __lt(self)->str:		#less than
		'''
	
