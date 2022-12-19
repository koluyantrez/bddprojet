import tokenizer
import expr
import rel
import SJU
import PRD

stopList = ["stop","close","exit","quit"]
specialToken = ["let","print"]
SPJRUDlist = ["select","project","join","rename","union","diff"]
exprSyntax = {"select":"select[(arg1,condition,arg2),relation/expression]","project" : "project[(arg1,arg2,...,argN),relation/expression]",
               "rename" : "rename[(oldArg,newArg),relation/expression]", "join": "join[relation/{expression1},relation/{expression2}]",
               "union": "union[relation/expression1,relation/expression2]", "difference" : "diff[relation/expression1,relation/expression2]"}

def readUserQuery(database : str):
    print("USING: " + database)
    while(True):
        query = input()
        if stopList.__contains__(query):
            break
        elif query.upper() == "HELP":
            printHelp()
        #tokens = tokenizer.tokenize("select[(W,=,D1),project[(W),WAREHOUSES]]")
        else:
            tokens = tokenizer.tokenize(query)
            try:
                expression = executeQuerry("R",tokens)
                print(expression.newRel)
                print(expression.querry + ";")
                
            except IndexError:
                print("Syntax Error: Perhaps an argument is missing ?")
            except Exception as e: 
                print(e)
                print()
    print("\n")






def executeQuerry(name: str,tokens : list) -> expr.Expression:
    #print(tokens)
    if len(tokens) == 1 or len(tokens) == 0:
        raise Exception("All expressions need to have arguments")
    # Check what expression was entered
    # _______________________________________________________________________________________________________________________________________________________________________________
    # Select[(arg1,condition,arg2),relation/expression]
    if tokens[0] == "select":
        if len(tokens) < 12:
            _syntaxError("Not enough arguments","select",tokens)


        if tokens[1] != '[' or tokens[len(tokens)-1] != ']':
            _syntaxError("The arguments of the 'SELECT' expression must start with [ and end with ]", "select",tokens)
        
        #if tokens[2] != '(' syntax error:
        if tokens[2] != '(':
            _syntaxError("'(' missing", "select", tokens)
        # Gets the args
        arg1 = tokens[3]
        
        condition = tokens[5]
        index = 6
        # In the case that the condition is two tokkens for exemple ! and = or < and >
        if tokens[6] != ',':
            condition += tokens[6]
            
            index += 2
        else:
            index += 1
        arg2 = tokens[index]
        
        # Vérifie que tokens[index + 2] est ')'
        
        if tokens[index + 1] != ')' :
            _syntaxError("')' missing", "select", tokens)
        if tokens[index + 2] != ',':
            _syntaxError("',' missing", "select", tokens)                 
    
        # Vérifie si le dernier paramètre est une expression si oui : CAS RECURSSIF
        if SPJRUDlist.__contains__(tokens[index + 3]):
            
            expression = executeQuerry(name + "ver2",tokens[index + 3:len(tokens)-1])
            return SJU.Select(arg1,condition,arg2,expression,name)
        else:
            relation = rel.getRelation(tokens[index + 3])
            if relation == None:
                raise Exception("Argument Error: \n FROM " + tokenizer.toString(tokens) + "\n There are no relation (created during the execution of the program) called: " + tokens[index + 5])

            return SJU.Select(arg1,condition,arg2,relation,name)
    # _______________________________________________________________________________________________________________________________________________________________________________
    elif tokens[0] == "project":
        
        if tokens[1] != '[' or tokens[len(tokens)-1] != ']':
            _syntaxError("The arguments of the 'SELECT' expression must start with [ and end with ]","project",tokens)
        
        if tokens[2] != '(':
            _syntaxError("'(' missing","project",tokens)
        # Get all the args
        args = []
        index = 0
        nextTok = ""
        
        while nextTok != ')':
            nextTok = tokens[index + 4]
            if(tokens[index + 3] != ','):
                
                args.append(tokens[index + 3]) 
            
            index += 1
            # if nextok = ']' it means that there isn't a ')', that means syntax error
            if(nextTok == ']'):
                _syntaxError("missing a ')' for it's iner arguments","project",tokens)
        args = tuple(i for i in args)
        
        # If the user gave an expression then recursivity
        if SPJRUDlist.__contains__(tokens[index + 5]):
            expression = executeQuerry(name + "ver2",tokens[index + 5:len(tokens)-1])
            return PRD.Project(args,expression,name)
        else:
            relation = rel.getRelation(tokens[index + 5])
            
            # If the relation asked doesn't exit -> error
            if relation == None:
                raise Exception("Argument Error: \n FROM " + tokenizer.toString(tokens) + "\n There are no relation (created during the execution of the program) called: " + tokens[index + 5])
            # else
            
            return PRD.Project(args,relation,name)
    # _______________________________________________________________________________________________________________________________________________________________________________
    elif tokens[0] == "rename":
        if len(tokens) < 9:
            _syntaxError("Not enough Arguments","rename",tokens)


        if tokens[1] != '[' or tokens[len(tokens)-1] != ']':
            _syntaxError("The arguments of the 'RENAME' expression must start with [ and end with ]","rename",tokens)
        if tokens[2] != '(' :
            _syntaxError("'(' missing","rename",tokens)
        # Get all the args
        oldArg = tokens[3]
        newArg = tokens[5]
        if tokens[6] != ')' :
            _syntaxError("')' missing", "rename",tokens)
        if tokens[4] != ',' or tokens[7] != ',':
            _syntaxError("',' missing", "rename", tokens)               

        # If the user  gave an expression then recursivity
        if SPJRUDlist.__contains__(tokens[8]):
            expression = executeQuerry(name + "ver2",tokens[8:len(tokens)-1])
            print(expression)
            return PRD.Rename(oldArg,newArg,expression,name)
        else:
            relation = rel.getRelation(tokens[8])
            
            # If the relation asked doesn't exit -> error
            if relation == None:
                raise Exception("Argument Error: \n FROM " + tokenizer.toString(tokens) + "\n There are no relation (created during the execution of the program) called: " + tokens[8])
            # else
            
            return PRD.Rename(oldArg,newArg,relation,name)
    # _______________________________________________________________________________________________________________________________________________________________________________
    elif tokens[0] == "join":
        if len(tokens) < 6:
            _syntaxError("Not enough arguments", "join", tokens)
        if tokens[1] != '[' or tokens[len(tokens)-1] != ']':
            _syntaxError("The arguments of the 'JOIN' expression must start with [ and end with ]","project",tokens)
        
        args = [1,2]
        index = 0
        # Get the expressions/relations
        for i in range(2):
            # Expression
            
            if tokens[index + 2] == '{':
                

                if not SPJRUDlist.__contains__(tokens[index + 3]):
                    _syntaxError("There must be an expression between '{' and '}'","join",tokens)

                cur = tokens[index +3]
                exp = []
                while cur != "}":
                    exp.append(cur)
                    index += 1
                    cur = tokens[3 + index]
                
                exp = tuple(exp)
                index += 3
                args[i] = executeQuerry(name + "ver2", exp)
            # Relation

            else:
                args[i] = rel.getRelation(tokens[index + 2 ])
                index += 2
                
            
                # If the relation asked doesn't exit -> error
                if args[i] == None:
                    raise Exception("Argument Error: \n FROM " + tokenizer.toString(tokens) + "\n There are no relation (created during the execution of the program) called: " + tokens[index - 2])
            
                
        return SJU.Join(args[0],args[1],name)
        
        
        


