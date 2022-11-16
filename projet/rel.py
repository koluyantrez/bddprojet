import sqlite3
from sqliteEnum import SqliteTypes as sType


class Relation:
    def __init__(self,database: str,name: str, args: dict):
               
        self.name = name                        # The name of the relation
        
        self.dataBase = database

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
        allArgs = ""
        for key in dicoArg:
            str += key + " " + dicoArg[key].value + ","
            allArgs += key + ","

        
        str = "(" + str[0:len(str)-1] 
        # Adds the primary key to all column so that we only allow distinct tuples
        str += " ,PRIMARY KEY (" + allArgs[0:len(allArgs)-1] + "));"
        

        #Create the querry to create 
        querry = "CREATE TABLE " + self.name + str
        # If there is an error, this means the table already exist, so we replace the old one
        try:
            self.c.execute(querry)
            
        except:
            self.deleteRel()
            self.c.execute(querry)

        

        
        self.conn.commit()

        
        
        
        
    # Deletes the relation 
    def deleteRel(self):
        self.c.execute("DROP TABLE " + self.name)
        self.conn.commit()
        
   
    # Check if the argument are of the correct type for their attribute
    # 1 = OK
    # 0 = Not the same length than arg
    # tuple = Problem with the type of an attribute and a value of the given tuple -> (Index of the problem in the tuple, Problem value, What type it should be, ... what other type it could be)
    #       ex: (1, "a", int, float) : "a" should be an integer or a float
    
    def checkTuple(self,tup : tuple):
        if(not len(tup) == len(self.args)):
            return 0
        
        index = 0
        for key in self.args:
            arg = self.args[key]
            # Type primitif à tester : str, int, float and None
            # We can skip the rest
            
            # If text then the correct python types is : str
            if arg == sType.TEXT and not isinstance(tup[index],str):
                print("Fail with TEXT")
                return (index, tup[index], str)

            if arg == sType.INTEGER and not isinstance(tup[index], int):
                print("Fail with INTEGER")
                return (index, tup[index], int)

            if arg == sType.REAL and not isinstance(tup[index], float) and not isinstance(tup[index], int):
                print("Fail with REAL")
                return (index, tup[index], float, int)

            if arg == sType.NULL and not tup[index] == None:
                print("Fail with NULL")
                return (index, tup[index], None)
            


            index +=1


        return 1
    

    #reste a faire : def addTuple()
    # Return the SQLite querry as a string
    def addTuple(self,tup: tuple) -> str:
        
        # A tuple needs to be the same length than the number of Arguments
        check = self.checkTuple(tup)
        

        if isinstance(check,tuple):
            res = "Argument " + str(check[0]) + " not matching with the relation " + self.name + " ,\n" + str(check[1]) + " should be :" + str(check[2])
            if (len(check) > 3):
                res += " or " + str(check[3])
            raise Exception(res)

        elif(check == 0):
            raise Exception("The tuple must have same number of arguments than in " + self.name + " , in this case: " + str(len(self.args)))
        # The tuple is okay, but we still need to check if it isn't already in the table
        # Since the table cannot have duplicates, if it throws an error it will mean that the tuple already exist in this relation
        querry = "INSERT INTO "+ self.name +" VALUES "
        tupStr = ""
        if (len(tup) == 1):
            if(isinstance(tup[0],str)):
                tupStr += '("'+str(tup[0])+'")'
            else:
                tupStr += '('+str(tup[0])+')'
            
        else:
            tupStr += str(tup)
        querry += tupStr
        
        try:
            self.c.execute(querry)
            self.conn.commit()
        except:
            raise Exception("The tuple "+ str(tupStr) +" already exist in " + self.name)
        
        self.conn.commit()
        return querry
        
        
     
    # Print the table in a cool way
    def __str__(self):
        res = self.name + "|"
        keys = self.__getMaxWordsLen()
        
        keysList = []
        for key in self.args:
            keysList.append(key) 
        
        nbOfArg = len(keys)

        # Print all the col keys
        for key in keys:
            res += " " + key
            space = " "*(keys[key] + 2 - len(key))
            res += space + "|"
        
        # Print the second line:

        lineSize = len(res) - len(self.name) - 1
        res += "\n"
        res += " " * len(self.name) + "|"
        res +="-"* lineSize + "\n"

        # Print all the other line/ tuples:

        # Count the number of tuple
        nbOfTup = self.getNbOfTuple()
        # Seleect all the tuple
        self.c.execute("SELECT * FROM " + self.name)
        for i in range(nbOfTup):
            res += " " * len(self.name) + "| "
            tup = self.c.fetchone()
            for j in range(nbOfArg):
                res += str(tup[j]) + " "*(keys[keysList[j]] - len(str(tup[j]))) + "  | " 
            
            res += "\n"

        return res

    # Return a dict that has for each arg the max length for the word
    def __getMaxWordsLen(self) -> dict:
        keys = {}
        keysList = []
        for key in self.args:
            keys[key] = len(key)
            keysList.append(key) 
        
        nbOfArg = len(keys)

        
        # Count the number of tuple
        nbOfTup = self.getNbOfTuple()
        # Get all tuple
        self.c.execute("SELECT * FROM " + self.name)

        # For all tuples
        for  i in range(nbOfTup):
            tup = self.c.fetchone()
            for j in range(nbOfArg):
                wordLen = len(str(tup[j]))
                
                if keys[keysList[j]]  < wordLen:
                    keys[keysList[j]] = wordLen
        return keys
    

    # ____________________________________________GETTER_________________________________________________
    # ATTENTION IT USES AN EXECUTE METHOD
    def getNbOfTuple(self) -> int:
        self.c.execute("SELECT COUNT(*) FROM " + self.name)

        return self.c.fetchone()[0]
    
    def getName(self) -> str:
        return self.name
    
    def getDataBase(self) -> str:
        return self.dataBase
    
    def getCursor(self) :
        return self.c

    def getArgs(self) -> dict:
        return self.args

        
     


