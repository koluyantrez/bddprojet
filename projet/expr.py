from rel import Relation


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


