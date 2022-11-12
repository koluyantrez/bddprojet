from rel import Relation
from sqliteEnum import SqliteTypes as sType

argsWare = {"W": sType.TEXT, "Address": sType.TEXT, "City": sType.TEXT}
WAREHOUSES = Relation(":memory:","WAREHOUSES",argsWare)



WAREHOUSES.addTuple(("D1","6, Rue de l'Eglise","Mons"))
WAREHOUSES.addTuple(("D2","18, Place du Parc","Mons"))
WAREHOUSES.addTuple(("D3","18, Place du Parc","Chimay"))
WAREHOUSES.addTuple(("D4","5, Avenue Louise","Enghien"))

