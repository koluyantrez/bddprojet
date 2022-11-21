from rel import Relation
from sqliteEnum import SqliteTypes as sType
from expr import Expression

class Union(Expression):
    #Union(relA,relB,newRel) = ???
    
    
    def __init__(self,relA: Relation,relB: Relation,newRel: str)->None:
		
		#Call the parent constructor

        # If it's an expression then 
        # we just mention that the sql querry is going
        # to be modified instead of created
        if (isinstance(relA,Expression) or isinstance(relB,Expression)):
            super().__init__(relA.newRel,None,None,True)
            # We initialize the basic attributes: newName, relA, relB  and Relation
            self.__initialisation(oldArgu,newArgu,self.oldRel)
        # If it's a relation then
        # We will just create an sql querry
        elif(isinstance(relA,Relation) or isinstance(relB,Relation)):
            super().__init__(relA,None,None)
            # We initialize the basic attributes: newName, oldArg, newArg and Relation
            self.__initialisation(oldArgu,newArgu,rel)
            self.querry = self.__createNewQuerry()
		
        #le cas ou aucun des deux n'existent
        if(not(isInDatabase(relA.getName(),relA.getDataBase()) and isInDatabase(relA.getName(),relA.getDataBase())))
			raise Exception("Your relation is not in database.")
        
        self.relA=relA
        self.relB=relB
        
        
        def __initialisation(self,relA,relB,rel : Relation):
            #self.__methodePourCHeckerLaPresenceDesReltions
            self.oldArg = oldArgu
            self.newArg = newArgu

            #We create the new name
            self.newName = "UnionWith_" + oldArgu + "And" + newArgu + "_From" + rel.getName()

            # We create the relation/ table
            self.newRel = self.__createRelation()
            
		def __checkRelation(self,relA,relB):		#à vérifier
			if(len(relA.getArgs())!=len(relB.getArgs())):
				raise Exception("The number of attribute from the relations is different")
