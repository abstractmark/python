import sys
import re

# Function check a string contains a regular expression
def isMatch(regex, string):
    return bool(re.search(regex, string))

# Replace all special characters in code with it's corresponding html entity
def replaceSpecialCharacters(str):
    str = re.sub("&", "&amp;", str)
    str = re.sub("\*", "&ast;", str)
    str = re.sub(">", "&gt;", str)
    str = re.sub("<", "&lt;", str)
    str = re.sub("\"", "&quot;", str)
    str = re.sub("'", "&#39;", str)
    str = re.sub("\\\\\`", "&#96;", str)
    str = re.sub("\`", "&#96;", str)
    str = re.sub("\{", "&#123;", str)
    str = re.sub("\}", "&#125;", str)
    str = re.sub("\_", "&UnderBar;", str)
    str = re.sub("\!", "&#33;", str)
    str = re.sub("\%", "&percnt;", str)
    str = re.sub("\~", "&#126;", str)
    return str

def parseClassUsage(data):
    data["className"] = ""
    for i in range(0, len(data["value"]) - 1):
        # Check whether the value contains "{!" and ends with "}"
        if(data["value"][i] == "{" and data["value"][i + 1] == "."):
            # Temporary variable to remove class chars
            newValue = data["value"][:i]
            for j in range(i + 2, len(data["value"])):
                if (data["value"][j] == "}"):
                    data["value"] = newValue + data["value"][j + 1 :]
                    data["value"] = data["value"].strip()
                    data["className"] = data["className"].strip()
                    return data
                else: data["className"] += data["value"][j]
    return data

def parseInlineStyle(data):
    data["inlineStyle"] = ""
    for i in range(0, len(data["value"]) - 1):
        # Check whether the value contains "{" and ends with "}" but it isn't heaidng id nor class
        if(data["value"][i] == "{" and data["value"][i + 1] != "!" and data["value"] != "#"):
            # Temporary variable to remove style chars
            newValue = data["value"][:i]
            for j in range(i + 1, len(data["value"])):
                if(data["value"][j] == "}"):
                    data["value"] = newValue + data["value"][j + 1 :].strip()
                    data["value"] = data["value"].strip()
                    return data
                else: data["inlineStyle"] += data["value"][j]
    return data


# Add class attribute and style attribute to element
def parseStyleAndClassAttribute(data):
    result = ""
    if("className" in data): result += f" class=\"{data['className']}\""
    if("inlineStyle" in data): result += f" style=\"{data['inlineStyle']}\""
    return result

# Replace all escape characters to it's html entities
def escapeCharacters(data):
    data = re.sub("\\\\\*", "&ast;", data)
    data = re.sub("\\\\\&", "&amp;", data)
    data = re.sub("\\\\\<", "&lt;", data)
    data = re.sub("\\\\\>", "&gt;", data)
    data = re.sub("\\\\\"", "&quot;", data)
    data = re.sub("\\\\\'", "&#39;", data)
    data = re.sub("\\\\\%", "&percnt;", data)
    data = re.sub("\\\\\_", "&UnderBar;", data)
    data = re.sub("\\\\\`", "&#96;", data)
    data = re.sub("\\\\\{", "&#123;", data)
    data = re.sub("\\\\\|", "&#125;", data)
    data = re.sub("\\\\\[", "&lbrack;", data)
    data = re.sub("\\\\\]", "&rbrack;", data)
    data = re.sub("\\\\\(", "&lpar;", data)
    data = re.sub("\\\\\)", "&rpar;", data)
    data = re.sub("\\\\\\\\", "&bsol;", data)
    data = re.sub("\\\\\|", "&vert;", data)
    data = re.sub("\\\\\!", "&#33;", data)
    data = re.sub("\\\\\~", "&#126;", data)
    data = re.sub("\\\\\@", "&commat;", data)
    data = re.sub("\\\\\#", "&num;", data)
    data = re.sub("\\\\\$", "&dollar;", data)
    data = re.sub("\\\\\^", "&Hat;", data)
    data = re.sub("\\\\\=", "&equals;", data)
    data = re.sub("\\\\\+", "&plus;", data)
    data = re.sub("\\\\\;", "&semi;", data)
    data = re.sub("\\\\\:", "&colon;", data)
    data = re.sub("\\\\\,", "&comma;", data)
    data = re.sub("\\\\\.", "&period;", data)
    data = re.sub("\\\\\/", "&sol;", data)
    data = re.sub("\\\\\?", "&quest;", data)
    data = re.sub("\\\\\-", "&#45;", data)
    return data

