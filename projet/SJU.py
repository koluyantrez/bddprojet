from rel import Relation
from sqliteEnum import SqliteTypes as sType
from expr import Expression


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
        if args[arg2] != args[arg1]:
            raise Exception("The type of the column " + arg1 + " ("+ str(args[arg1]) +") "+ "must be the same as the column " + arg2 + " ("+ str(args[arg2]) +")")

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
