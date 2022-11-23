from rel import Relation
from rel import isInDatabase
from sqliteEnum import SqliteTypes as sType
import relationsForTesting as r

from PRD import Rename
from PRD import Project
from PRD import Diff
from SJU import Join
from SJU import Select

# Project( (tuple d'arg), Relation  ) -> Nouvelle relation


A = Rename("Chef","Emp",r.DEPARTEMENTS)

print(A.newRel)

B = Project(("Dept","Emp"),r.EMPLOYES)

print(B.newRel)

C = Diff(B,A)

D = Project(("Emp",),C)
print(D.newRel)
res = Diff(
    Project(("Emp",),A),
    D
)

print(res.newRel)

cursor = res.newRel.getCursor()
cursor.execute(res.querry)
print(cursor.fetchall())
res.newRel.killCursor()
