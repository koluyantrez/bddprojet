import AST
import relationsForTesting

AST.readUserQuery("relationdata.db")


# Some query you can test
# select[(Color,<>,yellow),project[(W,Color,Product),WAREHOUSES]]
# select[(Color,<>,yellow),project[(W,Color,Product),STOCK]]
# select[(Color,<>,yellow),project[(W,Color,Product),STOCK]]
# select[(C,<>,yellow),rename[(Color,C),STOCK]]
# rename[(Qty,Quantity),project[(W,Color,Qty),STOCK]]
# rename[(W,Waahahha),select[(Color,<>,yellow),project[(W,Color,Product),STOCK]]]
# rename[(W,Ware),STOCK]

# union[{project[(W),WAREHOUSES]},{project[(W),STOCK]}]

# diff[{project[(Name),CC]},{project[(Country),Cities]}]


# GOOD : join[{select[(Color,<>,yellow),STOCK]} ,WAREHOUSES]
# GOOD : join[WAREHOUSES,{select[(Color,<>,yellow),STOCK]}]

# GOOD : join[STOCK,{project[(W),WAREHOUSES]}]
# GOOD : join[{select[(Color,<>,yellow),STOCK]},{project[(W,Color,Product),STOCK]}]


# select[(Product,=,handle),project[(W,Product,Qty,Color),STOCK]]
# GOOD : diff[{project[(W),WAREHOUSES]},{project[(W),STOCK]}]
# union[{project[(W),WAREHOUSES]},{project[(W),STOCK]}]
# 
# GOOD : diff[{rename[(Name,Country),project[(Name),CC]]}, {project[(Country),Cities]}]
# GOOD : diff[{project[(W),WAREHOUSES]},{project[(W),STOCK]}]
#