import re
from utils import negate, calcuate, parse_variables, parse_prop, all_combiantions, parse_prop_adv
from math import floor, ceil, prod


def is_prop(prop):
    # while non-nested parenthesis exist
    while re.search("(?:\()([^\()\)]*)(?:\))", prop):
        # for every non-nested parenthesis
        for part in re.findall("\([^\()\)]*\)", prop):
            # if the non-nested parenthesis is a valid proposition
            if re.fullmatch("(\([A-Z][⇒∧∨⇔][A-Z]\))|(\(¬[A-Z]\))", part):
                # replace it with a letter in the original prop
                prop = prop.replace(part, 'P')
            else:
                # is not a valid prop
                return 0
        # repeats until there are no more paired parenthesis
    # if only a letter remains
    if re.fullmatch("[A-Z]", prop):
        # is a valid prop
        return 1
    return 0


def compute(prop, interp):
    for i in prop:
        if i in interp:
            prop = prop.replace(i, str(interp[i]))
    while re.search("(?:\()([^\()\)]*)(?:\))", prop):
        for part in re.findall("\([^\()\)]*\)", prop):
            if re.fullmatch("\([01][⇒∧∨⇔][01]\)", part):
                char = str(calcuate(part[1], part[2], part[3]))
                prop = prop.replace(part, str(char))

            if re.fullmatch("\(¬[01]\)", part):
                char = negate(part[2])
                prop = prop.replace(part, str(char))
    return int(prop)


def truth_table(prop):
    variables = parse_variables(prop)
    propositions = parse_prop(prop)
    for i in variables:
        print(i, end=" ")
    for i in propositions:
        print(propositions[i].full_prop, end=" ")
    print()
    for temp_intp in all_combiantions(variables):
        for i in variables:
            print(temp_intp[i], end=" ")
        for i in propositions:
            prop_part = propositions[i].raw_prop
            if len(prop_part) == 5:
                propositions[i].value = calcuate(temp_intp[prop_part[1]], prop_part[2], temp_intp[prop_part[3]])
            elif len(prop_part) == 4:
                propositions[i].value = negate(temp_intp[prop_part[2]])
            temp_intp[i] = propositions[i].value
            print(' ' * propositions[i].value_offset, propositions[i].value, ' ' * propositions[i].value_end, sep="", end=" ")
        print()


def equivalence(first, second):
    variables = parse_variables(first+second)
    for i in variables:
        print(i, end=" ")
    print(first, second)
    first_offset = floor(len(first) / 2)
    second_offset = floor(len(second) / 2)
    first_end = ceil(len(first) / 2) - 1
    second_end = ceil(len(second) / 2) - 1
    equivalent = 1
    for temp_intp in all_combiantions(variables):
        for i in variables:
            print(temp_intp[i], end=" ")
        first_value = compute(first, temp_intp)
        second_value = compute(second, temp_intp)
        print(' ' * first_offset, first_value, ' ' * first_end, sep="", end=" ")
        print(' ' * second_offset, second_value, ' ' * second_end, sep="")
        if first_value != second_value:
            equivalent = 0
    return equivalent


def consequence(first, second):
    variables = parse_variables(''.join(first)+second)
    print(*first, second)
    first_offsets = [floor(len(i) / 2) for i in first]
    first_end = [ceil(len(i) / 2) - 1 for i in first]
    second_offset = floor(len(second) / 2)
    second_end = ceil(len(second) / 2) - 1
    prop_consequence = 0
    not_consequence = False
    for temp_intp in all_combiantions(variables):
        first_values = [compute(i, temp_intp) for i in first]
        second_value = compute(second, temp_intp)
        for i in range(len(first_values)):
            print(' ' * first_offsets[i], first_values[i], ' ' * first_end[i], sep="", end=" ")
        print(' ' * second_offset, second_value, ' ' * second_end, sep="")
        if prod(first_values) == 1:
            if second_value == 0:
                not_consequence = True
            else:
                prop_consequence = 1
    if not_consequence:
        return 0
    return prop_consequence


