from rel import Relation
from sqliteEnum import SqliteTypes as sType
from relationsForTesting import WAREHOUSES
from relationsForTesting import STOCK
from relationsForTesting import EMPLOYE
from relationsForTesting import DEPARTEMENT
from PRD import Rename


# Project( (tuple d'arg), Relation  ) -> Nouvelle relation

print(EMPLOYE)
R = Rename("NrEmp","Numero",EMPLOYE)
print(R)

#Idée d'ajout pour rel: check if argument is ok for sqlite



