import re

msgIdPattern = re.compile("^[0-9]{19}$")

def parseIdentifier(idStr):
    return int(idStr) if msgIdPattern.match(idStr) else None