def func_prop(function):
    variable_list = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    n_length = len(function[0])
    variable_list = variable_list[0:n_length]
    func_str = '('
    for combiantion in function:
        interpretation = dict(zip(variable_list, combiantion))
        list1 = []
        list0 = []
        for char in interpretation:
            if interpretation[char] == 0:
                list0.append(char)
            else:
                list1.append(char)
        if list0:
            func_str += f'¬{list0[0]}∧'
        if list1:
            func_str += f'{list1[0]}∧'
        for i in list0[1:]:
            func_str += f'({list0[0]}⇔{i})∧'
        for i in list1[1:]:
            func_str += f'({list1[0]}⇔{i})∧'
        func_str = func_str[:-1]+')∨('
    func_str = func_str[:-2]
    return func_str


def convert_nnf(prop, print=True):
    # ((P⇔Q)⇔(¬(P⇒(¬Q))))
    # (((¬()∨(¬(P⇒(¬Q))))∧((¬(¬(P⇒(¬Q))))∨(((¬P)∨Q)∧((¬Q)∨P))))
    variables = parse_variables(prop)
    for i in variables:
        prop = prop.replace(i, i+i)
    propositions = parse_prop_adv(prop)
    change = 1
    while change:
        change = 0
        for i in propositions.values():
            if i.raw_prop[3] == "⇔":
                i.raw_prop = f"(((¬{i.raw_prop[1:3]})∨{i.raw_prop[4:6]})∧((¬{i.raw_prop[4:6]})∨{i.raw_prop[1:3]}))"
                change = 1
            if i.raw_prop[3] == "⇒":
                i.raw_prop = f"((¬{i.raw_prop[1:3]})∨{i.raw_prop[4:6]})"
                change = 1
            elif i.raw_prop[1] == "¬" and len(i.raw_prop) == 5 and i.rep_list:
                taged_prop = propositions[i.rep_list[0]].raw_prop
                if "∧" in taged_prop:
                    propositions[i.rep_list[0]].raw_prop = "((¬" + taged_prop[1:].replace("∧", ")∨(¬") + ")"
                    propositions[i.rep_list[0]].renew_full(propositions)
                    i.raw_prop = i.rep_list[0]
                    change = 1
                elif "∨" in taged_prop:
                    propositions[i.rep_list[0]].raw_prop = "((¬" + taged_prop[1:].replace("∨", ")∧(¬") + ")"
                    propositions[i.rep_list[0]].renew_full(propositions)
                    i.raw_prop = i.rep_list[0]
                    change = 1
            i.renew_full(propositions)
        result = list(propositions.values())[-1].full_prop
        for i in variables:
            # ... (to be continued)
            if f"(¬(¬{i+i}))" in result:
                result = result.replace(f"(¬(¬{i+i}))", i+i)
                change = 1
        propositions = parse_prop_adv(result)
    for i in variables:
        result = result.replace(i+i, i)
        if print:
            # ... (to be continued)
            result = result.replace(f"(¬{i})", f"¬{i}")
    return result


def convert_xnf(prop, char):
    if char == "∧":
        op_char = "∨"
    else:
        op_char = "∧"
    prop = convert_nnf(prop, print=False)
    variables = parse_variables(prop)
    for i in variables:
        prop = prop.replace(i, i + i)
    propositions = parse_prop_adv(prop)
    change = 1
    while change:
        change = 0
        for i in propositions.values():
            if i.raw_prop[3] == op_char and i.rep_list:
                for rep in i.rep_list:
                    if change == 0:
                        sub_prop = propositions[rep].raw_prop
                        if char in sub_prop:
                            if rep == i.raw_prop[4:6]:
                                propositions[i.rep_list[0]].raw_prop = "((" + sub_prop[1:3] + op_char + i.raw_prop[1:3] + f"){char}(" + sub_prop[4:6] + op_char + i.raw_prop[1:3] + "))"
                            else:
                                propositions[i.rep_list[0]].raw_prop = "((" + sub_prop[1:3] + op_char + i.raw_prop[4:6] + f"){char}(" + sub_prop[4:6] + op_char + i.raw_prop[4:6] + "))"
                            i.raw_prop = rep
                            propositions[rep].renew_full(propositions)
                            change = 1
            i.renew_full(propositions)
        result = list(propositions.values())[-1].full_prop
        propositions = parse_prop_adv(result)
    return result
