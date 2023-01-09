import re


def calcuate(first_char, sign, last_char):
    if sign == "∧":
        return int(first_char) * int(last_char)
    if sign == "∨":
        return max(int(first_char), int(last_char))
    if sign == "⇒":
        if int(first_char) == 1 and int(last_char) == 0:
            return 0
        return 1
    if sign == "⇔":
        if int(first_char) == int(last_char):
            return 1
        return 0


def negate(char):
    if char == "1":
        return "0"
    return "1"


def parse_intp(intp_list):
    intp_dict = {}
    for arg in intp_list:
        intp_dict[arg[0]] = arg[2]
    return intp_dict


def parse_variables(prop):
    variables = re.findall("[A-Z]", prop)
    return list(set(variables))  # removing duplicates


def char_range(c1, c2):
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)


all_prop = {}


class Prop:
    def __init__(self, raw_prop, rep_list=[]):
        self.raw_prop = raw_prop
        self.rep_list = rep_list
        prop = raw_prop
        for rep in rep_list:
            prop = prop.replace(rep, all_prop[rep].full_prop)
        self.full_prop = prop

def first_valid_element(p_list):
    i=0
    while p_list[i] == '' and i<len(p_list)-1:
        i=i+1
    return p_list[i]

def parse_prop(prop):
    not_range = char_range('a', 'z')
    # while non-nested parenthesis exist
    while re.search("(?:\()([^\()\)]*)(?:\))", prop):
        # for every non-nested parenthesis
        for part in re.findall("\([^\()\)]*\)", prop):
            # if the non-nested parenthesis is a valid proposition
            valid_part = re.findall("(\([a-zA-Z][⇒∧∨⇔][a-zA-Z]\))|(\(¬[a-zA-Z]\))", part)
            valid_part = first_valid_element(valid_part[0])
            obj_part = Prop(raw_prop=valid_part, rep_list=re.findall("[a-z]", valid_part))
            p_not = next(not_range)
            all_prop[p_not] = obj_part
            prop = prop.replace(valid_part, p_not)
    return all_prop
