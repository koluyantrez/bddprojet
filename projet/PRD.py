from rel import Relation
from sqliteEnum import SqliteTypes as sType
from expr import Expression

class Rename(Expression):
    def __init__(self, oldArgu: str, newArgu: str, rel, name: str) -> None:
        #Call the parent constructor

        # If it's an expression then 
        # we just mention that the sql querry is going
        # to be modified instead of created
        if (isinstance(rel,Expression)):
            super().__init__(rel.newRel,None,None,False)
            # We initialize the basic attributes: newName, oldArg, newArg  and Relation
            self.__initialisation(oldArgu,newArgu,self.oldRel,name)
            self.querry = self.__fusionQuerries(rel)

        # If it's a relation then
        # We will just create an sql querry
        elif(isinstance(rel,Relation)):
            super().__init__(rel,None,None)
            # We initialize the basic attributes: newName, oldArg, newArg and Relation
            self.__initialisation(oldArgu,newArgu,rel,name)
            self.querry = self.__createNewQuerry()

            
    
    def __initialisation(self,oldArgu,newArgu,rel : Relation, name: str):
            self.__checkArgs(oldArgu,newArgu)
            self.oldArg = oldArgu
            self.newArg = newArgu

            #We create the new name
            #self.newName = "RenameOf_" + oldArgu + "To" + newArgu + "_From" + rel.getName()
            self.newName = name
            # We create the relation/ table
            self.newRel = self.__createRelation()
            



    def __checkArgs(self,oldArg,newArg):
        if(len(oldArg) == 0 or len(newArg) == 0):
            raise Exception("The length of oldArt and newArg must be greater than 0")
        if ( not self.oldRel.args.__contains__(oldArg)):
            raise Exception("The relation " + self.oldRel.getName() + " doesn't contain any argument called: " + oldArg)
        if (oldArg == newArg):
            raise Exception("It is useless to rename an argument to the same name")
        if (self.oldRel.args.__contains__(newArg)):
            raise Exception("The relation " + self.oldRel.getName() + " already has another argument called: " + newArg)

    # Get the dict of new Args for the new rel
    # Ex: change Qty to Quantity in {'W': <SqliteTypes.TEXT: 'text'>, 'Pro': <SqliteTypes.TEXT: 'text'>, 'Color': <SqliteTypes.TEXT: 'text'>, 'Qty': <SqliteTypes.INTEGER: 'integer'>}
    # new: {'W': <SqliteTypes.TEXT: 'text'>, 'Pro': <SqliteTypes.TEXT: 'text'>, 'Color': <SqliteTypes.TEXT: 'text'>, 'Quantity': <SqliteTypes.INTEGER: 'integer'>}
    def __getNewArgs(self) -> dict:
        newArgs = {}

        for key in self.oldRel.args:
            if (not key == self.oldArg):
                newArgs[key] = self.oldRel.args[key]
            else:
                newArgs[self.newArg] = self.oldRel.args[key]
        
        return newArgs

    def __createRelation(self) -> Relation:
        # We get the new arguments of the new Relation
        newArgs = self.__getNewArgs()
        # We create the rel with those new Args
        R = Relation(self.oldRel.getDataBase(),self.newName,newArgs)
        
    
        # We re add all the tuple from the other relation
        nbOfTup = self.oldRel.getNbOfTuple()
        cursor = self.oldRel.getCursor().execute("SELECT * FROM " + self.oldRel.getName())
        tup = cursor.fetchall()
        self.oldRel.killCursor()
        for i in range(nbOfTup):
            R.addTuple(tup[i])
        
        
        return R



    def __createNewQuerry(self) -> str:
        # Ex SELECT NrEmp, Dept AS DEPART, Pourcent FROM EMPLOYE: 
        querry = "SELECT "
        # Add to the str all the key but add AS new key when we find the old one
        for key in self.oldRel.getArgs():
            if (key != self.oldArg):
                querry += key + ", "
            else:
                querry += key + " AS " + self.newArg + ", "
        querry = querry[0:len(querry)-2] + " FROM " + self.oldRel.getName()


        return querry 

    def __fusionQuerries(self, expr: Expression):
        # Ex SELECT NrEmp, Dept AS DEPART, Pourcent FROM EMPLOYE: 
        querry = "SELECT "
        # Add to the str all the key but add AS new key when we find the old one
        for key in self.oldRel.getArgs():
            if (key != self.oldArg):
                querry += key + ", "
            else:
                querry += key + " AS " + self.newArg + ", "
        querry = querry[0:len(querry)-2]
        querry += " FROM \n\t" + "(" +expr.querry + ")" + " AS " + self.newRel.getName() 
        return querry

