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


