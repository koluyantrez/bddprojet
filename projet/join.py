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
            super().__init__(rel1.newRel,None,None)
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
    


