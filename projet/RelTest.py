from rel import Relation
from rel import isInDatabase
from sqliteEnum import SqliteTypes as sType
import relationsForTesting as r

from SPJRUD import Rename
from SPJRUD import Project
from SPJRUD import Diff
from projet.SPJRUD import Join
from projet.SPJRUD import Select

# Project( (tuple d'arg), Relation  ) -> Nouvelle relation


R = Rename("W","WARE",r.WAREHOUSES,"R")
S = Project(("W",),r.STOCK,"S")
E = Rename("W","WARE",S,"E")
T = Join(E,R,"T")

U = Select("WARE","=","D2",T,"U")

print(R.newRel)


print(S.newRel)

print(U.newRel)
V = Select("W","=","400",r.STOCK,"V")

cursor = U.newRel.getCursor()

cursor.execute(U.querry)

print(cursor.fetchall())

U.newRel.killCursor()