def parseTypography(data):
    def codeTypography(m):
        return f"<code>{replaceSpecialCharacters(m.group(1))}</code>"
    data = re.sub(f"\*\*(.*?)\*\*", r"<b>\1</b>", data)
    data = re.sub(f"_(.*?)_", r"<i>\1</i>", data)
    data = re.sub(f"%(.*?)%", r"<u>\1</u>", data)
    data = re.sub(f"\~\~(.*)\~\~", r"<del>\1</del>", data)
    data = re.sub(f"\`([^\`]+)\`", codeTypography, data)
    return data

# A recursion functioin to parse all link syntax
def parseLink(data):
    newData = ""
    text = ""
    url = ""
    continueLoopIndex = 0 # Variable to help changing iterator value
    # Checking for the syntax of link
    for i in range(len(data)):
        i = continueLoopIndex
        if i >= continueLoopIndex:
            continueLoopIndex += 1
        
        if(data[i] == "["):
            # Finding the end of the text
            for j in range(i + 1, len(data) - 1):
                if(data[j] == "]" and data[j + 1] == "("):
                    continueLoopIndex = j + 1
                    break
                else:
                    text += data[j]
        # Parsing the URL
        elif(data[i] == "(" and data[i - 1] == "]"):
            for j in range(i + 1, len(data)):
                if(data[j] == ")"):
                    newData += f"<a href = \"{url}\">{text}</a>"
                    i = len(data)
                    # Add others text into new data
                    for k in range(j + 1, len(data)):
                        newData += data[k]
                    # Call this function again to parse all link
                    while (isMatch(r"(?<!\!)\[.+\]\(.+\)", newData)):
                        newData = parseLink(newData)
                    return newData
                else:
                    url += data[j]
        else:
            newData += data[i]
    return newData

# Parse heading
def parseHeading(data):
    newData = {"type": "heading", "headingLevel": 0}
    # checking heading level
    for char in data["value"]:
        # Stop the loop when the character is not "#"
        if(char != "#"): break
        else: newData["headingLevel"] += 1
    newData["value"] = data["value"][newData["headingLevel"] + 1:]
    # Check if the heading includes heading id
    if(data["includes"]["headingId"]):
        newData["headingId"] = "";
        for i in range(len(data["value"])):
            # Check whether the heading contains "{#" and ends with "}"
            if(data["value"][i] == "{" and data["value"][i + 1] == "#"):
                # Temporary variable to remove heading id chars
                newValue = newData["value"][: i- newData["headingLevel"] - 1]
                for j in range(i + 2, len(data["value"])):
                    if(data["value"][j] == "}"):
                        newData["value"] = newValue + newData["value"][(j - newData["headingLevel"]):].strip()
                        break
                    else: newData["headingId"] += data["value"][j]
        # Remove unecessary space from heading id
        newData["headingId"] = newData["headingId"].strip()
        if(data["includes"]["classUsage"]): newData = parseClassUsage(newData)
        if(data["includes"]["inlineStyle"]): newData = parseInlineStyle(newData)
        if(data["includes"]["link"]): newData["value"] = parseLink(newData["value"])
    else:
        if(data["includes"]["classUsage"]): newData = parseClassUsage(newData)
        if(data["includes"]["inlineStyle"]): newData = parseInlineStyle(newData)
        if(data["includes"]["link"]): newData["value"] = parseLink(newData["value"])
        # Default Heading ID
        newData["headingId"] = re.sub("[^a-zA-Z0-6-]", "", re.sub("<\/?[^>]+(>|$)", "", newData["value"])).lower()[:50]
    return newData

