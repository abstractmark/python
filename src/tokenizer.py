import sys
from fractions import gcd
from functools import reduce

def Tokenize(abstractmark):
    tokenizedData = [];
    data = abstractmark.split('\n')
    #List to determine ammount of tab regardless the indentation
    totalSpaceArray = []
    for i in data:
        newData = {"value": i}
        #Checking wether the line is the last line
        if(i == data[len(data) - 1]): newData["lastElement"] = True
        else: newData["lastElement"] = False
        #Checking the line is in indentation
        if(len(i) > 0):
            if(ord(i[0]) == 32 or ord(i[0]) == 9): newData["hasTab"] = True
            else: newData["hasTab"] = False
        else: newData["hasTab"] = False
        #Coubnt the ammount of spaces or tabs
        totalSpace = 0
        totalTabs = 0
        for j in i:
            if(ord(j) != 32 and ord(j) != 9): break
            if(ord(j) == 9): totalTabs += 1
            elif(ord(j) == 32): totalSpace += 1

        newData["totalSpace"] = totalSpace
        newData["totalTabs"] = totalTabs
        totalSpaceArray.append(totalSpace)
        # Remove indentation from the value
        newData["value"] = newData["value"].strip()
        tokenizedData.append(newData)
    #Greatest common factor function used for finding indentation space.
    indentationSpace = reduce(gcd, totalSpaceArray)
    # If Could not find constant indentation.
    if indentationSpace == 1: print("\x1b[33mAbstractMark warning: 1 Space for indentation space might cause error or unexpected behavior. Please use atleast 2 spaces for your indentation  \x1b[0m")
    if indentationSpace == 0: indentationSpace = 1

    for i in tokenizedData:
        if(i["totalSpace"] and not i["totalTabs"]):
            i["totalTabs"] = i["totalSpace"] // indentationSpace
            del i["totalSpace"]
    
    return tokenizedData
    

sys.modules[__name__] = Tokenize