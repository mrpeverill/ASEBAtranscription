import json
import csv
import os
import re
import sys
path = sys.argv[1]

#This script reads ASEBA data from a file and outputs it to a CSV file.

#source: https://hackersandslackers.com/extract-data-from-complex-json-python/
def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results

jsons = {}
for filename in os.listdir(path):
    if re.match(".*\.json", filename):
        #print("found file %s" % filename)
        with open(os.path.join(path, filename), 'r') as f:
            bname=os.path.basename(filename)
            #print("Reading file %s" % bname)
            jsons[bname]=json.load(f)

answersets = {}
for subject in jsons:
    answersets[subject]={}
    for form in jsons[subject]['Forms']:
        for answer in form['FormInstrument']['Answers']:
            #print(answer)
            answersets[subject][answer['QuestionId']]=answer['Value']

qset=sorted(set(extract_values(jsons,'QuestionId')))
#print(sorted(qset))
sset=set(answersets.keys())
print(sset)
with open('csvfromjson.csv', mode='w',newline='') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['']+qset)
    for subject in sset:
        row=[subject]
        for i in qset:
            try:
                row.append(answersets[subject][i])
            except KeyError:
                row.append('')
        csv_writer.writerow(row)
    
