from rel import Relation
from sqliteEnum import SqliteTypes as sType


class Project():
    def __init__(self,args : tuple, rel : Relation) -> None:
        self.oldRel = rel
        self.args = args
        # We check the arguments given
        argsDic = self.__checkArgs()
        # The name will be Unique for each projection
        argStr = self.__argsToString().replace(",","")
            
        self.name = "ProjectOf_" + argStr + "_From" + rel.name
        
        self.querry = self.__createQuerry()
        
        
        # We create a new table in the database of the old one
        self.newRel = Relation(rel.dataBase,self.name,argsDic)
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

        #self.oldRel.c.execute("select * from " + self.name)
        #print(self.oldRel.c.fetchall())
    
        
