from rel import Relation
from sqliteEnum import SqliteTypes as sType
from sqliteEnum import checkCompatibility

# Every other class in this file is a child of the expression class stocking :
# The new Relation
# The old Relation
# The SQL querry created
# If it's a Querry created from multiple expression : ex -> Project((..),rename(...))
class Expression():
    def __init__(self,oldRel : Relation, newRel : Relation, querry:str, isOneExp = True) -> None:
        self.oldRel     = oldRel
        self.newRel     = newRel
        self.querry     = querry
        self.isOneExp   = isOneExp
    
    def __str__(self) -> str:
        return self.querry

    # Return the arguments as strings
    def _argsToString(self,args)-> str:
        argStr = ""
        for arg in args:
            argStr += arg + ","
        return argStr[0:len(argStr)-1]

    def _addTupples(self, querry: str):
        # We add all the tuples
        cursor = self.newRel.getCursor()
        cursor.execute(querry)
        tuples = cursor.fetchall()
        self.newRel.killCursor()
        for tup in tuples:
            try:
                self.newRel.addTuple(tup)
                
            except Exception as e:
                # Generally this exception is due to the unique constraint of the relation
                # I.E : cannot add the same tuple
                pass

#________________________________________________________________________________________________



class Join(Expression):
    # Join(Rel1,Rel2)

    def __init__(self, rel1: Relation, rel2: Relation, name = None):
            # 4 cas possibles:
        # rel1 est une expression et rel2 aussi
        if (isinstance(rel1,Expression) and isinstance(rel2,Expression)):
            super().__init__(rel1.newRel,None,None,False)
            self.__initialisation(rel1.newRel,rel2.newRel, name)
            self.querry = self.__fusionQuerries(rel1.querry,rel2.querry)

        # rel1 est une relation et rel2 une expression
        elif (isinstance(rel1,Relation) and isinstance(rel2,Expression)):
            super().__init__(rel1,None,None,False)
            self.__initialisation(rel1,rel2.newRel, name)
            self.querry = self.__fusionQuerries(rel1.getName(),rel2.querry)

        # rel1 est une expression et rel2 une relation
        elif (isinstance(rel1,Expression) and isinstance(rel2,Relation)):
            super().__init__(rel1.newRel,None,None,False)
            self.__initialisation(rel1.newRel,rel2, name)
            self.querry = self.__fusionQuerries(rel1.querry,rel2.getName())
        
        # rel1 est une relation et rel2 aussi
        elif (isinstance(rel1,Relation) and isinstance(rel2,Relation)):
            super().__init__(rel1,None,None)
            self.__initialisation(rel1,rel2,name)
            # la querry est ajouter dans __initialisation()


    def __initialisation(self, rel1: Relation, rel2: Relation, name: str):
        # We don't have to check the arguments given since the join method doesn't need that
        self.oldRel2 = rel2
        
        # We do need to create the new dic containing the args
        
        args = self.__createArgs()
        
        
        # We create the Name
        if name == None:
            name = "Join"+rel1.getName()+"_AND_"+rel2.getName()
        # We create the relation
            
        
        self.newRel = Relation(rel1.getDataBase(),name,args)
        # We create the basic querry
        querry = "SELECT * FROM " + rel1.getName() + " NATURAL JOIN " + rel2.getName()
        
        
        self._addTupples(querry)
        # We can keep this querry if the expression is only one
        if self.isOneExp:
            self.querry = querry
        
    def __createArgs(self) -> dict:
        args = dict(self.oldRel.getArgs())
        
        for key in self.oldRel2.getArgs():
            if(not args.__contains__(key)):
                args[key] = self.oldRel2.getArgs()[key]
        
        return args


    def __fusionQuerries(self,q1: str, q2: str) -> str:
        querry = "SELECT * FROM (" + q1 +") AS rel1 NATURAL JOIN (" + q2 + ") AS rel2"
        return querry
    
#________________________________________________________________________________________________


