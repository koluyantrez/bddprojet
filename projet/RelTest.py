import rel
from sqliteEnum import SqliteTypes as sType
from relationsForTesting import WAREHOUSES
from relationsForTesting import STOCK
from relationsForTesting import EMPLOYE
from PRD import Project
from PRD import Rename



# Project( (tuple d'arg), Relation  ) -> Nouvelle relation


#Idée d'ajout pour rel: check if argument is ok for sqlite

print(STOCK)

R = Rename("Product","Aina_Is_Cool1",STOCK)

print(R)


#print(sType.INTEGER.value)
