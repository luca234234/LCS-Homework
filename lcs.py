import argparse
from ast import literal_eval
from utils import parse_intp
from main import is_prop, compute, truth_table, consequence, equivalence, func_prop, convert_nnf, convert_xnf

# to do:
# - adaptor for relaxed syntax
# - better simplification

my_parser = argparse.ArgumentParser(prog='lcs', add_help=False)
my_parser.add_argument('-p', type=str, help='the proposition')
my_parser.add_argument('-i', help='the interpretation', nargs="*")
my_parser.add_argument('-t', action="store_true")
my_parser.add_argument('-compare', type=str)
my_parser.add_argument('-f', type=str)
my_parser.add_argument('-nnf', action="store_true")
my_parser.add_argument('-dnf', action="store_true")
my_parser.add_argument('-cnf', action="store_true")

args = my_parser.parse_args()
if args.p:
    raw_prop = args.p.replace(" ",  "")
elif args.compare:
    raw_prop = args.compare.replace(" ", "")

check = False

if args.compare:
    if "⊨" in raw_prop:
        operator = "⊨"
        first, second = raw_prop.split("⊨", 1)
        first = first.split(',')
        if type(first) != list:
            first = [first]
        check = 1
        for prop in first:
            check = check * is_prop(prop)
    else:
        operator = "∼"
        first, second = raw_prop.split("∼", 1)
        check = is_prop(first)
    check = check * is_prop(second)
elif args.p:
    check = is_prop(raw_prop)


if check:
    if args.t:
        truth_table(raw_prop)
    elif args.i:
        result = compute(raw_prop, parse_intp(args.i))
        if result == 1:
            print('True')
        else:
            print('False')
    elif args.nnf:
        result = convert_nnf(raw_prop)
        print(result)
    elif args.cnf:
        result = convert_xnf(raw_prop, "∧")
        print(result)
    elif args.dnf:
        result = convert_xnf(raw_prop, "∨")
        print(result)
    elif args.compare:
        if operator == "∼":
            result = equivalence(first, second)
            if result == 1:
                print("is equivalent")
            else:
                print("is not equivalent")
        else:
            result = consequence(first, second)
            if result == 1:
                print("is logical consequence")
            else:
                print("is not logical consequence")
    else:
        print("well formed formula")
elif args.f:
    result = func_prop(literal_eval(args.f))
    print(result)
else:
    print("not well formed formula")