class Select(Expression):
    __acceptedCondition = ('!=','<>','=','>','<','>=','<=')

    def __init__(self,arg1,condition: str,arg2, rel, name = None) -> None:
        # Call the parent constructor
        # If rel is a Relation:
        if(isinstance(rel,Relation)):
            super().__init__(rel,None,None)
            self.__initialisation(arg1,condition,arg2,rel,name)
            
        elif(isinstance(rel,Expression)):
            super().__init__(rel.newRel,None,None,False)
            self.__initialisation(arg1,condition,arg2,rel.newRel,name)
            arg2 = self.__checkArg2(arg2,rel.newRel,arg1)
            self.querry = self.__fusionQuerry(rel,arg1,arg2,condition)
    
    def __initialisation(self, arg1: str, condition: str, arg2: str, rel: Relation,name : str):
        # We check if arg1 is correct
        self.__checkArg1(arg1,rel)
        
        # We check the condition
        condition = self.__checkCondition(condition)
        # We create the new name
        if name == None:
            name = "Sel_" + arg1  + arg2 + "_From" + rel.getName()
        # We can check arg2
        arg2 = self.__checkArg2(arg2,rel,arg1)

        # We can create the new Relation
        self.newRel = Relation(rel.getDataBase(),name,rel.getArgs())
        # We can add the tuples
        querry = "SELECT * FROM " + rel.getName() + " WHERE " + arg1 + " " + condition + " " + arg2

        self._addTupples(querry)
        
        if (self.isOneExp):
            self.querry = querry
        
        

    def __checkCondition(self, condition: str) -> str:
        # We check if the condition is accepted in SQLite
        if not(self.__acceptedCondition.__contains__(condition)):
            raise Exception("'"+condition +"' is not part of the accepted conditions :\n" + str(self.__acceptedCondition))
        return condition

    # Check if arg1 is part of the relation
    def __checkArg1(self, arg1:str, rel: Relation):
        args = rel.getArgs()
        if not args.__contains__(arg1):
            raise Exception("Arg1 must be an argument of the relation: " + rel.getName() 
                + ".\n Or '" + arg1 + "' is not part of this relation.")
    
    # Check if arg2 is a column name if yes we return the same thing
    # If no, we add ' ' 
    def __checkArg2(self,arg2: str, rel: Relation, arg1: str):
        args = rel.getArgs()
        if not args.__contains__(arg2):
            return "'" + arg2 + "'"
        # We need to check that the type of arg1 is the same as arg2
        
        if not checkCompatibility(args[arg1],args[arg2]):
            raise Exception("The type of the column " + arg1 + " ("+ str(args[arg1]) +") "+ "must be compatible with the column " + arg2 + " ("+ str(args[arg2]) +")")

        return arg2

    def __fusionQuerry(self, rel: Expression, arg1, arg2, condition) -> str:
        querry = "SELECT * FROM (" + rel.querry + ") AS " + rel.newRel.getName() + " WHERE " + arg1 + " " + condition + " " + arg2

        return querry
    
    
#________________________________________________________________________________________________


class Union(Expression):
    # Verifier que relation 1 et relation 2 ont les même args
    # 
    def __init__(self,rel1: Relation, rel2: Relation, name = None):
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
        if name == None:
            name = "DiffOf_" + rel1.getName() + "_BY_" + rel2.getName()
        
        # We create the new relation
        self.newRel = Relation(rel1.getDataBase(),name,rel1.getArgs())

        # We create the basic querry
        querry = "SELECT "+ self._argsToString(rel1.getArgs()) + " FROM " + rel1.getName() + " UNION " + "SELECT "+ self._argsToString(rel1.getArgs()) + " FROM " + rel2.getName()
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
        querry = "SELECT "+ self._argsToString(arg1) + " FROM (" + q1 + ") AS rel1" + " UNION SELECT "+ self._argsToString(arg1) +  " FROM (" + q2 + ") AS rel2" 
        return querry

#________________________________________________________________________________________________

class Rename(Expression):
    def __init__(self, oldArgu: str, newArgu: str, rel, name = None) -> None:
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
            if name == None:
                #We create the new name
                self.newName = "RenOf_" + oldArgu + "To" + newArgu + "_From" + rel.getName()
            else:
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
    def __init__(self,args: tuple, rel, name = None) -> None:
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
        if name == None:
            # We create the new name
            argStr = self._argsToString(argsDic).replace(",","")
            name = "PrjOf_" + argStr + "_From" + self.oldRel.getName()
        
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
    def __init__(self,rel1: Relation, rel2: Relation, name = None):
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
        if name == None:    
            name = "DiOf_" + rel1.getName() + "_BY_" + rel2.getName()
        
        # We create the new relation
        self.newRel = Relation(rel1.getDataBase(),name,rel1.getArgs())

        # We create the basic querry
        querry = "SELECT "+ self._argsToString(rel1.getArgs()) + " FROM " + rel1.getName() + " EXCEPT " + "SELECT "+ self._argsToString(rel1.getArgs()) + " FROM " + rel2.getName()
        print(querry)
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
