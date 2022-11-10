import sqlite3



class Relation:
    def __init__(self,database: str,name: str, args: dict):
               
        self.name = name                        # The name of the relation

        self.conn = sqlite3.connect(database)   # Links to the given database

        self.c = self.conn.cursor()             # Gets the cursor so we can do some sqlite queries
        
        self.__createArgs(args)
    
        
    # "__" means private function 
    def __createArgs(self,dicoArg):
        # Check if args has at least one element
        if (not isinstance(dicoArg,dict) or len(dicoArg) == 0 ):
            raise Exception("args must be a dictionary with a least one element")
        
        self.args = dicoArg
        #Create the string that will be added in the sql querry to add arguments in the table
        str = ""
        for key in dicoArg:
            str += key + " " + dicoArg[key].value + ","

        str = "(" + str[0:len(str)-1] + ")"

        #Create the querry
        querry = "CREATE TABLE " + self.name + str
        print(querry)
        # If there is an error, this means the table already exist, so we replace the old one
        try:
            self.c.execute(querry)
        except:
            self.deleteRel()
            self.c.execute(querry)

        
        self.conn.commit()
        
        
        

    def deleteRel(self):
        self.c.execute("DROP TABLE " + self.name)
        self.conn.commit()

    

    #reste a faire : def addTuple()
    def addTuple(self,tup: tuple):
        # A tuple needs to be the same length than the number of Arguments
        if(not len(tup) == len(self.args)):
            
            raise Exception("The tuple must have same number of arguments than in " + self.name + " , in this case: " + str(len(self.args)))

        

    

        