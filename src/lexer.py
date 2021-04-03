import sys
import re

def isMatch(regex, string):
    return bool(re.search(regex, string))

def Lex(tokenizedData):
    lexedData = []
    for data in tokenizedData:
        newData = data.copy()
        # Showing what each line includes
        newData["includes"] = {};
        # Check whether the line contains heading ID
        if(isMatch(r"(.*?)\{\#(.*?)\}", data["value"])): newData["includes"]["headingId"] = True
        else: newData["includes"]["headingId"] = False
        # Check whether the line contains image
        if(isMatch(r"!\[[^\]]*\]\((.*?)\s*(\"(?:.*[^\"])\")?\s*\)", data["value"])): newData["includes"]["image"] = True
        else: newData["includes"]["image"] = False
        # Check whether the line contains link
        if(isMatch(r"(?<!\!)\[.+\]\(.+\)", data["value"])): newData["includes"]['link'] = True
        else: newData["includes"]["link"] = False
        # Check whether the line contains table
        if(isMatch(r"\|(.*?)\|", data["value"])): newData["includes"]["table"] = True
        else: newData["includes"]["table"] = False
        # Check whether the line contains task list
        if(isMatch(r"^- \[[xX ]\] \S+", data["value"])): newData["includes"]["taskList"] = True
        else: newData["includes"]["taskList"] = False
        # Check whether the line is class definition
        newData["includes"]["defineClass"] = True if data["value"] == "---define" else False
        # Check whether the line is Thematic Break
        newData["includes"]["horizontalRule"] = True if data["value"] == "---" else False
        # Check whether the line is a fenced code block
        if(isMatch(r"^\`\`\`", data["value"])): newData["includes"]["fencedCodeBlock"] = True
        else: newData["includes"]["fencedCodeBlock"] = False
        # Check whether the line is Ordered List
        if(isMatch(r"^\d+\. .", data["value"])): newData["includes"]["orderedList"] = True
        else: newData["includes"]["orderedList"] = False
        # Check whether the line is Unordered List
        if(isMatch(r"^- ((?!\[[xX ]\]).)*$", data["value"])): newData["includes"]["unorderedList"] = True
        else: newData["includes"]["unorderedList"] = False
        # Check whether the line is heading
        if(isMatch(r"^#{1,6} .", data["value"])): newData["includes"]["heading"] = True
        else: newData["includes"]["heading"] = False
        # Check whether the line is a blockquote
        if(isMatch(r"^>+ .", data["value"])): newData["includes"]["blockquote"] = True
        else: newData["includes"]["blockquote"] = False
        # Check whether the line is including external css
        if(isMatch(r"stylesheet\s*(=|:)", data["value"])): newData["includes"]["stylesheet"] = True
        else: newData["includes"]["stylesheet"] = False
        # Check whether the line is including external javascript
        if(isMatch(r"script\s*(=|:)", data["value"])): newData["includes"]["externalScript"] = True
        else: newData["includes"]["externalScript"] = False
        # Check whether the line is marquee tag
        if(isMatch(r"(<~|~>)\s*(.*?)", data["value"])): newData["includes"]["marquee"] = True
        else: newData["includes"]["marquee"] = False
        if(isMatch(r"(.*?)\{((?!(\#|\!|\.)))(.*?)\}", data["value"])): newData["includes"]["inlineStyle"] = True
        # Check whether the line contains inline style
        else: newData["includes"]["inlineStyle"] = False
        # Showing whether the line contains class usage
        if(isMatch(r"(.*?)\{\.(.*?)\}", data["value"])): newData["includes"]["classUsage"] = True
        else: newData["includes"]["classUsage"] = False
        # Push the into array
        lexedData.append(newData)

    return lexedData
            

sys.modules[__name__] = Lex