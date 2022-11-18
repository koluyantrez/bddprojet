from rel import Relation
from sqliteEnum import SqliteTypes as sType
from expr import Expression


class Select(Expression):
	#Select(Condition("Attribut","Valeur",Relation))
	#Show all arguments
	# exemple : Select(Neq(’Country’, 'Mali’),'CC') = S_Country="Mali" (CC)
	
	def __init__(self, ope: Expression)-> None:
		super().__init__(rel,None,None)
		self.ope=ope
		
		self.newName = self.ope.toString()
	
	def __checkOpe(self,ope):
		if (len(ope) == 0):
			raise Exception("The length of operation must be greater than 0")
	
	def __checkArgEq(self,key,rel):
		if(not self.rel.args.__contains__(key)):
			raise Exception("The relation "+self.rel.name+" don't have key called \""+key+"\"")
	
	def __checkArgCompare(self,key,val):
		if(not self.rel.args.__contains__(key)):
			raise Exception("The relation "+self.rel.name+" don't have key called \""+key+"\"")
		try:
			float(val)


class Eq(Select):
	#Eq("Attribut","Value",rel)
	def __init__(self,key: str,val: str,rel: Relation)->None:
		
		self.__checkArgSel(key)
		
		self.rel=rel
		self.key=key
		self.val=val
	
	def __str__(self):  
		return "SELECT * FROM " + self.rel.name+" WHERE "+self.key+" == "+self.val
	
	def __getNewArgs(self) -> dict:
		newArgs = {}
		
		try:
			for k in self.rel.args:
				if (k == self.key and float(self.rel.argrs[k]) == float(self.val):
					newArgs[k] = self.oldRel.args[k]
			return newArgs
			
		except:
			for k in self.rel.args:
				if (k == self.key and self.rel.argrs[k] == self.val:
					newArgs[k] = self.oldRel.args[k]
			return newArgs
		

	def __createRelation(self) -> Relation:
		newArgs = self.__getNewArgs()
		# Create the rel
		R = Relation(self.rel.dataBase,self.newName,newArgs)
		# We need to add all tuples to the new rel
		nbOfTup = self.rel.getNbOfTuple()
		self.rel.c.execute()
		
		for i in range(nbOfTup):
			R.addTuple(self.rel.c.fetchone(str(self)))	#paramète dans str?
		
		return R
		

class Neq(Select):
	#Neq("Attribut","Value",rel)
	def __init__(self,key: str,val: str,rel: Relation)->None:
		
		self.__checkArgSel(key)
		
		self.rel=rel
		self.key=key
		self.val=val
	
	def __str__(self): 
			return "SELECT * FROM " + self.rel.name+" WHERE "+self.key+" <> "+self.val

	
	def __getNewArgs(self) -> dict:
		newArgs = {}
		
		try:
			for k in self.rel.args:
				if (k == self.key and float(self.rel.argrs[k]) == float(self.val):
					newArgs[k] = self.oldRel.args[k]
			return newArgs
			
		except:
			for k in self.rel.args:
				if (k == self.key and self.rel.argrs[k] == self.val:
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
			R.addTuple(self.rel.c.fetchone(str(self)))	#paramète dans str?
		
		return R
