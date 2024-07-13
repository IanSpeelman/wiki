import re

def convertToHtml(content):
    lines = content.splitlines()
    result = ""
    for line in lines:
        result += f"{links(bold(headers(line)))}"
    return result

def headers(line):
    h1 = re.compile("# ")
    h2 = re.compile("## ")
    h3 = re.compile("### ")
    h4 = re.compile("#### ")
    h5 = re.compile("##### ")
    h6 = re.compile("###### ")
    list = re.compile("\* ")
    if h6.match(line):
        return f"<h6>{line.split("# ")[1]}</h6>"
    elif h5.match(line):
        return f"<h5>{line.split("# ")[1]}</h5>"
    elif h4.match(line):
        return f"<h4>{line.split("# ")[1]}</h4>"
    elif h3.match(line):
        return f"<h3>{line.split("# ")[1]}</h3>"
    elif h2.match(line):
        return f"<h2>{line.split("# ")[1]}</h2>"
    elif h1.match(line):
        return f"<h1>{line.split("# ")[1]}</h1>"
    elif list.match(line):
        return f"<li>{line.split("* ")[1]}</li>"
    else:
        return line

def links(line):
    result = re.split("\[|\]|\(|\)", line)
    string = ""
    if len(result) > 1:
        link = []
        for i in range(len(result)):
            if i % 4 == 1:

                link.append(result[i])
            elif i % 4 == 3:
                link.append(result[i])
                string += f"<a href='{link[1]}'>{link[0]}</a>"
                link = []
            else:
                string += result[i]
    string += result[0]
    if len(string) > 0 and string[0] != "<":
        return f"<p>{string}</p>"   
    else:
        return f'{string}'
    
def bold(line):
    boldresult = re.split("\*\*", line)
    string = ""
    if len(boldresult) > 1:
        for i in range(len(boldresult)):
            if i % 2 == 1:
                string += f"<b>{boldresult[i]}</b>"
            else:
                string += boldresult[i]
    return string