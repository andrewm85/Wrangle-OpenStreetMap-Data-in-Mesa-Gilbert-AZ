# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 10:31:35 2021

@author: andre
"""
import sqlite3
import pandas
from sqlite3 import Error

def create_connection(db_file):
    
    conn = None
    
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        
    return conn



def create_table(conn, create_table_sql):
    
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print (e)
        
        
        
def main():
    database = r"C:/Users/Andre/Desktop/OpenStreetMaps.db"
    
    
    sql_create_nodes_table = """CREATE TABLE IF NOT EXISTS nodes (
                             id INTEGER PRIMARY KEY NOT NULL,
                             lat REAL,
                             lon REAL,
                             user TEXT,
                             uid INTEGER,
                             version INTEGER,
                             changeset INTEGER,
                             timestamp TEXT
                             );"""
            
    sql_create_nodes_tags_table = """CREATE TABLE IF NOT EXISTS nodes_tags (
                              id INTEGER,
                              key TEXT,
                              value TEXT,
                              type TEXT,
                              FOREIGN KEY (id) REFERENCES nodes(id)
                              );"""

    sql_create_ways_table = """CREATE TABLE IF NOT EXISTS ways (
                        id INTEGER PRIMARY KEY NOT NULL,
                        user TEXT,
                        uid INTEGER,
                        version TEXT,
                        changeset INTEGER,
                        timestamp TEXT
                        );"""

    sql_create_ways_tags_table = """CREATE TABLE IF NOT EXISTS ways_tags (
                             id INTEGER NOT NULL,
                             key TEXT NOT NULL,
                             value TEXT NOT NULL,
                             type TEXT,
                             FOREIGN KEY (id) REFERENCES ways(id)
                             );"""

    sql_create_ways_nodes_table = """CREATE TABLE IF NOT EXISTS ways_nodes (
                              id INTEGER NOT NULL,
                              node_id INTEGER NOT NULL,
                              position INTEGER NOT NULL,
                              FOREIGN KEY (id) REFERENCES ways(id),
                              FOREIGN KEY (node_id) REFERENCES nodes(id)
                              );"""

    conn = create_connection(database)


    if conn is not None:
        create_table(conn, sql_create_nodes_table)
    
        create_table(conn, sql_create_nodes_tags_table)
    
        create_table(conn, sql_create_ways_table)
    
        create_table(conn, sql_create_ways_tags_table)
    
        create_table(conn, sql_create_ways_nodes_table)
    else:
        print("Error! Cannot connect ot database")

    
    nodes = "C:/Users/Andre/Documents/Mesamap_nodes.csv"
    nodes_tags = "C:/Users/Andre/Documents/Mesamap_nodes_tags.csv"
    ways = "C:/Users/Andre/Documents/Mesamap_ways.csv"
    ways_tags = "C:/Users/Andre/Documents/Mesamap_ways_tags.csv"
    ways_nodes = "C:/Users/Andre/Documents/Mesamap_ways_nodes.csv"

    i = 1

    while i <= 5:
        if i == 1:
            table_name = "nodes"
            file = nodes
        elif i == 2:
            table_name = "nodes_tags"
            file = nodes_tags
        elif i == 3:
            table_name = "ways"
            file = ways
        elif i == 4:
            table_name = "ways_tags"
            file = ways_tags
        elif i == 5:
            table_name = "ways_nodes"
            file = ways_nodes
        i=i+1
        
        df = pandas.read_csv(file)
        df.to_sql(table_name, conn, if_exists='append', index=False)     



if __name__ =='__main__':
    main()
