#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 14:34:19 2022

referensi :
https://www.codegrepper.com/code-examples/sql/write+pandas+dataframe+to+postgresql+table+psycopg2
"""

# Write pandas df into postgres table
import psycopg2
import psycopg2.extras as extras
import pandas as pd
from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

import requests
from bs4 import BeautifulSoup
    
def executor():   
    def execute_values(conn, df, table):  
        tuples = [tuple(x) for x in df.to_numpy()]  
        cols = ','.join(list(df.columns))
        # SQL query to execute
        query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
        cursor = conn.cursor()
        try:
            extras.execute_values(cursor, query, tuples)
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            conn.rollback()
            cursor.close()
            return 1
        print("the dataframe is inserted")
        cursor.close()  
      
    conn = psycopg2.connect(
        database="scrap_hukumonline", user='postgres', password='postgres', host='127.0.0.1', port='5432'
    )
    
    
    judul = []
    link = []
    kategori = []
    berita = []
    tanggal = []

    
    for x in range(1,2):
        website = f'https://www.hukumonline.com/klinik/arsip/page/{x}/'
        r = requests.get(website)
        soup = BeautifulSoup(r.content,'html.parser')
        for i in soup.find_all('div',class_='klinik-list d-flex flex-column divider-bottom my-3'):
            for a in i.find_all('a',href=True,limit=1):
                print("Judul : ",i.h2.text)
                print('Link : https://www.hukumonline.com',a['href'])
                site = 'https://www.hukumonline.com' + a['href']
                m = requests.get(site)
                soup2 = BeautifulSoup(m.content,'html.parser')

                dummy_berita = []
                for j in soup2.find_all('p'): 
                    dummy_berita.append(j.text)
                judul.append(i.h2.text)
                link.append(a['href'])
                berita.append(dummy_berita)
                for x in i.find_all('a',href=True,limit=2)[1::1]:
                    # print("Category : ",x.text)
                    kategori.append(x.text)
                for y in i.find_all('span',class_="small text-muted mr-1"):
                    # print("Tanggal : ",y.text)
                    tanggal.append(y.text)
                #Penulisnya belom dibuat
                # print("\n")
    
    df = pd.DataFrame(judul)
    df.rename(columns={0:"Judul"},inplace=True)
    # df["Link"] = link_new
    # df["Berita"] =  berita
    
    df["Category"] = kategori
    now= datetime.now()
    df["exec_time"] = str(now)
    df = df.fillna("-")
    
    
    return (execute_values(conn, df, 'scrap_berita'))
    
dag = DAG('testcon', description='Load to Postgres',
          schedule_interval='0 * * * *',
          start_date=datetime(2022, 7, 25), catchup=False)

dummy_operator = DummyOperator(task_id='dummy_task', retries=3, dag=dag)

postgres_operator = PythonOperator(task_id='postgres_task', python_callable=executor, dag=dag)

dummy_operator >> postgres_operator
