
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
    intp_dict={}
    for arg in intp_list:
        intp_dict[arg[0]] = arg[2]
    return intp_dict
