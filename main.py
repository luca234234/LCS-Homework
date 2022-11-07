import re

input = input().replace(" ",  "")


def is_prop(prop):
    while re.search("(?:\()([^\()\)]*)(?:\))", prop):
        for part in re.findall("\([^\()\)]*\)", prop):
            if re.fullmatch("(\([A-Z][⇒∧∨⇔][A-Z]\))|(\(¬+[A-Z]\))", part):
                prop = re.sub("\([^\()\)]*\)", "P", prop, 1)
            else:
                return False
    if re.fullmatch("[A-Z]", prop):
        return True
    return False


if is_prop(input):
    print("true")
else:
    print("false")