# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 21:19:52 2015

@author: Administrator
"""

import datetime
import requests
import sqlite3 as lite

url = 'https://api.forecast.io/forecast/'

cities = {
    "Boston": '42.331960, -71.020173',
    "Seattle": '47.620499, -122.350876',
    "Miami": '25.775163, -80.208615',
    "Cleveland": '41.478462, -81.679435',
    "Nashville": '36.171800, -86.785002'
}

api_key = 'cfc6c7845bf3bab98a881bc32987677a'

con = lite.connect('weather.db')
cur = con.cursor()

with con:
    cur.execute("DROP TABLE IF EXISTS daily_temp")
    cur.execute(
        """CREATE TABLE daily_temp (
                query_time INT,
                Boston REAL,
                Seattle REAL,
                Miami REAL,
                Cleveland REAL,
                Nashville REAL);"""
    )
    
for i in range(30):
    query_time = int(((datetime.datetime.now() - datetime.timedelta(days=i)) - datetime.datetime(1970,1,1)).total_seconds())
    #print query_time
    with con:
        cur.execute("INSERT INTO daily_temp(query_time) VALUES (?)", (query_time,))
     
    for city, loc in cities.items():
        api_call = url + api_key + '/' + loc + ',' + str(query_time)

        r = requests.get(api_call)
        max_temp = r.json()['daily']['data'][0]['temperatureMax']
        
        with con:
            cur.execute(
                "UPDATE daily_temp SET " + city + " = " + str(max_temp) + " " +
                "WHERE query_time = " + str(query_time)
            )    