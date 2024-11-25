from datetime import datetime
from Creds import connection, stmHeaders
from google.protobuf.json_format import MessageToJson
import csv
import requests
import json
import gtfs_pb2
import os
from HelperFunctions import normalize_time

cursor = connection.cursor()

with open('ConstantInformation/gtfs_mta/stop_times.txt', mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        stop_time_id = 1
        for row in csv_reader:
            trip_id = row['trip_id']
            stop_id = row['stop_id']
            stop_sequence = row['stop_sequence']
            arrival_time = normalize_time(row['arrival_time'])
            departure_time = normalize_time(row['departure_time'])

            insert_query = "INSERT INTO mta_metro_stop_time (mta_metro_stop_time_id, mta_metro_stop_time_trip_id, mta_metro_stop_time_stop_id, mta_metro_stop_time_stop_sequence, mta_metro_stop_arrival_time, mta_metro_stop_departure_time) VALUES (%s, %s, %s, %s, %s, %s);"
            cursor.execute(insert_query, (stop_time_id, trip_id, stop_id, stop_sequence, arrival_time, departure_time))
            connection.commit()
            print("Added record number ", stop_time_id)
            stop_time_id += 1
            
print("Data inserted into mta_metro_stop_time table")