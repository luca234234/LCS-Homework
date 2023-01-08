import argparse
from utils import parse_intp
from main import is_prop, compute, truth_table

my_parser = argparse.ArgumentParser(prog='lcs', add_help=False)
my_parser.add_argument('-p', type=str, help='the proposition')
my_parser.add_argument('-i', help='the interpretation', nargs="*")
my_parser.add_argument('-t')

args = my_parser.parse_args()


raw_prop = args.p.replace(" ",  "")
interp = parse_intp(args.i)

check = is_prop(raw_prop)
truth = {'1': 'True', '0': 'False'}

if interp and check:
    print("well formed formula")
    print(truth[compute(raw_prop, interp)])
elif check:
    if args.t:
        truth_table(raw_prop)
    print("well formed formula")
else:
    print("not well formed formula")
