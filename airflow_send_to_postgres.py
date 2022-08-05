#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 11:17:50 2022

@author: limaindonesia
"""

import psycopg2

try :
    conn = psycopg2.connect(user="postgres",
                                  password="postgres",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="scrap_hukumonline")
    
    conn.autocommit = True
    cursor = conn.cursor()
    print("Connection Success")
    
    cursor.execute("DROP TABLE IF EXISTS scrap_berita")
    
    sql = '''CREATE TABLE scrap_berita(
    Judul VARCHAR(100) NOT NULL,
    Link VARCHAR(100) NOT NULL,
    Berita VARCHAR(2000) NOT NULL,
    Category VARCHAR(50) NOT NULL
    )'''
    #sql = '''CREATE database scrap_hukumonline''';
    cursor.execute(sql)
    
    print("Tables Created Successfully")
    #print("Database created successfully........")
    conn.close()
    
except:
    print("Connection Error")
    
    
