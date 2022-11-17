from rel import Relation
from sqliteEnum import SqliteTypes as sType
from expr import Expression

class Rename(Expression):
    def __init__(self, oldArgu: str, newArgu: str, rel) -> None:
        #Call the parent constructor

        # If it's an expression then 
        # we just mention that the sql querry is going
        # to be modified instead of created
        if (isinstance(rel,Expression)):
            super().__init__(rel.newRel,None,None,False)
            # We initialize the basic attributes: newName, oldArg, newArg  and Relation
            self.__initialisation(oldArgu,newArgu,self.oldRel)

        # If it's a relation then
        # We will just create an sql querry
        elif(isinstance(rel,Relation)):
            super().__init__(rel,None,None)
            # We initialize the basic attributes: newName, oldArg, newArg and Relation
            self.__initialisation(oldArgu,newArgu,rel)
            self.querry = self.__createNewQuerry()

            
    
    def __initialisation(self,oldArgu,newArgu,rel : Relation):
            self.__checkArgs(oldArgu,newArgu)
            self.oldArg = oldArgu
            self.newArg = newArgu

            #We create the new name
            self.newName = "RenameOf_" + oldArgu + "To" + newArgu + "_From" + rel.getName()

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

# ___________________________________________________________________________________________________
class Project(Expression):
    def __init__(self,args: tuple, rel) -> None:
        #Call the parent constructor

        # If it's an expression then 
        # we just mention that the sql querry is going
        # to be modified instead of created
        if (isinstance(rel,Expression)):
            super().__init__(rel.newRel,None,None,False)
            # We initialize the basic attributes: newName, oldArg, newArg  and Relation
            self.__initialisation(args,self.oldRel)

        # If it's a relation then
        # We will just create an sql querry
        elif(isinstance(rel,Relation)):
            super().__init__(rel,None,None)
            # We initialize the basic attributes: newName, oldArg, newArg and Relation
            self.__initialisation(args,rel)
            self.querry = self.__createNewQuerry()

    def __initialisation(self,args: dict, oldRel: Relation):
        # We check the arguments given
        argsDic = self.__checkArgs(args)
        # We create the new name
        argStr = self.__argsToString(argsDic).replace(",","")
        name = "ProjectOf_" + argStr + "_From" + self.oldRel.getName()
        # We create the new relation
        self.newRel = Relation(self.oldRel.getDataBase(),name,argsDic)
        # We fill this table
        querry = self.__createNewQuerry()
        # If it's only one expression we can juste create a basic querry
        if(self.isOneExp):
            self.querry = querry
        else:
            self.querry = self.__modifyQuerry()

        self.__addTuples(querry)

    def __addTuples(self,querry):
        # We get a new cursor
        cursor = self.oldRel.getCursor()
        cursor.execute(querry)
        tuples = cursor.fetchall()
        # We kill the curent cursor
        self.oldRel.killCursor()
        for tup in tuples:
            try:
                self.newRel.addTuple(tup)
            except Exception as e:
                # Generally this exception is due to the unique constraint of the relation
                # I.E : cannot add the same tuple
                pass




    def __createNewQuerry(self) -> str:
        # SELECT ARG1,ARG2,...,ARGn FROM RELNAME;
        argStr = self.__argsToString(self.newRel.getArgs())

        querry = "SELECT " + argStr + " FROM " + self.oldRel.getName()
        return querry
    def __modifyQuerry(self) -> str:
        return None
    
    # Return the arguments as strings
    def __argsToString(self,args)-> str:
        argStr = ""
        for arg in args:
            argStr += arg + ","
        return argStr[0:len(argStr)-1]

    
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
