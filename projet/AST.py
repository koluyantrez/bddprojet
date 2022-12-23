import tokenizer
import rel
import SPJRUD
import traceback
import readline
import sqlite3

stopList = ["stop","close","exit","quit"]
SPJRUDlist = ["select","project","join","rename","union","diff"]
exprSyntax = {"select":"select[(arg1,condition,arg2),relation/expression]","project" : "project[(arg1,arg2,...,argN),relation/expression]",
               "rename" : "rename[(oldArg,newArg),relation/expression]", "join": "join[relation/{expression1},relation/{expression2}]",
               "union": "union[relation/{expression1},relation/{expression2}]", "difference" : "diff[relation/{expression1},relation/{expression2}]"}

def readUserQuery(database : str):
    print("USING: " + database)
    while(True):
        query = input("> ")
        if stopList.__contains__(query.lower()):
            break
        elif query.upper() == "HELP":
            printHelp()
        else:
                try:
                    tokens = tokenizer.tokenize(query)

                    if len(tokens) == 1 :
                        printRel(tokens[0])
                        
                    elif len(tokens) != 0:
                        name = None
                        index = 0
                        # If there is an equal we can give a name
                        if tokens[1] == '=':
                            name = tokens[0]
                            index += 2

                        expression = executeQuerry(name,tokens[index:])
                        print("\033[96m" + str(expression.newRel) + "\033[0m")
                        print("\033[94m" + expression.querry +  ";"+"\033[0m" )
                        print()
                    else:
                        print()
                except IndexError:
                    print("\033[91mUnknown Error: Perhaps an argument is missing ? \033[0m")
                except Exception as e: 
                    print(e)
                    print()
    print("\n")






def executeQuerry(name: str,tokens : list) -> SPJRUD.Expression:
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
            
            expression = executeQuerry(None,tokens[index + 3:len(tokens)-1])
            try:
                return SPJRUD.Select(arg1,condition,arg2,expression,name)
            except Exception as e:
                _expressionError(e,"select",tokens)
        else:
            relation = rel.getRelation(tokens[index + 3])
            if relation == None:
                _argumentError(tokens[index + 3],tokens)
            try:
                return SPJRUD.Select(arg1,condition,arg2,relation,name)
            except Exception as e:
                _expressionError(e,"select",tokens)
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
            expression = executeQuerry(None,tokens[index + 5:len(tokens)-1])
            try:
                return SPJRUD.Project(args,expression,name)
            except Exception as e:
                _expressionError(e,"project",tokens)
        else:
            relation = rel.getRelation(tokens[index + 5])
            
            # If the relation asked doesn't exit -> error
            if relation == None:
                raise Exception("Argument Error: \n FROM " + tokenizer.toString(tokens) + "\n There are no relation (created during the execution of the program) called: " + tokens[index + 5])
            # else
            try:
                return SPJRUD.Project(args,relation,name)
            except Exception as e:
                _expressionError(e,"project",tokens)
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
            expression = executeQuerry(None,tokens[8:len(tokens)-1])
            try:
                return SPJRUD.Rename(oldArg,newArg,expression,name)
            except Exception as e:
                _expressionError(e,"rename",tokens)
        else:
            relation = rel.getRelation(tokens[8])
            
            # If the relation asked doesn't exit -> error
            if relation == None:
                raise Exception("Argument Error: \n FROM " + tokenizer.toString(tokens) + "\n There are no relation (created during the execution of the program) called: " + tokens[8])
            # else
            try:
                return SPJRUD.Rename(oldArg,newArg,relation,name)
            except Exception as e:
                _expressionError(e,"rename",tokens)
    # _______________________________________________________________________________________________________________________________________________________________________________
    elif tokens[0] == "join":
        if len(tokens) < 6:
            _syntaxError("Not enough arguments", "join", tokens)
        if tokens[1] != '[' or tokens[len(tokens)-1] != ']':
            _syntaxError("The arguments of the 'JOIN' expression must start with [ and end with ]","project",tokens)
        
        args = _getBothArgs(tokens,name)
        try:
            return SPJRUD.Join(args[0],args[1],name)
        except Exception as e:
                _expressionError(e,"join",tokens)
    #_______________________________________________________________________________________________________________________________________________________________________________
    elif tokens[0] == "diff":
        if len(tokens) < 6:
            _syntaxError("Not enough arguments", "difference", tokens)
        if tokens[1] != '[' or tokens[len(tokens)-1] != ']':
            _syntaxError("The arguments of the 'DIFF' expression must start with [ and end with ]","diff",tokens)
        
        args = _getBothArgs(tokens,name)
        try:
            return SPJRUD.Diff(args[0],args[1],name)
        except Exception as e:
                _expressionError(e,"difference",tokens)
    #_______________________________________________________________________________________________________________________________________________________________________________
    elif tokens[0] == "union":
        if len(tokens) < 6:
            _syntaxError("Not enough arguments","union",tokens)
        if tokens[1] != '[' or tokens[len(tokens)-1] != ']':
            _syntaxError("The arguments of the 'UNION' expression must start with [ and end with ]","union",tokens)
        
        args = _getBothArgs(tokens,name)
        try:
            return SPJRUD.Union(args[0],args[1],name)
        except Exception as e:
                _expressionError(e,"union",tokens)
    #_______________________________________________________________________________________________________________________________________________________________________________
    else:
        raise Exception("\033[91mThe expression: " + tokens[0] + " is not part of the SPRJURD expressions\033[0m")
        
    




def printHelp():
    i = 0
    print("Expression Syntax: ")
    for key in exprSyntax:
        jump = " " * (11 - len(key))
        print("\t " + key + jump + ":= " + exprSyntax[key])
        if(i == 2):
            print("")
        i += 1

def printRel(relName: str):
    relation = rel.getRelation(relName)
    if relation == None:
        _argumentError(relName,None)
    print(relation)




def _syntaxError(reason : str, expression : str, tokens : tuple):
    raise Exception("\033[91m Syntax Error: '"+ reason + "' \n From:" + tokenizer.toString(tokens) + "\n Please check that you have something like this : \n " + exprSyntax[expression] + " \033[0m")

def _argumentError(reason: str,tokens: tuple):
    fro = ""
    if tokens != None:
        fro = tokenizer.toString(tokens)
    else:
        fro = reason
    raise Exception("\033[91mArgument Error: \n FROM " + fro + "\n There are no relation (created during the execution of the program) called: " + reason + "\033[0m")

def _expressionError(e: Exception, expression: str, tokens: tuple):
    
    raise Exception("\033[91mExpression Error: \n FROM " + tokenizer.toString(tokens) + "\nCould not execute "+ expression + " expression"  + "\n Reason : " + str(e)   +"\033[0m")


def _getBothArgs(tokens: tuple, name: str) -> list:

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
                args[i] = executeQuerry(None, exp)
            # Relation

            else:
                args[i] = rel.getRelation(tokens[index + 2 ])
                index += 2
                
            
                # If the relation asked doesn't exit -> error
                if args[i] == None:
                    _argumentError(str(tokens[index + 2]),tokens)
        return args
            

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
