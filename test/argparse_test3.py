import argparse

# create the top-level parser
parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('--foo', action='store_true', help='foo help')
subparsers = parser.add_subparsers(help='sub-command help')

# create the parser for the "a" command
parser_a = subparsers.add_parser('a', help='a help')
parser_a.add_argument('bar', type=int, help='bar help')

# create the parser for the "b" command
parser_b = subparsers.add_parser('b', help='b help')
parser_b.add_argument('--baz', choices='XYZ', help='baz help')
# print main help
print(parser.format_help())

# retrieve subparsers from parser
subparsers_actions = [
    action for action in parser._actions 
    if isinstance(action, argparse._SubParsersAction)]
# there will probably only be one subparser_action,
# but better safe than sorry
for subparsers_action in subparsers_actions:
    # get all subparsers and print help
    for choice, subparser in subparsers_action.choices.items():
        print("Subparser '{}'".format(choice))
        print(subparser.format_help())