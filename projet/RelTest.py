import rel
from sqliteEnum import SqliteTypes as sType


args = {"A": sType.REAL,"B": sType.TEXT, "C": sType.INTEGER}

#p1 = rel.Relation("relationdata.db","TestRel",args)
p1 = rel.Relation("relationdata.db","R",args)
p2 = rel.Relation("relationdata.db","S",args)




#Print all tables
p1.c.execute("""SELECT name FROM sqlite_master
            WHERE type ='table'; """)

print(p1.c.fetchall())

x = (8.5,"H",98)
y = (1,"O",69)



p1.addTuple(x)
p1.addTuple(y)


p1.c.execute("SELECT * FROM R")
print(p1.c.fetchall())



#print(sType.INTEGER.value)