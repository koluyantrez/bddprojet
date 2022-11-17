from rel import Relation
from sqliteEnum import SqliteTypes as sType
from relationsForTesting import WAREHOUSES
from relationsForTesting import STOCK
from relationsForTesting import EMPLOYE
from relationsForTesting import DEPARTEMENT
from PRD import Rename
from PRD import Project


# Project( (tuple d'arg), Relation  ) -> Nouvelle relation

print(EMPLOYE)

R = Project(("W",),WAREHOUSES)

print(R.querry)

#Idée d'ajout pour rel: check if argument is ok for sqlite



