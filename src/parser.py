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

            print(data["value"])
    return parsedData

sys.modules[__name__] = Parse