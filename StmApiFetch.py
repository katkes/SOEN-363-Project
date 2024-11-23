import requests
from HelperFunctions import  epoch_to_date, table_creation, insert_into_stm_stop_line_tables, fetch_and_create_json_stm_response_json, french_english_color_mapping
from Creds import connection, stmHeaders
import json

cursor = connection.cursor()

# table_creation()
# insert_into_stm_stop_line_tables(cursor)

# Fetch and save response for version 1 and 2 of the service status API, as well as live location data into corresponding JSON files
# TODO: Look into why this doesn't work anymore 
# fetch_and_create_json_stm_response_json("https://api.stm.info/pub/od/i3/v1/messages/etatservice")
# fetch_and_create_json_stm_response_json("https://api.stm.info/pub/od/i3/v2/messages/etatservice")
# fetch_and_create_json_stm_response_json("https://api.stm.info/pub/od/gtfs-rt/ic/v2/tripUpdates")

# serviceStatusApiUrlV2 = "https://api.stm.info/pub/od/i3/v2/messages/etatservice"
# stmServiceStatusResponseV2 = requests.get(serviceStatusApiUrlV2, headers=stmHeaders)

# stm_bus_stop_cancelled_moved_relocated_id = 1
# for record in stmServiceStatusResponseV2.json().get("alerts"):

#     description_texts = record.get("description_texts", [])
#     informed_entities = record.get("informed_entities", [])
#     active_periods = record.get("active_periods", [])
#     print(description_texts)

#     if len(description_texts) > 1 and ("annulés" in description_texts[0].get("text") or "cancelled" in description_texts[1].get("text")) and len(informed_entities) == 3:
#         stop_code = informed_entities[2].get("stop_code")
#         reason = description_texts[1].get("text")

#         if active_periods and active_periods.get("start") is not None:
#             time_of_cancellation = epoch_to_date(active_periods.get("start"))

#             cursor.execute("SELECT stm_bus_stop_id FROM stm_bus_stop WHERE stm_bus_stop_code = %s", (stop_code,))
#             result = cursor.fetchone()
#             if result:
#                 stm_bus_stop_id = result[0]

#                 cursor.execute(
#                     "INSERT INTO stm_bus_stop_cancelled_moved_relocated (stm_bus_stop_cancelled_moved_relocated_id, stm_bus_stop_id, stm_bus_stop_code, stm_bus_stop_cancelled_moved_relocated_date, stm_bus_stop_cancelled_moved_relocated_reason) VALUES (%s, %s, %s, %s, %s)",
#                     (stm_bus_stop_cancelled_moved_relocated_id, stm_bus_stop_id, stop_code, time_of_cancellation, reason)
#                 )
#                 stm_bus_stop_cancelled_moved_relocated_id += 1
#             connection.commit()

# TODO: Implement real-time data database implementation
with open('stm_response_trips.json', 'r') as file:
    stm_response_trips = json.load(file)
    print("hello")

    live_trip_id = 1
    for record in stm_response_trips.get("entity", []):

        trip_update = record.get("tripUpdate", {})

        trip = trip_update.get("trip", {})
        stop_time_updates = trip_update.get("stopTimeUpdate", [])
        time_of_record = trip_update.get("timestamp")

        trip_id = trip.get("trip_id")
        start_date = epoch_to_date(trip.get("startDate"))
        schedule_relationship = trip.get("scheduleRelationship") # Either scheduled or canceled
        route_id = trip.get("routeId")

        for stop in stop_time_updates:
            stop_sequence = stop.get("stopSequence")
            arrival_time = stop.get("arrival", {}).get("time")
            departure_time = stop.get("departure", {}).get("time")



            stop_id = stop.get("stopId")
            arrival = stop.get("arrival", {})
            departure = stop.get("departure", {})
            arrival_time = epoch_to_date(arrival.get("time")) if arrival.get("time") else None
            departure_time = epoch_to_date(departure.get("time")) if departure.get("time") else None

            # print(f"Trip ID: {trip_id}, Stop ID: {stop_id}, Arrival Time: {arrival_time}, Departure Time: {departure_time}")


        # print(len(record))
        # print(record)
        live_trip_update = record.get("tripUpdate", {})
        trip_id = live_trip_update.get("trip", {}).get("trip_id")

        # print(live_trip_update)

        
        trip_id = trip_update.get("trip", {}).get("trip_id")
        stop_time_updates = trip_update.get("stopTimeUpdate", [])
        
        if not stop_time_updates:
            continue

        for stop_time_update in stop_time_updates:
            stop_id = stop_time_update.get("stop_id")
            arrival = stop_time_update.get("arrival", {})
            departure = stop_time_update.get("departure", {})
            arrival_time = epoch_to_date(arrival.get("time")) if arrival.get("time") else None
            departure_time = epoch_to_date(departure.get("time")) if departure.get("time") else None

            # print(f"Trip ID: {trip_id}, Stop ID: {stop_id}, Arrival Time: {arrival_time}, Departure Time: {departure_time}")
