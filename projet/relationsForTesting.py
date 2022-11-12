from rel import Relation
from sqliteEnum import SqliteTypes as sType

argsWare = {"W": sType.TEXT, "Address": sType.TEXT, "City": sType.TEXT}
WAREHOUSES = Relation(":memory:","WAREHOUSES",argsWare)



WAREHOUSES.addTuple(("D1","6, Rue de l'Eglise","Mons"))
WAREHOUSES.addTuple(("D2","18, Place du Parc","Mons"))
WAREHOUSES.addTuple(("D3","18, Place du Parc","Chimay"))
WAREHOUSES.addTuple(("D4","5, Avenue Louise","Enghien"))


argsWare = {"W": sType.TEXT, "Product": sType.TEXT, "Color": sType.TEXT, "Qty": sType.INTEGER}
STOCK = Relation(":memory:","STOCK",argsWare)


STOCK.addTuple(("D1","hinge","yellow",200))
STOCK.addTuple(("D1","hinge","blue",150))
STOCK.addTuple(("D2","lock","blue",100))
STOCK.addTuple(("D2","hinge","yellow",200))
STOCK.addTuple(("D2","handle","red",100))
STOCK.addTuple(("D4","hinge","red",150))
STOCK.addTuple(("D4","lock","red",600))





