import rel
from sqliteEnum import SqliteTypes as sType


args = {"A": sType.INTEGER,"B": sType.TEXT, "C": sType.REAL}

p1 = rel.Relation("relationdata.db","TestRel",args)





#Print all tables
p1.c.execute("""SELECT name FROM sqlite_master
            WHERE type ='table'; """)

print(p1.c.fetchall())

x = (3,1,4)
p1.addTuple(x)


#print(sType.INTEGER.value)