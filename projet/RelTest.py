from rel import Relation
from sqliteEnum import SqliteTypes as sType
from relationsForTesting import WAREHOUSES
from relationsForTesting import STOCK
from relationsForTesting import EMPLOYE
from relationsForTesting import DEPARTEMENT
from PRD import Rename
from PRD import Project
from PRD import Diff

# Project( (tuple d'arg), Relation  ) -> Nouvelle relation

print(WAREHOUSES)

#R = Rename("W","WARE",
#        Project(("W","Address"),WAREHOUSES))

#print(R.querry)
#c = EMPLOYE.getCursor()
#c.execute(R.querry)
#res = c.fetchall()
#EMPLOYE.killCursor()
#print(res)
#print(R.newRel)


R = Project(("NrEmp",),EMPLOYE)
S = Project(("Chef",),DEPARTEMENT)
U = Rename("Chef","NrEmp",S)


T = Diff(R,U.newRel)
#Idée d'ajout pour rel: check if argument is ok for sqlite


print(T.newRel)

