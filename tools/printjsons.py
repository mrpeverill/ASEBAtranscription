# This is just a script to print json files neatly.

from pprint import pprint
import json
import argparse

#Read Args
parser = argparse.ArgumentParser()
parser.add_argument("filea", help="First Json.")
parser.add_argument("fileb", help="Second Json.")
args = parser.parse_args()

#Setup printer (just for debug output)
#pp = pprint.PrettyPrinter(indent=4)

with open(args.filea, 'r') as handle:
    filea = json.load(handle)

with open(args.fileb, 'r') as handle:
    fileb = json.load(handle)

    
print("PRINTING FILE A")
with open('fileaout.txt', 'w') as handle:
    pprint(filea,stream=handle)

print("PRINTING FILE B")
with open('filebout.txt', 'w') as handle:
    pprint(fileb,stream=handle)