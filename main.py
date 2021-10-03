import csv
import json
import os
import collections
import pathlib
import xml.etree.ElementTree as ET

def rfile(pattr, path = __file__):            
    currDir = pathlib.Path(path).parent
    for sub in pattr:
        for file in currDir.glob(sub):
            yield file

def rjson(file):
    with open(file, 'r', encoding='utf-8') as f:
        text = json.load(f)
        global _n_, _p_
        Data=[]
        for section, data in text.items():
            ind=[]
            for line in data:
                line = collections.OrderedDict(sorted(line.items(), key=lambda keys: keys[0])) 
                for keys in line.keys():
                    if keys.startswith("D"):
                        _n_ = int(keys[1:]) if int(keys[1:]) >= _n_ else _n_ 
                    if keys.startswith("M") and int(keys[1:]) > _n_ and int(keys[1:]) not in ind:
                        ind.append(int(keys[1:]))
                for id in ind:
                    del line['M' +str(id)]
                Data.append(line)
        return Data

def rcsv(file):
    with open(file, 'r', encoding='utf-8') as f:
        text = csv.DictReader(f)
        global _n_
        Data=[]
        ind=[]
        for line in text:
            line = collections.OrderedDict(sorted(line.items(), key=lambda k: k[0]))
            for keys in line.keys():
                if keys.startswith("D"):
                    _n_ = int(keys[1:]) if int(keys[1:]) >= _n_ else _n_
                if keys.startswith("M") and int(keys[1:]) > _n_ and int(keys[1:]) not in ind:
                    ind.append(int(keys[1:]))
                if keys.startswith("M"):
                    try:
                        line[keys] = int(line[keys])
                    except ValueError:
                        print("Error: invalid value")
            for id in ind:
                del line['M'+str(id)]
            Data.append(line)
        return Data

def rxml(file):
    with open(file, 'r', encoding='utf-8') as f:
        text = ET.parse(file).getroot()
        global _n_
        data=[]
        for objects in text.findall('./objects'):
            line=collections.OrderedDict()
            for obj in objects.findall('object'):
                if obj.attrib['name'].startswith('D') and _n_ == 0:
                    _n_ = int(obj.attrib['name'][1:]) if int(obj.attrib['name'][1:]) >= _n_ else _n_
                try:
                    line[obj.attrib['name']] = int(obj.find('value').text) if obj.attrib['name'].startswith('M') else obj.find('value').text
                except ValueError:
                    line[obj.attrib['name']] = obj.find('value').text
                    print("Error: invaid value")
            line = collections.OrderedDict(sorted(line.items(), key=lambda k: k[0]))
            data.append(line)

        return data
def proccesse():
    pattr=['*.csv', '*.json','*.xml']
    dicts=[]
    for file in rfile(pattr):
        if file.name.endswith('.csv'):
            dicts.append(rcsv(file))
        elif file.name.endswith('.json'):
            dicts.append(rjson(file))
        elif file.name.endswith('.xml'):
            dicts.append(rxml(file))
    result=[]
    for file in dicts:
        for Dict in file:
            result.append(Dict)
    return result

def basic_result():
    data = proccesse()
    data = sorted(data, key=lambda k: k['D1'])
    with open('my_basic_result.tsv', 'wt') as outf:
        tsv_w = csv.writer(outf, delimiter='\t')
        tsv_w.writerow([keys for keys in data[0].keys()])
        for row in data:
            tsv_w.writerow([value for value in row.values()])
    return 
def advance_result():
    return 
_n_=0
advance_result()
basic_result()