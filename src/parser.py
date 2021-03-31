import sys
import re

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
    if("className" in data): result += f"class=\"{data['className']}\""
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
    else:
        if(data["includes"]["classUsage"]): newData = parseClassUsage(newData)
        if(data["includes"]["inlineStyle"]): newData = parseInlineStyle(newData)
        # Default Heading ID
        newData["headingId"] = re.sub("[^a-zA-Z0-6-]", "", re.sub("<\/?[^>]+(>|$)", "", newData["value"])).lower()[:50]
    return newData


# Main Function
def Parse(lexedData):
    parsedData = []
    # Assign paragraph variable
    endParagraph = False
    paragraphValue = []
    # First, split lexed data by paragraph
    for data in lexedData:
        if(data["value"] == "" and endParagraph): endParagraph = False
        elif (data["value"] == "" and not endParagraph): endParagraph = True
        else:
            newData = {}
            data["value"] = escapeCharacters(data["value"])
            # Parse typography of the value except for link and image
            if not (data["includes"]["image"] and data["includes"]["link"]):
                data["value"] = parseTypography(data["value"])
            # Checking the type of each data
            if(data["includes"]["heading"]):
                newData = parseHeading(data)
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
        
    def toHTML(data):
        htmlData = ""
        for i in data:
            if(i["type"] == "heading"):
                if(i["headingId"]):
                    htmlData += f"<h{i['headingLevel']} id='{i['headingId']}' {parseStyleAndClassAttribute(i)}>{i['value']}</h{i['headingLevel']}>"
                else:
                    htmlData += f"<h{i['headingLevel']} {parseStyleAndClassAttribute(i)}>{i['value']}</h{i['headingLevel']}>"
        return htmlData
    
    parsedHtml = "";

    for data in parsedData:
        if(toHTML(data)): parsedHtml += toHTML(data)

    print(parsedHtml)

    return parsedData

sys.modules[__name__] = Parse