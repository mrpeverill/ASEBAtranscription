import json
import csv
import argparse
import pprint
import warnings
import time
import numpy as np
import os
from AsebaParseLib import *

#This script will attempt to convert a csv file from a digital data entry platform (such as Redcap) in to a set of json files readable by the ASEBA scoring program. It depends on AsebaParseScripts.py, and additionally requires a mapping file. CBCL and YSR data output files as well as the mapping file are specified at the command line.

#Debugging: If you get keyerrors it is likely that either a) your mapping file is incorrect or b) your csv files aren't encoded in UTF-8. To fix this, open the csv in excel, save as, and make sure the file type is 'CSV UTF-8'

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
# If you don't like arguments you can comment all the lines between 'read args' and here and hard code the file paths here:
#E.g. :
#mappingfile=/path/to/your/mappingfile.csv
mappingfile=args.mapping
cbclfile=args.cbcl
ysrfile=args.ysr

#Setup printer (just for debug output)
pp = pprint.PrettyPrinter(indent=4)

#Read Mapping
mapping={}
try:
    with open(mappingfile, 'r', encoding='utf-8-sig') as csvfile:
        csvReader=csv.DictReader(csvfile)
        for rows in csvReader:
            id = rows['QuestionId']
            mapping[id] = rows
except FileNotFoundError:
    print("Error: Mapping file %s not found" % mappingfile)
    exit(1)

recordindex=str(mapping['1000']['SourceField'])
#print("recordindex is %s" % recordindex)

#Read CBCL Data
cbcldata={}
try:
    with open(cbclfile, 'r', encoding='utf-8-sig') as csvfile:
        csvReader=csv.DictReader(csvfile)
        for rows in csvReader:
            #id = scrubadub.clean(rows['subid'], replace_with='identifier')
            id = rows[recordindex]
            cbcldata[id] = rows
except FileNotFoundError:
    print("Error: CBCL file %s not found" % cbclfile)
    exit(1)
except KeyError:
    print("The mapping file says ID column is '%s', but couldn't find that column in the CBCL file (%s). Adjust question 1000 in the mapping to match the id column of the CBCL file. If they appear to match, there may be a problem with the file encoding (see comments at head of script)" % (recordindex,cbclfile)) 

#pp.pprint(cbcldata['3001'])

#Read YSR Data
ysrdata={}
try:
    with open(ysrfile, 'r', encoding='utf-8-sig') as csvfile:
        csvReader=csv.DictReader(csvfile)
        for rows in csvReader:
            id = rows[recordindex]
            ysrdata[id] = rows
except FileNotFoundError:
    print("Error: YSR file %s not found" % ysrfile)
    exit(1)
except KeyError:
    print("The mapping file says ID column is '%s', but couldn't find that column in the YSR file (%s). Adjust question 1000 in the mapping to match the id column of the CBCL file. If they appear to match, there may be a problem with the file encoding (see comments at head of script)" % (recordindex,ysrfile))
    exit(1)

#Try to clean out identifiable info.


#Make a Subject List
slist=list(filter(None,list(cbcldata.keys())))
ysrslist=list(filter(None,list(ysrdata.keys())))
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

print("Finished. Output file must be compressed to zip before import")
