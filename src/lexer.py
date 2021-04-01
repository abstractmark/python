import sys
import re
def Lex(tokenizedData):
    lexedData = []
    for data in tokenizedData:
        newData = data.copy()
        # Showing what each line includes
        newData["includes"] = {};
        # Check whether the line contains heading ID
        if(re.match(r"(.*?)\{\#(.*?)\}", data["value"])): newData["includes"]["headingId"] = True
        else: newData["includes"]["headingId"] = False
        # Check whether the line contains image
        if(re.match(r"!\[[^\]]*\]\((.*?)\s*(\"(?:.*[^\"])\")?\s*\)", data["value"])): newData["includes"]["image"] = True
        else: newData["includes"]["image"] = False
        # Check whether the line contains link
        if(re.match(r"(?<!\!)\[.+\]\(.+\)", data["value"])): newData["includes"]['link'] = True
        else: newData["includes"]["link"] = False
        # Check whether the line contains table
        if(re.match(r"\|(.*?)\|", data["value"])): newData["includes"]["table"] = True
        else: newData["includes"]["table"] = False
        # Check whether the line contains task list
        if(re.match(r"^- \[[xX ]\] \S+", data["value"])): newData["includes"]["taskList"] = True
        else: newData["includes"]["taskList"] = False
        # Check whether the line is class definition
        newData["includes"]["defineClass"] = True if data["value"] == "---define" else False
        # Check whether the line is Thematic Break
        newData["includes"]["horizontalRule"] = True if data["value"] == "---" else False
        # Check whether the line is a fenced code block
        if(re.match(r"^\`\`\`", data["value"])): newData["includes"]["fencedCodeBlock"] = True
        else: newData["includes"]["fencedCodeBlock"] = False
        # Check whether the line is Ordered List
        if(re.match(r"^\d+\. .", data["value"])): newData["includes"]["orderedList"] = True
        else: newData["includes"]["orderedList"] = False
        # Check whether the line is Unordered List
        if(re.match(r"^- ((?!\[[xX ]\]).)*$", data["value"])): newData["includes"]["unorderedList"] = True
        else: newData["includes"]["unorderedList"] = False
        # Check whether the line is heading
        if(re.match(r"^#{1,6} .", data["value"])): newData["includes"]["heading"] = True
        else: newData["includes"]["heading"] = False
        # Check whether the line is a blockquote
        if(re.match(r"^>+ .", data["value"])): newData["includes"]["blockquote"] = True
        else: newData["includes"]["blockquote"] = False
        # Check whether the line is including external css
        if(re.match(r"stylesheet\s*(=|:)", data["value"])): newData["includes"]["stylesheet"] = True
        else: newData["includes"]["stylesheet"] = False
        # Check whether the line is including external javascript
        if(re.match(r"script\s*(=|:)", data["value"])): newData["includes"]["externalScript"] = True
        else: newData["includes"]["externalScript"] = False
        # Check whether the line is marquee tag
        if(re.match(r"(<~|~>)\s*(.*?)", data["value"])): newData["includes"]["marquee"] = True
        else: newData["includes"]["marquee"] = False
        if(re.match(r"(.*?)\{((?!(\#|\!|\.)))(.*?)\}", data["value"])): newData["includes"]["inlineStyle"] = True
        # Check whether the line contains inline style
        else: newData["includes"]["inlineStyle"] = False
        # Showing whether the line contains class usage
        if(re.match(r"(.*?)\{\.(.*?)\}", data["value"])): newData["includes"]["classUsage"] = True
        else: newData["includes"]["classUsage"] = False
        # Push the into array
        lexedData.append(newData)

    return lexedData
            

sys.modules[__name__] = Lex