def parseBlockquote(lexedData, index):
    # Index usedto skip element until the index
    breakIndex = None
    newData = {"type": "blockquote", "value": []}
    # Check if it's followed by blockquote
    for i in range(index, len(lexedData)):
        # End the loop if it's not followed by blockquote
        if(not lexedData[i]["includes"]["blockquote"]):
            index = i
            breakIndex = i
            break
        else:
            blockquoteDepthLevel = 0
            trimmedValue = ""
            # Check blockqupte's depth level and remove blockquote syntax from blockquote value
            for j in range(len(lexedData[i]["value"])):
                # Check blockquote's syntax
                if(lexedData[i]["value"][j] == ">"): blockquoteDepthLevel += 1
                else:
                    trimmedValue = lexedData[i]["value"][blockquoteDepthLevel:].strip()
                    break
            blockquoteData = {"value": trimmedValue, "blockquoteDepthLevel": blockquoteDepthLevel}
            # Get style and class information about the blockquote
            if(lexedData[i]["includes"]["classUsage"]): blockquoteData = parseClassUsage(blockquoteData)
            if(lexedData[i]["includes"]["inlineStyle"]): blockquoteData = parseInlineStyle(blockquoteData)
            if(lexedData[i]["includes"]["link"]): blockquoteData["value"] = parseLink(blockquoteData["value"])
            # Push the data
            newData["value"].append(blockquoteData)

    # A recursive function to parse blockquoteand its children into html tags
    def parseDescendants(parent, data, index):
        result = ""
        for i in range(index, len(data["value"])):
            # Break when meets a blockquote with the same depth level and its index is higher than parent index
            if(parent == data["value"][i]["blockquoteDepthLevel"] and i != index): break
            # If the blockquote depth level is the same as parent depth level + 1
            if(parent + 1 == data["value"][i]["blockquoteDepthLevel"]):
                # If it's not an empty string
                result += f"<blockquote{parseStyleAndClassAttribute(data['value'][i])}>{parseTypography(data['value'][i]['value'])}{parseDescendants(parent + 1, data, i)}</blockquote>" if bool(len(parseDescendants(parent + 1, data, i))) else f"<blockquote{parseStyleAndClassAttribute(data['value'][i])}>{parseTypography(data['value'][i]['value'])}</blockquote>"
        return result
    
    newData['value'] = parseDescendants(0, newData, 0)
    if(not breakIndex): breakIndex = len(lexedData) - 1
    else: breakIndex -= 1
    return {'data': newData, 'breakIndex': breakIndex, 'endParagraph': breakIndex == len(lexedData) - 1}
            

def parseImage(data):
    newData = {"type": "image", "value": data["value"], "altText": "", "imageSrc": ""}
    if(data["includes"]["classUsage"]): newData = parseClassUsage(newData)
    if(data["includes"]["inlineStyle"]): newData = parseInlineStyle(newData)
    continueLoopIndex = 0 # Variable to help changing iterator value
    for i in range(0, len(newData["value"]) - 1):
        i = continueLoopIndex
        if i >= continueLoopIndex:
            continueLoopIndex += 1
        # Check whether if it is started with ![
        if newData["value"][i] == "!" and newData["value"][i + 1] == "[":
            for j in range(i + 2, len(newData["value"])):
                # Break the loop if it is ended with ]
                if newData["value"][j] == "]":
                    continueLoopIndex = j + 1
                    break
                else: newData["altText"] += newData["value"][j] #Otherwise, save it as Alt text
        elif(newData["value"][i] == "("):
            for j in range(i + 1, len(newData["value"])):
                if(newData["value"][j] == ")"):
                    return newData
                else: newData["imageSrc"] += newData["value"][j] # Get image source


    return newData

def parseMarquee(data):
    newData = {"type": "marquee", "value": data["value"][2:].strip()}
    # Parse class and inline style
    if(data["includes"]["classUsage"]): newData = parseClassUsage(newData)
    if(data["includes"]["inlineStyle"]): newData = parseInlineStyle(newData)
    # CHeck the marquee direction
    direction = "right" if data["value"][0:2] == "~>" else "left"
    newData["value"] = f"<div class='marquee' data-direction='{direction}'><div class='marquee-content'{parseStyleAndClassAttribute(newData)}>{newData['value']}</div></div>"

    if("inlineStyle" in newData): del newData["inlineStyle"]
    if("className" in newData): del newData["className"]
    return newData

