import psycopg2 as psycopg
import os
from datetime import datetime
from HelperFunctions import  epoch_to_date, table_creation, insert_into_stm_stop_line_tables, fetch_and_create_json_stm_response_json,epoch_to_timestamp, french_english_color_mapping
import json
from dotenv import load_dotenv

load_dotenv()
POSTGRES_PASS = os.getenv("POSTGRES_PASS")

connection = psycopg.connect(
    host="localhost",
    dbname="SOEN-363-Project",
    user="postgres",
    password=POSTGRES_PASS,
    port=5432
)
cursor = connection.cursor()

table_creation()
insert_into_stm_stop_line_tables(cursor)

# Fetch and save response for version 2 of the service status API, as well as live location data into corresponding JSON files
fetch_and_create_json_stm_response_json("https://api.stm.info/pub/od/i3/v2/messages/etatservice") # --> Hardcoding the stm_response_v2_orange_line_down.json file
fetch_and_create_json_stm_response_json("https://api.stm.info/pub/od/gtfs-rt/ic/v2/tripUpdates")

trip_id_set = set()
live_trip_stop_id_set = set()

with open('stm_response_v2_orange_line_down.json', 'r') as file:
    stm_bus_stop_cancelled_moved_relocated_data = json.load(file)

    stm_bus_stop_cancelled_moved_relocated_id = 1
    for record in stm_bus_stop_cancelled_moved_relocated_data.get("alerts"):

        description_texts = record.get("description_texts", [])
        informed_entities = record.get("informed_entities", [])
        active_periods = record.get("active_periods", [])

        if len(description_texts) > 1 and ("annulés" in description_texts[0].get("text") or "cancelled" in description_texts[1].get("text")) and len(informed_entities) == 3:
            stop_code = informed_entities[2].get("stop_code")
            reason = description_texts[1].get("text")

            if active_periods and active_periods.get("start") is not None:
                time_of_cancellation = epoch_to_date(active_periods.get("start"))

                cursor.execute("SELECT stm_bus_stop_id FROM stm_bus_stop WHERE stm_bus_stop_code = %s", (stop_code,))
                result = cursor.fetchone()
                if result:
                    stm_bus_stop_id = result[0]
                    cursor.execute(
                        "INSERT INTO stm_bus_stop_cancelled_moved_relocated (stm_bus_stop_cancelled_moved_relocated_id, stm_bus_stop_id, stm_bus_stop_code, stm_bus_stop_cancelled_moved_relocated_date, stm_bus_stop_cancelled_moved_relocated_reason) VALUES (%s, %s, %s, %s, %s)",
                        (stm_bus_stop_cancelled_moved_relocated_id, stm_bus_stop_id, stop_code, time_of_cancellation, reason)
                    )
                    stm_bus_stop_cancelled_moved_relocated_id += 1
                connection.commit()
    print("Populated stm_bus_stop_cancelled_moved_relocated table")

with open('stm_live_trip_dates.txt', 'r') as date_file:
    filenames = date_file.read().splitlines()
    live_stm_bus_trip_id = 1
for filename in filenames:
    if filename == '':
        continue
    with open(filename, 'r') as file:
        stm_response_trips = json.load(file)

        skipped = 0
        for record in stm_response_trips.get("entity", []):
            trip_id = record.get("id")
            if not trip_id:
                continue
            if trip_id in trip_id_set:
                continue
            trip_id_set.add(trip_id)


            trip_update = record.get("tripUpdate", {})

            trip = trip_update.get("trip", {})
            stop_time_updates = trip_update.get("stopTimeUpdate", [])
            time_of_record = trip_update.get("timestamp")

            trip_id = trip.get("tripId")
            if not trip_id:
                continue

            cursor.execute("SELECT stm_bus_trip_id FROM stm_bus_trip WHERE stm_bus_trip_id = %s", (trip_id,))
            result_trip_id = cursor.fetchone()

            if not result_trip_id:
                continue

            combined_date = trip.get("startDate") 
            combined_date_str = str(combined_date)
            year = int(combined_date_str[:4])
            month = int(combined_date_str[4:6])
            day = int(combined_date_str[6:])
            trip_date = datetime(year, month, day)
            
            schedule_relationship = trip.get("scheduleRelationship") # Either scheduled or canceled

            insert_query = "INSERT INTO live_stm_bus_trip (live_stm_bus_trip_id, stm_bus_trip_id, live_stm_bus_trip_date) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (live_stm_bus_trip_id, trip_id, trip_date))

            for stop in stop_time_updates:
                stop_sequence = stop.get("stopSequence")
                arrival_time = stop.get("arrival", {}).get("time")
                departure_time = stop.get("departure", {}).get("time")
                schedule_relationship = stop.get("scheduleRelationship")

                stop_id = stop.get("stopId")
                if not stop_id:
                    skipped += 1
                    continue
                if stop_id in live_trip_stop_id_set:
                    skipped += 1
                    continue
                live_trip_stop_id_set.add(stop_id)
                cursor.execute("SELECT stm_bus_stop_id FROM stm_bus_stop WHERE stm_bus_stop_id = %s", (stop_id,))
                result_route_id = cursor.fetchone()

                if not result_route_id:
                    skipped += 1
                    continue

                arrival = stop.get("arrival", {})
                departure = stop.get("departure", {})
                arrival_time = epoch_to_timestamp(arrival.get("time")) if arrival.get("time") else None
                departure_time = epoch_to_timestamp(departure.get("time")) if departure.get("time") else None
                if not arrival_time or not departure_time:
                    continue

                insert_query = "INSERT INTO live_stm_bus_trip_stop (live_stm_bus_trip_stop_id, live_stm_bus_trip_id, stm_bus_stop_id, live_stm_bus_stop_arrival_time, live_stm_bus_stop_departure_time, live_stm_bus_trip_stop_sequence, live_stm_bus_trip_stop_schedule_relationship) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, (trip_id, trip_id, stop_id, arrival_time, departure_time, stop_sequence, schedule_relationship))
            
            live_stm_bus_trip_id += 1   

        connection.commit()
        print("Skipped " + str(skipped) + " records")
    print("Populated live_stm_bus_trip and live_stm_bus_trip_stop tables")

connection.close()