from rel import Relation
from sqliteEnum import SqliteTypes as sType

# Every other class in this file is a child of the expression class stocking :
# The new Relation
# The old Relation
# The SQL querry created
class Expression():
    def __init__(self,oldRel : Relation, newRel : Relation, querry:str, isOneExp = True) -> None:
        self.oldRel     = oldRel
        self.newRel     = newRel
        self.querry     = querry
        self.isOneExp   = isOneExp
    
    def __str__(self) -> str:
        return self.querry

class Project(Expression):
    def __init__(self,args : tuple, rel) -> None:

        #Calls the parent constructor
        if(isinstance(rel,Expression)):
            print("isExpression")
            super().__init__(rel.newRel,None,None,False)
        elif(isinstance(rel,Relation)):
            super().__init__(rel,None,None)
        else:
            raise Exception("The relation argument must be an SPJRUD expression or a relation")
        
        

        self.args = args
        # We check the arguments given
        argsDic = self.__checkArgs()
        # The name will be Unique for each projection
        argStr = self.__argsToString().replace(",","")
            
        self.name = "ProjectOf_" + argStr + "_From" + self.oldRel.name
        
        self.querry = self.__createQuerry()
        
        
        # We create a new table in the database of the old one
        self.newRel = Relation(self.oldRel.dataBase,self.name,argsDic)
        # We still need to fill that table with the correct values
        self.__addTuples()


    



    
    # Raises an error if something is wrong with the tuple given
    def __checkArgs(self):
        

        if len(self.args) == 0:
            raise Exception("The size of the tuple must be at least : 1")
        elif len(self.args) > len(self.oldRel.args):
            raise Exception("The size of the tuple must be smaller or equal than the number of the relation given:\n " 
                            + "Gave a tuple with " + str(len(self.args)) + " elements.\n" 
                            + " But the relation " + self.oldRel.name + " has " + str(len(self.oldRel.args)) + " arguments")
        relArgs = self.oldRel.args
        
        argDic = {}
        for arg in self.args:
            # Vérifie que l'argument appartient au tableau
            if (not relArgs.__contains__(arg)):
                raise Exception("The relation " + self.oldRel.name + " does not contain any argument called: " + arg)
            else:
                # Copie les arguments et leurs types
                argDic[arg] = relArgs[arg]
        return argDic
            
    def __argsToString(self)-> str:
        argStr = ""
        for arg in self.args:
            argStr += arg + ","
        return argStr[0:len(argStr)-1]

    def __createQuerry(self)-> str:
        
        # SELECT ARG1,ARG2,...,ARGn FROM RELNAME;
        argStr = self.__argsToString()

        querry = "SELECT " + argStr + " FROM " + self.oldRel.name
        return querry

    def __addTuples(self):
        
        self.oldRel.c.execute(self.querry)
        
        for tup in self.oldRel.c.fetchall():
            
            try:
                self.newRel.addTuple(tup)
            except Exception as e:
                pass

        
class Rename(Expression):
    # Rename("OldArg", "NewArg", Rel)
    # = Rename in Rel, OldArg to NewArg


    # UTILISER DES ALIAS POUR DES COLONNES MDRRRRRR

    def __init__(self, oldArgu: str, newArgu: str, rel: Relation) -> None:
        #Calls the parent constructor
        if(isinstance(rel,Expression)):
            print("isExpression")
            super().__init__(rel.newRel,None,None,False)
        elif(isinstance(rel,Relation)):
            super().__init__(rel,None,None)
        else:
            raise Exception("The relation argument must be an SPJRUD expression or a relation")
        
        # First we check if the old argument exist in the old rel
        self.__checkOldArg(oldArgu,newArgu)
        self.oldArgu = oldArgu
        self.newArgu = newArgu
        
        # We can create the name of the new relation
        self.newName = "RenameOf_" + oldArgu + "To" + newArgu + "_From" + rel.name
        
        

        # In the dic of Args from the oldRelation we change the old name to the new one
        self.newRel = self.__createRelation()
        # ex: 
        # ALTER TABLE STOCK RENAME COLUMN Qty TO Quantity

        self.querry = self.__createQuerry()

    def __checkOldArg(self,oldArg,newArg):
        if (len(oldArg) == 0 or len(newArg) == 0):
            raise Exception("The length of oldArt and newArg must be greater than 0")
        if ( not self.oldRel.args.__contains__(oldArg)):
            raise Exception("The relation " + self.oldRel.name + " doesn't contain any argument called: " + oldArg)
        if (oldArg == newArg):
            raise Exception("It is useless to rename an argument to the same name")
        if (self.oldRel.args.__contains__(newArg)):
            raise Exception("The relation " + self.oldRel.name + " already has another argument called: " + newArg)

    # Get the dict of new Args for the new rel
    # Ex: change Qty to Quantity in {'W': <SqliteTypes.TEXT: 'text'>, 'Pro': <SqliteTypes.TEXT: 'text'>, 'Color': <SqliteTypes.TEXT: 'text'>, 'Qty': <SqliteTypes.INTEGER: 'integer'>}
    # new: {'W': <SqliteTypes.TEXT: 'text'>, 'Pro': <SqliteTypes.TEXT: 'text'>, 'Color': <SqliteTypes.TEXT: 'text'>, 'Quantity': <SqliteTypes.INTEGER: 'integer'>}
    def __getNewArgs(self) -> dict:
        newArgs = {}

        for key in self.oldRel.args:
            if (not key == self.oldArgu):
                newArgs[key] = self.oldRel.args[key]
            else:
                newArgs[self.newArgu] = self.oldRel.args[key]
        
        return newArgs

    def __createRelation(self) -> Relation:
        newArgs = self.__getNewArgs()
        # Create the rel
        R = Relation(self.oldRel.dataBase,self.newName,newArgs)
        # We need to add all tuples to the new rel
        nbOfTup = self.oldRel.getNbOfTuple()
        self.oldRel.c.execute("SELECT * FROM " + self.oldRel.name)
        
        for i in range(nbOfTup):
            R.addTuple(self.oldRel.c.fetchone())

        return R

    def __createQuerry(self) -> str:
        # Ex : 
        return "HI"
        

    # RENAME(PROJECT)
    # SELECT W ware, PRODUCT FROM STOCK;

    # PROJECT(ware, RENAME)
    # SELECT W ware, (tous les arg de stock) FROM STOCK
    
    # SELECT W ware FROM STOCK