def parseTable(lexedData, index):
    newData = {"type": "table", "value": {"head": [], "body": []}}
    breakIndex = None
    def parseTableRow(row):
        tableRowValue = []
        # Checking the table syntax
        if(row[0] != "|"): return None
        else:
            tableDataValue = ""
            for i in range(len(row)):
                if(i == len(row) - 1 and row[i] != "|"):
                    tableDataValue += row[i]
                    # Parse class usage and inline style
                    classUsage = parseClassUsage({"value": tableDataValue})
                    inlineStyle = parseInlineStyle({"value": classUsage.value})
                    # Check if className and inlineStyle is not empty string
                    if(classUsage.className): newData["className"] = classUsage["className"]
                    if(inlineStyle["inlineStyle"]): newData["inlineStyle"] = inlineStyle["inlineStyle"]
                elif(row[i] == "|"):
                    # Pusing table data value to table row value array if it's not an empty string table data value
                    value = escapeCharacters(tableDataValue.strip())
                    # Parse the value if it's an image
                    if(isMatch(r'!\[[^\]]*\]\((.*?)\s*(\"(?:.*[^"])")?\s*\)', value)):
                        newValue = {"altText": "", "imageSrc": ""}
                        continueLoopIndex = 0
                        for j in range(len(value)):
                            if continueLoopIndex > 0 and index < continueLoopIndex:
                                continue
                            if(value[j] == "|" and value[j + 1] == "["):
                                for k in range(j + 2, len(value)):
                                    # Break the loop if it is ended with ]
                                    if(value[k] == "]"):
                                        continueLoopIndex = k
                                        break
                                    else: newValue["altText"] += value[k] # Otherwise save it as Alt text
                            elif(value[j] == "("):
                                for k in range(j + 1, len(value)):
                                    if(value[j] == ")"):
                                        break
                                    else: newValue["imageSrc"] += value[k]
                        value = f"<img src='{newValue['imageSrc']}' alt='{newValue['altText']}' />"
                    else: value = parseLink(parseTypography(value))
                    if(tableDataValue): tableRowValue.append(value)
                    tableDataValue = ""
                else: tableDataValue += row[i]
        return tableRowValue
    for i in range(index, len(lexedData)):
        if(not lexedData[i]["includes"]["table"]):
            breakIndex = i
            break
        else:
            if(i == index):
                newData["value"]["head"] = parseTableRow(lexedData[i]["value"])
            else:
                # Function to check if it isa heading syntax (===== OR -----)
                def checkHeadingSyntax(data):
                    for j in range(len(data)):
                        for k in range(len(data[j])):
                            if(data[j][k] != "-" and data[j][k] != "="):
                                return False
                    return True
                # If it's not heading syntax, then push it to tbody
                if(not checkHeadingSyntax(parseTableRow(lexedData[i]["value"]))):
                    newData["value"]["body"].append(parseTableRow(lexedData[i]["value"]))
    # Merge all to html tags
    def mergeTableRow(tr, isHeading):
        trValue = "<tr>"
        for td in tr:
            trValue += f"<td>{td}</td>" if not isHeading else f"<th>{td}</th>"
        return trValue + "</tr>"
    result = f"<table{parseStyleAndClassAttribute(newData)}><thead>{mergeTableRow(newData['value']['head'], True)}</thead><tbody>"
    for tr in newData["value"]["body"]:
        result += mergeTableRow(tr, False)
    result = f"{result}</tbody></table>"
    newData["value"] = result
    # Delete inline style and class name ket from newData to not to be parsed twice
    if("inlineStyle" in newData): del newData["inlineStyle"]
    if("className" in newData): del newData["className"]
    if(not breakIndex): breakIndex = len(lexedData) - 1
    return {"data": newData, "breakIndex": breakIndex, "endParagraph": breakIndex == len(lexedData) - 1}

