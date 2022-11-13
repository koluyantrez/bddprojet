import rel
from sqliteEnum import SqliteTypes as sType
from relationsForTesting import WAREHOUSES
from relationsForTesting import STOCK
from PRD import Project



# Project( (tuple d'arg), Relation  ) -> Nouvelle relation





R = Project(("City",), WAREHOUSES)

print(R.newRel)


#print(sType.INTEGER.value)
