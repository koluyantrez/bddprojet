from rel import Relation
from sqliteEnum import SqliteTypes as sType

args = {"W": sType.TEXT, "Address": sType.TEXT, "City": sType.TEXT}
WAREHOUSES = Relation("relationdata.db","WAREHOUSES",args)



WAREHOUSES.addTuple(("D1","6, Rue de l'Eglise","Mons"))
WAREHOUSES.addTuple(("D2","18, Place du Parc","Mons"))
WAREHOUSES.addTuple(("D3","18, Place du Parc","Chimay"))
WAREHOUSES.addTuple(("D4","5, Avenue Louise","Enghien"))


args = {"W": sType.TEXT, "Product": sType.TEXT, "Color": sType.TEXT, "Qty": sType.INTEGER}
STOCK = Relation("relationdata.db","STOCK",args)


STOCK.addTuple(("D1","hinge","yellow",200))
STOCK.addTuple(("D1","hinge","blue",150))
STOCK.addTuple(("D2","lock","blue",100))
STOCK.addTuple(("D2","hinge","yellow",200))
STOCK.addTuple(("D2","handle","red",100))
STOCK.addTuple(("D4","hinge","red",150))
STOCK.addTuple(("D4","lock","red",600))

args = {"NrEmp": sType.TEXT, "Dept": sType.TEXT, "Pourcent": sType.INTEGER}

EMPLOYE = Relation("relationdata.db", "EMPLOYE", args)

EMPLOYE.addTuple(("E1","Info",40))
EMPLOYE.addTuple(("E1","Bio",40))
EMPLOYE.addTuple(("E2","Eco",100))
EMPLOYE.addTuple(("E3","Bio",50))
EMPLOYE.addTuple(("E3","Eco",50))
EMPLOYE.addTuple(("E4","Eco",100))
EMPLOYE.addTuple(("E5","Eco",50))
EMPLOYE.addTuple(("E5","Bio",25))
EMPLOYE.addTuple(("E5","Info",25))


args = {"NomDept":sType.TEXT,"Budget":sType.INTEGER,"Chef":sType.TEXT}
DEPARTEMENT = Relation("relationdata.db", "DEPARTEMENT", args)

DEPARTEMENT.addTuple(("Info",5000,"E1"))
DEPARTEMENT.addTuple(("Bio",3500,"E1"))
DEPARTEMENT.addTuple(("Eco",4000,"E5"))


args = {"Emp": sType.TEXT,"Dept": sType.TEXT, "Depuis": sType.TEXT}
EMPLOYES = Relation("relationdata.db","EMPLOYES",args)

EMPLOYES.addTuple(("Ed","Jeux","8 jan 1982"))
EMPLOYES.addTuple(("Ed","MIS","11 jan 1997"))
EMPLOYES.addTuple(("An","Jeux","13 sep 2001"))
EMPLOYES.addTuple(("Pierre","MIS","23 oct 1992"))
EMPLOYES.addTuple(("Pierre","Jeux","11 nov 1995"))

args = {"Dept": sType.TEXT,"Chef": sType.TEXT}
DEPARTEMENTS = Relation("relationdata.db","DEPARTEMENTS",args)

DEPARTEMENTS.addTuple(("Jeux","An"))
DEPARTEMENTS.addTuple(("MIS","Pierre"))






