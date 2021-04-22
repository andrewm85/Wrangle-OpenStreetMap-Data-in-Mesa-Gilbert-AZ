# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 12:38:14 2021

@author: andre
"""
import sqlite3

conn = sqlite3.connect("C:/Users/Andre/Desktop/OpenStreetMaps.db") 

#Number of Nodes
cur=conn.cursor()
cur.execute("SELECT count(id) FROM nodes")  

data = cur.fetchone()

print ("Number of nodes:",data[0])


#Number of Ways
cur=conn.cursor()
cur.execute("SELECT count(id) FROM ways")  

data = cur.fetchone()

print ("Number of ways:",data[0])


#Number of unique users
cur=conn.cursor()
cur.execute("SELECT DISTINCT count(*) FROM (SELECT uid FROM nodes UNION SELECT uid FROM ways)")  

data = cur.fetchone()

print ("Number of unique users:",data[0])

print()
#Top 10 contributing users
cur=conn.cursor()
cur.execute("""SELECT data.user, COUNT(*) as number
            FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) as data
            GROUP BY data.user
            ORDER BY number DESC
            LIMIT 10;""")  

data = cur.fetchall()

print ("Top 10 contributing users")
for row in data:
    print (row)


print()
#Top 10 amenities
cur=conn.cursor()
cur.execute("""SELECT data.value, COUNT(*)
                FROM (SELECT value, key FROM nodes_tags UNION ALL SELECT value, key FROM ways_tags) as data
                WHERE data.key='amenity' and data.value<>''
                GROUP BY data.value
                ORDER BY Count(*) DESC
                LIMIT 10;""")  

data = cur.fetchall()

print("Top 10 amenities")
for row in data:
    print (row)
    
    