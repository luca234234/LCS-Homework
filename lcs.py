import argparse
from utils import parse_intp
from main import is_prop, compute, truth_table

my_parser = argparse.ArgumentParser(prog='lcs', add_help=False)
my_parser.add_argument('-p', type=str, help='the proposition')
my_parser.add_argument('-i', help='the interpretation', nargs="*")
my_parser.add_argument('-t', action="store_true")

args = my_parser.parse_args()
raw_prop = args.p.replace(" ",  "")
check = is_prop(raw_prop)

if check:
    if args.t:
        truth_table(raw_prop)
    elif args.i:
        compute(raw_prop, parse_intp(args.i))
    else:
        print("well formed formula")
else:
    print("not well formed formula")