# Main Function
def Parse(lexedData):
    parsedData = []
    # Assign paragraph variable
    endParagraph = False
    paragraphValue = []
    # First, split lexed data by paragraph
    continueLoopIndex = 0 # Variable to help changing iterator value
    for index in range(len(lexedData)):
        if continueLoopIndex > 0 and index < continueLoopIndex:
            continue
        data = lexedData[index]
        if(data["value"] == "" and endParagraph): endParagraph = False
        elif (data["value"] == "" and not endParagraph): endParagraph = True
        else:
            newData = {}
            data["value"] = escapeCharacters(data["value"])
            # Parse typography of the value except for link and image
            if not (data["includes"]["image"] and data["includes"]["link"]):
                data["value"] = parseTypography(data["value"])
            # Checking the type of each data
            includesValueList = list(data["includes"].values())
            includesKeyList = list(data["includes"].keys())

            if(data["includes"]["fencedCodeBlock"]):
                newData["type"] = "fencedCodeBlock"
                newData["value"]= data["value"]
                if(data["includes"]["classUsage"]): newData = parseClassUsage(newData)
                if(data["includes"]["inlineStyle"]): newData = parseInlineStyle(newData)
                newData["value"] = ""
                for j in range(index + 1, len(lexedData)):
                    # Check if the line is a fenced code block close tag
                    if(lexedData[j]["includes"]["fencedCodeBlock"]):
                        continueLoopIndex = j + 1
                        # Check if fenced code block close tag is also the end of the file
                        if(lexedData[j]["lastElement"]): endParagraph = True
                        break
                    else: newData["value"] += f"{replaceSpecialCharacters(lexedData[j]['value'])}<br />" # Add a <br> tag in the end of each line

            elif(data["includes"]["defineClass"]):
                newData["type"] = "defineClass"
                newData["value"] = ""
                # Find the close tag of define class
                for i in range(index + 1, len(lexedData)):
                    if(lexedData[i]["value"] == "---"):
                        continueLoopIndex = i + 1
                        # Check if define class close tag is also end of the file
                        if(lexedData[i]["lastElement"]): endParagraph = True
                        break
                    else: newData["value"] += lexedData[i]["value"]

            elif(data["includes"]["stylesheet"]):
                newData["type"] = "stylesheet"
                newData["value"] = re.compile('(https?.\/\/[^\s]+)').findall(data["value"])[0]
            
            elif(data["includes"]["externalScript"]):
                newData["type"] = "scripts"
                newData["value"] = re.compile('(https?.\/\/[^\s]+)').findall(data["value"])[0]

            elif(data["includes"]["horizontalRule"]):
                newData["type"] = "plain"
                newData["value"] = "<hr />"

            elif(data["includes"]["blockquote"]):
                newData = parseBlockquote(lexedData, index)
                # Checking if it's the end of paragraph / file
                endParagraph = newData["endParagraph"]
                # Skip to non-table element
                continueLoopIndex = newData["breakIndex"]
                newData = newData["data"]
                
            elif(data["includes"]["table"]):
                newData = parseTable(lexedData, index);
                # Checking if it's the end of paragraph /file
                endParagraph = newData["endParagraph"]
                # Skip to non-table element
                continueLoopIndex = newData["breakIndex"]
                newData = newData["data"]

            elif(data["includes"]["marquee"]):
                # Calling parseMarquee function
                newData = parseMarquee(data)

            elif(data["includes"]["image"]):
                # Calling parseImage function
                newData = parseImage(data)

            elif(data["includes"]["heading"]):
                # Calling parseHeading Function
                newData = parseHeading(data)
            
            elif(data["includes"]["taskList"]):
                newData["type"] = "taskList";
                newData["checked"] = data["value"][3] == "x" or data["value"][3] == "X"
                newData["value"] = data["value"][5:].strip()
                if(data["includes"]["classUsage"]): newData = parseClassUsage(newData)
                if(data["includes"]["inlineStyle"]): newData = parseInlineStyle(newData)
                if(data["includes"]["link"]): newData["value"] = parseLink(newData["value"])

            # Check if it is a plain text
            elif((True not in includesValueList) or (includesValueList.index(True) == includesKeyList.index("classUsage")) or (includesValueList.index(True) == includesKeyList.index("inlineStyle")) or includesValueList.index(True) == includesKeyList.index("link") ):
                newData["type"] = "plain"
                newData["value"] = data["value"]
                if(data["includes"]["classUsage"]): newData = parseClassUsage(newData)
                if(data["includes"]["inlineStyle"]): newData = parseInlineStyle(newData)
                if(data["includes"]["link"]): newData["value"] = parseLink(newData["value"])
                # Parse typography once again (important for line which contains link)
                newData["value"] = parseTypography(newData["value"])
            # Plain text
            else: paragraphValue.append(data)
            # Push new data
            paragraphValue.append(newData)
        if(endParagraph or data["lastElement"]):
            # Reset Variable to Default
            endParagraph = False
            # Push paragraph information to parsedData
            parsedData.append(paragraphValue)
            paragraphValue = []
    
    stylesheets = []
    scripts = []
    parsedStyleTags = []
    usedTable = []
        
    def toHTML(data):
        htmlData = ""
        for i in range(len(data)):
            if("type" in data[i]):
                if(data[i]["type"] == "plain" or data[i]["type"] == "marquee"):
                    # Add br tag if there is next line and the current line is not horizontal rule inside the paragraph
                    if(i + 1 < len(data) and "type" in data[i + 1]):
                        newLine = i + 1 < len(data) and not bool(re.search(r"<(?!\/?(a|img|b|i|u|del|code)(?=>|\s.*>))\/?.*?>", data[i + 1]["value"])) and data[i + 1]["type"] == "plain" and data[i]["value"] != "<hr />"
                    else:
                        newLine = False
                    if "className" in data[i] or "inlineStyle" in data[i]:
                        htmlData += f"<span{parseStyleAndClassAttribute(data[i])}>{data[i]['value']}</span>{'<br />' if newLine else ''}"
                    else:
                        htmlData += f"{data[i]['value']}{'<br />' if newLine else ''}"
                elif(data[i]["type"] == "heading"):
                    if(data[i]["headingId"]):
                        htmlData += f"<h{data[i]['headingLevel']} id='{data[i]['headingId']}' {parseStyleAndClassAttribute(data[i])}>{data[i]['value']}</h{data[i]['headingLevel']}>"
                    else:
                        htmlData += f"<h{data[i]['headingLevel']} {parseStyleAndClassAttribute(data[i])}>{data[i]['value']}</h{data[i]['headingLevel']}>"
                elif(data[i]["type"] == "fencedCodeBlock"):
                    # Insert fenced code block value inside <code> and <pre> tags
                    htmlData += f"<pre{parseStyleAndClassAttribute(data)}><code>{data[i]['value']}</code></pre>"
                elif(data[i]["type"] == "defineClass"):
                    if(data[i]["value"] not in parsedStyleTags): parsedStyleTags.append(data[i]["value"])
                elif(data[i]["type"] == "taskList"):
                    htmlData += f"<div{parseStyleAndClassAttribute(data[i])}><input type='checkbox' id='{i}' {'checked' if data[i]['checked'] else ''} onclick='return false;' /><label for='{i}'>{data[i]['value']}</label></div>"
                elif(data[i]["type"] == "image"):
                    htmlData += f"<img src={data[i]['imageSrc'] if data[i]['imageSrc'] else ''} alt={data[i]['altText'] if data[i]['altText'] else ''}{parseStyleAndClassAttribute(data[i])} />"
                elif(data[i]["type"] == "stylesheet"):
                    if(data[i]["value"] not in stylesheets): stylesheets.append(data[i]["value"])
                elif(data[i]["type"] == "scripts"):
                    if(data[i]["value"] not in scripts): scripts.append(data[i]["value"])
                elif(data[i]["type"] == "table" or data[i]['type'] == "blockquote"):
                    htmlData += data[i]["value"]
        return htmlData
    
    parsedHtml = "";

    for data in parsedData:
        # Check if the paragraph doesn't need <p> tags
        needParagraphTag = False
        for element in data:
            if "type" in element:
                if element["type"] == "heading":
                    needParagraphTag = False
                    break
                # If it's HTML Element
                elif (re.match(r"<\/?[a-z][\s\S]*>", element["value"])):
                    needParagraphTag = False
                # No need <p> tag if it's blockquote text
                elif (element["type"] == "blockquote"):
                    needParagraphTag = False
                # No need <p> tag if there's no any plain text inside the paragraph
                elif (element["type"] == "plain"):
                    needParagraphTag = not(element["value"] == "<hr />" and len(data) == 1 or re.match(r"<(?!\/?(a|img|b|i|u|del|code)(?=>|\s.*>))\/?.*?>", element["value"]))
        result = toHTML(data)
        if(result):
            if(needParagraphTag): parsedHtml += f"<p>{result}</p>"
            else: parsedHtml += result

    return {"body": parsedHtml, "styles": parsedStyleTags, "stylesheets": stylesheets, "scripts": scripts}

sys.modules[__name__] = Parse