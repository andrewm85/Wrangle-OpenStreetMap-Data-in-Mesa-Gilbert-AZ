# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 14:44:55 2021

@author: Andrew Marksberry
"""

import xml.etree.ElementTree as ET
import codecs
import pprint
import json
import re
from collections import defaultdict

#Set file location
osmfile = open('C:/Users/andre/Documents/Mesamap.osm','rb')

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)

phone_number_re = re.compile(r'(?<=^\+).*|^.*', re.IGNORECASE)
phone_numbers = defaultdict(set)
phonenumber = 0

#Expected street values
expected = ["Street", "Avenue", "Boulevard", "Creek", "Drive",
            "Court", "Place", "Road", "Circle", "Highway", "Freeway", 
            "South", "North", "East", "West", "Way", "Parkway", "Array", "Lane",
            "Axiom", "Benton", "Dante", "Drexel", "Encore", "Excimer", "Hassett",
            "Lane", "Lansing", "Magnetic", "Mall", "Olivine", "Sabrina", "Sunview",
            "Synapse", "Verde"]

#Correct street mapping
mapping = {"Blvd": "Boulevard", "Ct": "Court", "Ave": "Avenue", "Dr": "Drive", "Rd": "Road", "St": "Street"}

#Audit the street names and correct the incorrect values
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
            better_name = update(street_name, mapping)
            print (street_name, "=>", better_name)
                        
def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print ('%s: %d' % (k,v))

#Set the is street value
def is_street_name(elem):
    return (elem.attrib['k'] == 'addr:street')

#Perform the update of each street that needs fixed
def update(name, mapping):
    word = name.split()
    for w in range(len(word)):
        if word[w] in mapping:
            word[w] = mapping[word[w]]
    name = ' '.join(word)
    return name

def audit_phone_number(phone_numbers, phone_number):
    m = phone_number_re.search(phone_number)
    if m:
        phone_numbers[1].add(phone_number)
        better_number = updatephone(phone_number, mapping)
        print (phone_number, "=>", better_number)

def updatephone(phone_number, mapping):
    phone_number = phone_number.replace('+','').replace('-', '').replace('(','').replace(')','').replace(' ','').replace('.','')
    if 'x' in phone_number:
        phone_number = phone_number[:10]
    elif phone_number[0] == '1':
        phone_number = phone_number[1:]
    else:
        phone_number
    phone_number = '+1-'+phone_number[0:3]+'-'+phone_number[3:6]+ '-'+phone_number[6:]
    return phone_number

def is_phone_number(elem):
    return (elem.attrib['k'] == 'phone')

#Update Postcode
def update_postcode(postcode):
    match = re.match(r'^\D*(\d{5}).*', postcode)
    clean_postcode = match.group(1)
    return clean_postcode

def is_postcode(elem):
    return (elem.attrib['k'] == 'addr:postcode')

#Initial audit function    
def audit():
    for event, elem in ET.iterparse(osmfile, events=("start",)):
        if (elem.tag == 'way' or elem.tag == 'node'):
            for tag in elem.iter('tag'):
                if is_street_name(tag):
                   audit_street_type(street_types, tag.attrib['v'])
                if is_phone_number(tag):
                    audit_phone_number(phone_numbers, tag.attrib['v'])
                if is_postcode(tag):
                    tag.attrib['v'] = update_postcode(tag.attrib['v'])

def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = audit(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

if __name__ == "__main__":
    audit()