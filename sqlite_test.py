#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 15:17:53 2022
"""

import pandas as pd
import numpy as np
import sqlite3

from numpy import NaN
sheet_id = "1mK8Noe5G7BXF8kr-KXolomsxndT63MBMJF4LYJECZPk"
sheet_name = "IPO_Profit"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

df = pd.read_csv(url)
df.iloc[1,0] = "No"
df.iloc[1,1] = "Ticker"
df.iloc[1,2] = "Date"
df.iloc[1,3] = "UW1"
df.iloc[1,4] = "UW2"
df.iloc[1,5] = "UW3"
df.iloc[1,8] = "Final_Price"
df.iloc[1,9] = "Lot_Haka1"
df.iloc[1,10] = "Haka1_Price"
df.iloc[1,11] = "Lot_Haka2"
df.iloc[1,12] = "Haka2_Price"
df.iloc[1,13] = "Allotment"
df.iloc[1,14] = "Sell_Price"
df.iloc[1,15] = "Profit"
df.iloc[1,16] = "Profit_Margin"
df.columns = df.iloc[1,:]
df = df.iloc[2:,1:17]
df["Ticker"] = df["Ticker"].fillna("~")
df["Date"] = df["Date"].fillna("~")
df["UW1"] = df["UW1"].fillna("~")
df["UW2"] = df["UW2"].fillna("~")
df["UW3"] = df["UW3"].fillna("~")
df = df[df["Ticker"]!="~"].fillna(0)

df = df.replace("Rp","",regex=True)
kolom = list(df.columns)
kolom = kolom[9:13]

for i in kolom:
  df[i] = df[i].replace(".","",regex=True)
  df[i] = df[i].astype('int')

try:
  conn = sqlite3.connect('database')
  c = conn.cursor()
  print("Connect Successfully")
except:
  print("Connection Error")

  
create = "CREATE TABLE IF NOT EXISTS saham(No INTEGER,Ticker TEXT,Date DATETIME,UW1 TEXT,UW2 TEXT,UW3 TEXT,Sektor TEXT,Papan TEXT,Final_Price TEXT,Lot_Haka1 INTEGER,Haka1_Price INTEGER,Lot_Haka2 INTEGER,Haka2_Price INTEGER,Allotment INT,Sell_Price INTEGER,Profit TEXT,Profit_Margin TEXT)"

c.execute(create)
conn.commit()

df.to_sql('saham',conn,if_exists="replace",index=True)

select = """
  SELECT * FROM saham
"""

c.execute(select)

for row in c.fetchall():
   print(row)