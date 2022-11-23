from rel import Relation
from sqliteEnum import SqliteTypes as sType
from expr import Expression


class Join(Expression):
    # Join(Rel1,Rel2)

    def __init__(self, rel1: Relation, rel2: Relation):
            # 4 cas possibles:
        # rel1 est une expression et rel2 aussi
        if (isinstance(rel1,Expression) and isinstance(rel2,Expression)):
            super().__init__(rel1.newRel,None,None,False)
            self.__initialisation(rel1.newRel,rel2.newRel)
            self.querry = self.__fusionQuerries(rel1.querry,rel2.querry)

        # rel1 est une relation et rel2 une expression
        elif (isinstance(rel1,Relation) and isinstance(rel2,Expression)):
            super().__init__(rel1,None,None,False)
            self.__initialisation(rel1,rel2.newRel)
            self.querry = self.__fusionQuerries(rel1.getName(),rel2.querry)

        # rel1 est une expression et rel2 une relation
        elif (isinstance(rel1,Expression) and isinstance(rel2,Relation)):
            super().__init__(rel1.newRel,None,None,False)
            self.__initialisation(rel1.newRel,rel2)
            self.querry = self.__fusionQuerries(rel1.querry,rel2.getName())
        
        # rel1 est une relation et rel2 aussi
        elif (isinstance(rel1,Relation) and isinstance(rel2,Relation)):
            super().__init__(rel1,None,None)
            self.__initialisation(rel1,rel2)
            # la querry est ajouter dans __initialisation()


    def __initialisation(self, rel1: Relation, rel2: Relation):
        # We don't have to check the arguments given since the join method doesn't need that
        self.oldRel2 = rel2
        
        # We do need to create the new dic containing the args
        args = self.__createArgs()
        
        # We create the Name
        name = "Joined"+rel1.getName()+"_AND_"+rel2.getName()
        # We create the relation
        self.newRel = Relation(rel1.getDataBase(),name,args)
        # We create the basic querry
        querry = "SELECT * FROM " + rel1.getName() + " NATURAL JOIN " + rel2.getName()
        self._addTupples(querry)
        # We can keep this querry if the expression is only one
        if self.isOneExp:
            self.querry = querry
        
    def __createArgs(self) -> dict:
        args = self.oldRel.getArgs()
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

    def __init__(self,arg1,condition: str,arg2, rel) -> None:
        # Call the parent constructor
        # If rel is a Relation:
        if(isinstance(rel,Relation)):
            super().__init__(rel,None,None)
            self.__initialisation(arg1,condition,arg2,rel)
            
        elif(isinstance(rel,Expression)):
            super().__init__(rel.newRel,None,None,False)
            self.__initialisation(arg1,condition,arg2,rel.newRel)
            arg2 = self.__checkArg2(arg2,rel.newRel)
            self.querry = self.__fusionQuerry(rel,arg1,arg2,condition)
    
    def __initialisation(self, arg1: str, condition: str, arg2: str, rel: Relation):
        # We check if arg1 is correct
        self.__checkArg1(arg1,rel)
        
        # We check the condition
        condition = self.__checkCondition(condition)
        # We create the new name
        name = "Select_" + arg1  + arg2 + "_From" + rel.getName()
        # We can check arg2
        arg2 = self.__checkArg2(arg2,rel)

        # We can create the new Relation
        self.newRel = Relation(rel.getDataBase(),name,rel.getArgs())
        # We can add the tuples
        querry = "SELECT * FROM " + rel.getName() + " WHERE " + arg1 + " " + condition + " " + arg2
        print(querry)
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
    def __checkArg2(self,arg2: str, rel: Relation):
        args = rel.getArgs()
        if not args.__contains__(arg2):
            return "'" + arg2 + "'"
        return arg2

    def __fusionQuerry(self, rel: Expression, arg1, arg2, condition) -> str:
        querry = "SELECT * FROM (" + rel.querry + ") AS " + rel.newRel.getName() + " WHERE " + arg1 + " " + condition + " " + arg2

        return querry
    