# select[(Color,<>,yellow),project[(W,Color,Product),WAREHOUSES]]
# select[(Color,<>,yellow),project[(W,Color,Product),STOCK]]
# select[(Color,<>,yellow),project[(W,Color,Product),STOCK]]
# select[(C,<>,yellow),rename[(Color,C),STOCK]]
# rename[(Qty,Quantity),project[(W,Color,Qty),STOCK]]
# rename[(W,Waahahha),select[(Color,<>,yellow),project[(W,Color,Product),STOCK]]]
# rename[(W,Ware),STOCK]


# GOOD : join[{select[(Color,<>,yellow),STOCK]} ,WAREHOUSES]
# GOOD : join[WAREHOUSES,{select[(Color,<>,yellow),STOCK]}]

# GOOD : join[STOCK,{project[(W),WAREHOUSES]}]
# GOOD : join[{select[(Color,<>,yellow),STOCK]},{project[(W,Color,Product),STOCK]}]


# select[(Product,=,handle),project[(W,Product,Qty,Color),STOCK]]
# project[(c,W),rename[(Color,c),STOCK]]
# Problème car != en token : ['!','=']
        

def printHelp():
    i = 0
    print("Expression Syntax: ")
    for key in exprSyntax:
        jump = " " * (11 - len(key))
        print("\t " + key + jump + ":= " + exprSyntax[key])
        if(i == 2):
            print("")
        i += 1



def _syntaxError(reason : str, expression : str, tokens : tuple):
    raise Exception("Syntax Error: '"+ reason + "' \n From:" + tokenizer.toString(tokens) + "\n Please check that you have something like this : \n " + exprSyntax[expression])