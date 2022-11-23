import sqlite3
import os
from sqliteEnum import SqliteTypes as sType


class Relation:
    def __init__(self,database: str,name: str, args: dict):
               
        self.__name = name                        # The name of the relation
        
        self.__dataBase = database

        self.__conn = sqlite3.connect(database)   # Links to the given database

        self.__c = self.__conn.cursor()             # Gets the cursor so we can do some sqlite queries
        self.__nbOfTuple = 0
        self.__createArgs(args)
        self.__conn.close()
    
        
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
        querry = "CREATE TABLE " + self.__name + str
        # If there is an error, this means the table already exist, so we replace the old one
        try:
            self.__c.execute(querry)
            
        except:
            self.deleteRel()
            self.__c.execute(querry)

        

        
        self.__conn.commit()

        
    
        
        
    # Deletes the relation 
    def deleteRel(self):
        self.__c.execute("DROP TABLE " + self.__name)
        self.__conn.commit()
        
   
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
        conn = sqlite3.connect(self.__dataBase)

        c =  conn.cursor()

        # A tuple needs to be the same length than the number of Arguments
        check = self.checkTuple(tup)
        
        
        

        if isinstance(check,tuple):
            res = "Argument " + str(check[0]) + " not matching with the relation " + self.__name + " ,\n" + str(check[1]) + " should be :" + str(check[2])
            if (len(check) > 3):
                res += " or " + str(check[3])
            raise Exception(res)

        elif(check == 0):
            raise Exception("The tuple must have same number of arguments than in " + self.__name + " , in this case: " + str(len(self.args)))
        # The tuple is okay, but we still need to check if it isn't already in the table
        # Since the table cannot have duplicates, if it throws an error it will mean that the tuple already exist in this relation
        querry = "INSERT INTO "+ self.__name +" VALUES "
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
            c.execute(querry)
            self.__nbOfTuple += 1
            conn.commit()
        except Exception as e:

            raise Exception("The tuple "+ str(tupStr) +" already exist in " + self.name)
        
        conn.commit()
        conn.close()
        return querry
        
        
     
    # Print the table in a cool way
    def __str__(self):
        conn = sqlite3.connect(self.__dataBase)
        c = conn.cursor()
        res = self.__name + "|"
        keys = self.__getMaxWordsLen(c)
        
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

        lineSize = len(res) - len(self.__name) - 1
        res += "\n"
        res += " " * len(self.__name) + "|"
        res +="-"* lineSize + "\n"

        # Print all the other line/ tuples:

        # Count the number of tuple
        nbOfTup = self.getNbOfTuple()
        # Seleect all the tuple
        c.execute("SELECT * FROM " + self.__name)
        for i in range(nbOfTup):
            res += " " * len(self.__name) + "| "
            tup = c.fetchone()
            for j in range(nbOfArg):
                res += str(tup[j]) + " "*(keys[keysList[j]] - len(str(tup[j]))) + "  | " 
            
            res += "\n"
        conn.close()
        return res

    # Return a dict that has for each arg the max length for the word
    def __getMaxWordsLen(self,c: sqlite3.Cursor) -> dict:
        keys = {}
        keysList = []
        for key in self.args:
            keys[key] = len(key)
            keysList.append(key) 
        
        nbOfArg = len(keys)

        
        # Count the number of tuple
        nbOfTup = self.getNbOfTuple()
        # Get all tuple
        c.execute("SELECT * FROM " + self.__name)

        # For all tuples
        for  i in range(nbOfTup):
            tup = c.fetchone()
            for j in range(nbOfArg):
                wordLen = len(str(tup[j]))
                
                if keys[keysList[j]]  < wordLen:
                    keys[keysList[j]] = wordLen
        return keys
    

    # ____________________________________________GETTER_________________________________________________
    def getNbOfTuple(self) -> int:
        return self.__nbOfTuple
    
    def getName(self) -> str:
        return self.__name
    
    def getDataBase(self) -> str:
        return self.__dataBase
    
    def getCursor(self) -> sqlite3.Cursor :
        # If cursor raises an error then the database if closed so we open a new connection
        try:
            self.__conn.cursor().execute("SELECT * FROM" + self.__name)
        except:
            self.__conn = sqlite3.connect(self.__dataBase)
            c = self.__conn.cursor()
            return c
        return self.__conn.cursor()
        
    # Kills the connection of the relation to the database, can be open again with getCursor
    def killCursor(self) -> None:
        self.__conn.close()

    def getArgs(self) -> dict:
        return self.args

        

#Return True if the relation exist in the database, False otherwise
# relName: The name of the relation checked
# database: the path to the database being checked
def isInDatabase(relName: str, database: str) -> bool:
    path = database
    isExist = os.path.exists(path)
    if (not isExist):
        raise FileNotFoundError("The file " + database +" has not been found.")
    isIn = True
    conn = sqlite3.connect(database)
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM " + relName)
    except:
        isIn = False
    conn.close()
    return isIn


