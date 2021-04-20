# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 12:07:45 2021

@author: Andrew Marksberry 

Parses the OSM data
"""

import xml.etree.ElementTree as ET
from pprint import pprint
import operator

#Set file location
osmfile = 'C:/Users/andre/Documents/Mesamap.osm'

def count_tags(filename):
    """
    Parses the OSM file and count the number of tags by type.
    Args:
        filename: Where the osm file is located
    Returns:
        element_count: dictionary storing the element name and count of occurences 
        k_attributes: dictionary storing k attributes and its correponding value
    """
    element_count = {}
    k_attributes = {}

    # iterate through each elements
    for event, element in ET.iterparse(filename, events=("start",)):
        # Iterate through all tags and get a count for each of them
        element_count[element.tag] = element_count.get(element.tag, 0) + 1

        # for sub elements whose tag is "tag" and has attribute "k", count the occurences for every k attribute
        if element.tag == 'tag' and 'k' in element.attrib:
            k_attributes[element.get("k")] = k_attributes.get(element.get("k"), 0) + 1

    # sort the dictionary by counts in decending order
    k_attributes = sorted(k_attributes.items(), key=operator.itemgetter(1))[::-1]
    element_count = sorted(element_count.items(), key=operator.itemgetter(1))[::-1]

    return element_count, k_attributes

def main():
    """ Starts the counting process """
    element_count, k_attributes = count_tags(osmfile)
    print (element_count)
    print (k_attributes)
    return element_count, k_attributes

if __name__ == "__main__":
    main()