from rel import Relation
from rel import isInDatabase
from sqliteEnum import SqliteTypes as sType
from relationsForTesting import WAREHOUSES
from relationsForTesting import STOCK
from relationsForTesting import EMPLOYE
from relationsForTesting import DEPARTEMENT

from PRD import Rename
from PRD import Project
from PRD import Diff
from join import Join

# Project( (tuple d'arg), Relation  ) -> Nouvelle relation

print(WAREHOUSES)


T = Project(("W"),WAREHOUSES)
S = Project(("W","Product"),STOCK)


R = Join(STOCK,WAREHOUSES)

c = R.newRel.getCursor()
c.execute(str(R))
print(c.fetchall())

R.newRel.killCursor()

print(R.newRel)