# ___________________________________________________________________________________________________
class Project(Expression):
    def __init__(self,args: tuple, rel, name: str) -> None:
        #Call the parent constructor

        # If it's an expression then 
        # we just mention that the sql querry is going
        # to be modified instead of created
        if (isinstance(rel,Expression)):
            super().__init__(rel.newRel,None,None,False)
            # We initialize the basic attributes: newName, oldArg, newArg  and Relation
            self.__initialisation(args,self.oldRel,name)
            self.querry = self.__fusionQuerries(rel)

        # If it's a relation then
        # We will just create an sql querry
        elif(isinstance(rel,Relation)):
            super().__init__(rel,None,None,name)
            # We initialize the basic attributes: newName, oldArg, newArg and Relation
            self.__initialisation(args,rel,name)
            self.querry = self.__createNewQuerry()

    def __initialisation(self,args: dict, oldRel: Relation, name: str):
        # We check the arguments given
        argsDic = self.__checkArgs(args)
        # We create the new name
        #argStr = self._argsToString(argsDic).replace(",","")
        #name = "ProjectOf_" + argStr + "_From" + self.oldRel.getName()
        # We create the new relation
        self.newRel = Relation(self.oldRel.getDataBase(),name,argsDic)
        # We fill this table
        querry = self.__createNewQuerry()
        # If it's only one expression we can juste create a basic querry
        if(self.isOneExp):
            self.querry = querry


        self._addTupples(querry)

    




    def __createNewQuerry(self) -> str:
        # SELECT ARG1,ARG2,...,ARGn FROM RELNAME;
        argStr = self._argsToString(self.newRel.getArgs())

        querry = "SELECT " + argStr + " FROM " + self.oldRel.getName()
        return querry

    def __fusionQuerries(self, expr: Expression):
        # SELECT ARG1,ARG2,...,ARGn FROM RELNAME;
        argStr = self._argsToString(self.newRel.getArgs())
        # Ex SELECT NrEmp, Dept AS DEPART, Pourcent FROM EMPLOYE: 
        querry = "SELECT " + argStr
        
        querry += " FROM \n\t" + "(" +expr.querry + ")" + " AS " + self.newRel.getName() 
        return querry



    
    # Returns the argument wanted if nothing is wrong
    # Raises an error if something is wrong with given tuple
    def __checkArgs(self,args: dict):
        

        if len(args) == 0:
            raise Exception("The size of the tuple must be at least : 1")
        elif len(args) > len(self.oldRel.args):
            raise Exception("The size of the tuple must be smaller or equal than the number of the relation given:\n " 
                            + "Gave a tuple with " + str(len(args)) + " elements.\n" 
                            + " But the relation " + self.oldRel.getName() + " has " + str(len(self.oldRel.args)) + " arguments")
        relArgs = self.oldRel.args
        
        argDic = {}
        for arg in args:
            # Vérifie que l'argument appartient au tableau
            if (not relArgs.__contains__(arg)):
                raise Exception("The relation " + self.oldRel.getName() + " does not contain any argument called: " + arg)
            else:
                # Copie les arguments et leurs types
                argDic[arg] = relArgs[arg]
        return argDic

#_______________________________________________________________________________________________________________________

class Diff(Expression):
    # Diff(rel1,rel2) = SELECT * FROM REL1 EXCEPT SELECT * FROM REL2
    # i.e Rel1 @minus Rel2
    # Verifier que relation 1 et relation 2 ont les même args
    # 
    def __init__(self,rel1: Relation, rel2: Relation, name : str):
        # 4 cas possibles:
        # rel1 est une expression et rel2 aussi
        if (isinstance(rel1,Expression) and isinstance(rel2,Expression)):
            super().__init__(rel1.newRel,None,None,False)
            self.__initialisation(rel1.newRel,rel2.newRel,name)
            self.querry = self.__fusionQuerries(rel1.querry,rel2.querry,rel1.newRel.getArgs())

        # rel1 est une relation et rel2 une expression
        elif (isinstance(rel1,Relation) and isinstance(rel2,Expression)):
            super().__init__(rel1,None,None,False)
            self.__initialisation(rel1,rel2.newRel,name)
            self.querry = self.__fusionQuerries(rel1.getName(),rel2.querry,rel1.getArgs())

        # rel1 est une expression et rel2 une relation
        elif (isinstance(rel1,Expression) and isinstance(rel2,Relation)):
            super().__init__(rel1.newRel,None,None)
            self.__initialisation(rel1.newRel,rel2,name)
            self.querry = self.__fusionQuerries(rel1.querry,rel2.getName(),rel1.newRel.getArgs())
        
        # rel1 est une relation et rel2 aussi
        elif (isinstance(rel1,Relation) and isinstance(rel2,Relation)):
            super().__init__(rel1,None,None)
            self.__initialisation(rel1,rel2,name)
            # la querry est ajouter dans __initialisation()


    

        
    def __initialisation(self, rel1: Relation, rel2: Relation, name: str):
        # We check the arguments given
        self.__checkArgs(rel1,rel2)

        # We create the new name

        #name = "DiffOf_" + rel1.getName() + "_BY_" + rel2.getName()
        
        # We create the new relation
        self.newRel = Relation(rel1.getDataBase(),name,rel1.getArgs())

        # We create the basic querry
        querry = "SELECT "+ self._argsToString(rel1.getArgs()) + " FROM " + rel1.getName() + " EXCEPT " + "SELECT "+ self._argsToString(rel1.getArgs()) + " FROM " + rel2.getName()
        self.__createQuerry(rel1,rel2)
        self._addTupples(querry)

        if(self.isOneExp):
            self.querry = querry
        


    def __checkArgs(self,rel1: Relation, rel2: Relation):
        # We need to check if both relations have the same arguments before moving any futher
        if (not rel1.getArgs() == rel2.getArgs()):
            raise Exception("Difference not possible"
                            +" because " + rel1.getName() + " does not have the same args than "+ rel2.getName())
        
            
    
    def __createQuerry(self,rel1: Relation, rel2:Relation) -> str:        
        arg1 = self._argsToString(rel1.getArgs())
        arg2 = self._argsToString(rel2.getArgs())
        



    def __fusionQuerries(self, q1: str, q2: str, arg1: dict) -> str:
        querry = "SELECT "+ self._argsToString(arg1) + " FROM (" + q1 + ") AS rel1" + " EXCEPT SELECT "+ self._argsToString(arg1) +  " FROM (" + q2 + ") AS rel2" 
        return querry


