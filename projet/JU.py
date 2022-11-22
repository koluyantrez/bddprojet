from rel import Relation
from sqliteEnum import SqliteTypes as sType
from expr import Expression

class Union(Expression):
	#Union(relA,relB,newRel) = relA U relB
	
	
	def __init__(self,relA: Relation,relB: Relation,newRel: str)->None:
		
		#Call the parent constructor
		
		# If it's an expression then 
		# we just mention that the sql querry is going
		# to be modified instead of created
		if (isinstance(relA,Expression) or isinstance(relB,Expression)):
			super().__init__(relA.newRel,None,None,True)
			# We initialize the basic attributes: newName, relA, relB  and Relation
			self.__initialisation(relA,relB,self.newRel)
		# If it's a relation then
		# We will just create an sql querry
		elif(isinstance(relA,Relation) or isinstance(relB,Relation)):
			super().__init__(relA,None,None)
			# We initialize the basic attributes: newName, oldArg, newArg and Relation
			self.__initialisation(relA,relB,self.newRel)
			self.querry = self.__createNewQuerry()
		
		#le cas ou aucun des deux n'existent
		if(not(isInDatabase(relA.getName(),relA.getDataBase()) and isInDatabase(relA.getName(),relA.getDataBase()))):
			raise Exception("Your relation is not in database.")
		
		self.relA=relA
		self.relB=relB
        
        
	def __initialisation(self,relA: Relation,relB: Relation,rel: Relation):
		
		if(not(Relation.isInDatabase(relA.getName(),relA.getDataBase()) and Relation.isInDatabase(relA.getName(),relA.getDataBase()))):
			raise Exception("This relation is not in database.")
		
		__checkRelation(relA,relB)
		__checkAttributes(relA,relB)

		self.relA = relA
		self.relB = relB
	
		#We create the new name
		self.newName = "UnionWith_" + relA.getName() + "And" + relB.getName()
	
		# We create the relation/ table
		self.newRel = self.__createRelation()
           
	def __checkRelation(self,relA,relB):
		if(len(relA.getArgs())!=len(relB.getArgs())):
			raise Exception("The number of attribute from the relations is different")
		for a in relA.getArgs():
			for b in relB.getArgs():
				if(a!=b):
					raise Exception("Attribute is differente, you cannot do an union.")
	
	def __checkAttributes(relA,relB)->dict:
		
	
	def __getArgs(self):
		newArgs={}
		for a in self.relA.getArgs():
			newArgs[a] = self.relB.getArgs()[b]
		
		return newArgs
	
	def __createRelation(self) -> Relation:
		# We get the new arguments of the new Relation
		newArgs = self.__getNewArgs()
		# We create the rel with those new Args
		R = Relation(self.relB.getDataBase(),self.newName,newArgs)
	 
		# We re add all the tuple from the other relation
		nbOfTupA = self.relA.getNbOfTuple()
		nbOfTupB = self.relB.getNbOfTuple()
		cursor = self.relB.getCursor().execute("SELECT * FROM " + self.relB.getName())	#???
		tup = cursor.fetchall()
		self.relB.killCursor()
		for i in range(nbOfTupA+nbOfTupB):
			R.addTuple(tup[i])

		return R

	def __createNewQuerry(self)->str:
		return "SELECT * FROM "+self.relA.getName()+" UNION SELECT * FROM "+self.relB.getName()
