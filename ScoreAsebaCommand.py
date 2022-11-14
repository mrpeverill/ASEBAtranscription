import json
import csv
import argparse
import pprint
import warnings
import time
import numpy as np
import os
from AsebaParseScripts import *

#This script will attempt to convert a csv file from a digital data entry platform (such as Redcap) in to a set of json files readable by the ASEBA scoring program. It depends on AsebaParseScripts.py, and additionally requires a mapping file. CBCL and YSR data output files as well as the mapping file are specified at the command line.

#Configure Warnings
def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
    return ' %s:%s: %s:%s\n' % (os.path.basename(filename), lineno, category.__name__, message)

warnings.formatwarning = warning_on_one_line

#Read Args
parser = argparse.ArgumentParser()
parser.add_argument("mapping", help="Specify the CSV file with the study variable mappings.")
parser.add_argument("cbcl", help="Specify the CSV with the CBCL school age (6-18) form data.")
parser.add_argument("ysr", help="Specify the CSV with the YSR school age (6-18) form data.")
args = parser.parse_args()

#Setup printer (just for debug output)
pp = pprint.PrettyPrinter(indent=4)

#Read Mapping
mapping={}
with open(args.mapping, 'r') as csvfile:
    csvReader=csv.DictReader(csvfile)
    for rows in csvReader:
        id = rows['QuestionId']
        mapping[id] = rows


recordindex=str(mapping['1000']['SourceField'])


#scrubadub.clean("John is a tool", replace_with='identifier')

#Read CBCL Data
cbcldata={}
with open(args.cbcl, 'r') as csvfile:
    csvReader=csv.DictReader(csvfile)
    for rows in csvReader:
        #id = scrubadub.clean(rows['subid'], replace_with='identifier')
        id = rows[recordindex]
        cbcldata[id] = rows

#pp.pprint(cbcldata['3001'])

#Read YSR Data
ysrdata={}
with open(args.ysr, 'r') as csvfile:
    csvReader=csv.DictReader(csvfile)
    for rows in csvReader:
        id = rows[recordindex]
        ysrdata[id] = rows

#Try to clean out identifiable info.


#Make a Subject List
slist=list(cbcldata.keys())
ysrslist=list(ysrdata.keys())
cbclmisslist = np.setdiff1d(ysrslist,slist)

if len(cbclmisslist)!=0:
    warnings.warn("Records %s are in the ysr data file but not the cbcl data file. They will not be processed because right now we can only get age and gender from the cbcl file. Please add lines to the cbcl file (they do not need to have keyed form data)" % [str(i) + ", " for i in cbclmisslist], UserWarning)
#print(slist)

try:
    os.mkdir('output',)
except OSError as exc:  # Python >2.5
    if os.path.isdir('output'):
        print("output directory exists")
        pass
    else:
        raise

for i in slist: #["5010"]:
    print("processing %s " % i)
    try: 
        ysrtemp=ysrdata[i]
    except KeyError:
        warnings.warn("Record %s is not in YSR file; youth data will be missing" % i,UserWarning)
        ysrtemp=None
    sdict=asebadictformat(mapping,cbcldata[i],ysrtemp)
    with open(os.path.join('output',i+'.json'), 'w') as fp:
        json.dump(sdict, fp)

with open(os.path.join('output','[Content_Types].xml'), 'w') as fp:
    fp.write("""<?xml version="1.0" encoding="utf-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="json" ContentType="" /></Types>""")
#This will print a python dict based on our example json file.
#with open("9999.json") as json_file:
#   data = json.load(json_file)

