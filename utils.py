import re
from math import floor, ceil
import itertools

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
    if int(char) == 1:
        return 0
    return 1


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


def char_range_adv():
    for i in range(10):
        for c in range(ord('a'), ord('z')+1):
            yield chr(c)+str(i)


class Prop:
    value = None

    def __init__(self, raw_prop, all_prop, rep_list=[]):
        self.raw_prop = raw_prop
        self.rep_list = rep_list
        prop = raw_prop
        for rep in rep_list:
            prop = prop.replace(rep, all_prop[rep].full_prop)
        self.full_prop = prop
        self.value_offset = floor(len(prop)/2)
        self.value_end = ceil(len(prop)/2)-1

    def renew_full(self, all_prop):
        prop = self.raw_prop
        for rep in self.rep_list:
            prop = prop.replace(rep, all_prop[rep].full_prop)
        self.full_prop = prop

def first_valid_element(p_list):
    i = 0
    while p_list[i] == '' and i<len(p_list)-1:
        i = i+1
    return p_list[i]


def all_combiantions(param_list):
    for values in itertools.product([0, 1], repeat=len(param_list)):
        yield dict(zip(param_list, values))


def parse_prop(prop):
    all_prop = {}
    all_parts = []
    not_range = char_range('a', 'z')
    # while non-nested parenthesis exist
    while re.search("(?:\()([^\()\)]*)(?:\))", prop):
        # for every non-nested parenthesis
        for part in re.findall("\([^\()\)]*\)", prop):
            # if the non-nested parenthesis is a valid proposition
            # valid_part = re.findall("(\([a-zA-Z][⇒∧∨⇔][a-zA-Z]\))|(\(¬[a-zA-Z]\))", part)
            # valid_part = first_valid_element(valid_part[0])
            valid_part = part
            if valid_part not in all_parts:
                all_parts.append(valid_part)
                obj_part = Prop(raw_prop=valid_part, all_prop=all_prop, rep_list=re.findall("[a-z]", valid_part))
                p_not = next(not_range)
                all_prop[p_not] = obj_part
                prop = prop.replace(valid_part, p_not)
    return all_prop


def parse_prop_adv(prop):
    all_prop = {}
    all_parts = []
    not_range = char_range_adv()
    # while non-nested parenthesis exist
    while re.search("(?:\()([^\()\)]*)(?:\))", prop):
        # for every non-nested parenthesis
        for part in re.findall("\([^\()\)]*\)", prop):
            # if the non-nested parenthesis is a valid proposition
            # valid_part = re.findall("(\([a-zA-Z][⇒∧∨⇔][a-zA-Z]\))|(\(¬[a-zA-Z]\))", part)
            # valid_part = first_valid_element(valid_part[0])
            valid_part = part
            all_parts.append(valid_part)
            obj_part = Prop(raw_prop=valid_part, all_prop=all_prop, rep_list=re.findall("[a-z][0-9]", valid_part))
            p_not = next(not_range)
            all_prop[p_not] = obj_part
            prop = prop.replace(valid_part, p_not, 1)
    return all_prop