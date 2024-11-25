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

with open('ConstantInformation/gtfs_stm/stop_times.txt', mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        stop_time_id = 1
        skipped = 0
        for row in csv_reader:
            print(row)
            print("")
            trip_id = row['trip_id']
            stop_id = row['stop_id']
            stop_sequence = row['stop_sequence']
            arrival_time = normalize_time(row['arrival_time'])
            departure_time = normalize_time(row['departure_time'])
            print("Arrival Time: ", arrival_time)
            print("Departure Time: ", departure_time)
            if arrival_time is None or departure_time is None:
                skipped += 1
                print("Skipped: ", skipped)
                continue # TODO: fix overflow of time, currently ignoring invalid time entries

            cursor.execute("SELECT stm_bus_trip_id FROM stm_bus_trip WHERE stm_bus_trip_id = %s", (trip_id, ))
            result_trip = cursor.fetchone()
            
            cursor.execute("SELECT stm_bus_stop_id FROM stm_bus_stop WHERE stm_bus_stop_code = %s", (stop_id, ))
            result_stop = cursor.fetchone()

            print("Trip" + str(result_trip))

            if result_trip and result_stop:
                insert_query = "INSERT INTO stm_bus_stop_time (stm_bus_stop_time_id, stm_bus_stop_time_trip_id, stm_bus_stop_time_stop_id, stm_bus_stop_time_stop_sequence, stm_bus_stop_arrival_time, stm_bus_stop_departure_time) VALUES (%s, %s, %s, %s, %s, %s);"
            else:
                insert_query = "INSERT INTO stm_metro_stop_time (stm_metro_stop_time_id, stm_metro_stop_time_trip_id, stm_metro_stop_time_stop_id, stm_metro_stop_time_stop_sequence, stm_metro_stop_arrival_time, stm_metro_stop_departure_time) VALUES (%s, %s, %s, %s, %s, %s);"

            cursor.execute(insert_query, (stop_time_id, trip_id, stop_id, stop_sequence, arrival_time, departure_time))
            stop_time_id += 1
        connection.commit()

print("Populated stm_bus_stop_time table")
print("Skipped: ", skipped)