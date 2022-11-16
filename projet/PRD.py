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
            super().__init__(rel.newRel,None,None,True)
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
            raise Exception("The relation " + self.oldRel.__name + " doesn't contain any argument called: " + oldArg)
        if (oldArg == newArg):
            raise Exception("It is useless to rename an argument to the same name")
        if (self.oldRel.args.__contains__(newArg)):
            raise Exception("The relation " + self.oldRel.__name + " already has another argument called: " + newArg)

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

        