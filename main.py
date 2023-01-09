import re
from utils import negate, calcuate, parse_variables, parse_prop


def is_prop(prop):
    # while non-nested parenthesis exist
    while re.search("(?:\()([^\()\)]*)(?:\))", prop):
        # for every non-nested parenthesis
        for part in re.findall("\([^\()\)]*\)", prop):
            # if the non-nested parenthesis is a valid proposition
            if re.fullmatch("(\([A-Z][⇒∧∨⇔][A-Z]\))|(\(¬[A-Z]\))", part):
                # replace it with a letter in the original prop
                prop = re.sub("(\([A-Z][⇒∧∨⇔][A-Z]\))|(\(¬[A-Z]\))", "P", prop, 1)
            else:
                # is not a valid prop
                return False
        # repeats until there are no more paired parenthesis
    # if only a letter remains
    if re.fullmatch("[A-Z]", prop):
        # is a valid prop
        return True
    return False


def compute(prop, interp):
    for i in prop:
        if i in interp:
            prop = prop.replace(i, interp[i])
    while re.search("(?:\()([^\()\)]*)(?:\))", prop):
        for part in re.findall("\([^\()\)]*\)", prop):

            if re.fullmatch("\([01][⇒∧∨⇔][01]\)", part):
                char = str(calcuate(part[1], part[2], part[3]))
                prop = re.sub("\([01][⇒∧∨⇔][01]\)", char, prop, 1)

            if re.fullmatch("\(¬[01]\)", part):
                char = negate(part[2])
                prop = re.sub("\(¬[01]\)", char, prop, 1)
    if prop == '1':
        print('True')
    else:
        print('False')


def truth_table(prop):
    variables = parse_variables(prop)
    propositions = parse_prop(prop)
    for i in variables:
        print(i, end=" ")
    for i in propositions:
        print(propositions[i].full_prop, end=" ")