from rel import Relation
from sqliteEnum import SqliteTypes as sType
from expr import Expression

Class Union(Expression):
    
    def __init__(self,relA: Relation,relB: Relation)->None:
        #le cas ou aucun des deux n'existent
        
        self.relA=relA
        self.relB=relB
        
        
