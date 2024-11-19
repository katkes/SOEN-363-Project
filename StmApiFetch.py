import requests
import json
from google.protobuf.json_format import MessageToJson
import gtfs_pb2 
import csv
from HelperFunctions import extract_line_name, epoch_to_date, table_creation, french_english_color_mapping
from Creds import connection, stmHeaders

cursor = connection.cursor()
table_creation()

# Insert data into stm_metro_line and stm_bus_line tables
with open('ConstantInformation/gtfs_stm/routes.txt', mode='r', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        line_name = extract_line_name(row['route_long_name'])
        if "Ligne" in row['route_long_name']:
            color_name = french_english_color_mapping.get(line_name, line_name)
            insert_query = "INSERT INTO stm_metro_line (stm_metro_line_id, line_colour, line_number) VALUES (%s, %s, %s);"
            cursor.execute(insert_query, (row['route_id'], color_name, row['route_id']))
        else:
            insert_query = "INSERT INTO stm_bus_line (stm_bus_line_id, line_name, line_number) VALUES (%s, %s, %s);"
            cursor.execute(insert_query, (row['route_id'], line_name, row['route_id']))

#Insert data into stm_metro_stop and stm_bus_stop tables
with open('ConstantInformation/gtfs_stm/stops.txt', mode='r', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if "STATION" in row['stop_name']:
            insert_query = "INSERT INTO stm_metro_stop (stm_metro_stop_id, stm_metro_stop_name, stm_metro_stop_code) VALUES (%s, %s, %s);"
            cursor.execute(insert_query, (row['stop_id'], row['stop_name'], row['stop_code']))
        else: 
            insert_query = "INSERT INTO stm_bus_stop (stm_bus_stop_id, stm_bus_stop_name, stm_bus_stop_code) VALUES (%s, %s, %s);"
            cursor.execute(insert_query, (row['stop_id'], row['stop_name'], row['stop_code']))

connection.commit()


# # Fetch and save response for version 1
# serviceStatusApiUrlV1 = "https://api.stm.info/pub/od/i3/v1/messages/etatservice"
# stmServiceStatusResponseV1 = requests.get(serviceStatusApiUrlV1, headers=stmHeaders)
# if stmServiceStatusResponseV1.status_code == 200:
#     stmResponseV1 = stmServiceStatusResponseV1.json()
#     with open('stm_response_v1.json', 'w') as json_file:
#         json.dump(stmResponseV1, json_file, indent=4)
#         print("Json response has been written to stm_response_v1.json")
# else:
#     print(f"Error: Received status code {stmServiceStatusResponseV1.status_code} for URL {serviceStatusApiUrlV1}")

# Fetch and save response for version 2
serviceStatusApiUrlV2 = "https://api.stm.info/pub/od/i3/v2/messages/etatservice"
stmServiceStatusResponseV2 = requests.get(serviceStatusApiUrlV2, headers=stmHeaders)

stm_bus_stop_cancelled_moved_relocated_id = 1

for record in stmServiceStatusResponseV2.json().get("alerts"):

    description_texts = record.get("description_texts", [])
    informed_entities = record.get("informed_entities", [])
    active_periods = record.get("active_periods", [])
    print(description_texts)

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

        # print(record.get("active_periods").get("start"))
        # print(record.get("active_periods"))
        # time_of_cancellation = epoch_to_date(record.get("active_periods").get("start"))
        # print(time_of_cancellation)


        # cursor.execute("SELECT stm_bus_stop_id FROM stm_bus_stop WHERE stm_bus_stop_code = %s", (stop_code,))
        # result = cursor.fetchone()
        # if result:
        #     stm_bus_stop_id = result[0]

        # cursor.execute(
        #             "INSERT INTO stm_bus_stop_cancelled_moved_relocated (stm_bus_stop_cancelled_moved_relocated_id, stm_bus_stop_id, stm_bus_stop_code, stm_bus_stop_cancelled_moved_relocated_date, stm_bus_stop_cancelled_moved_relocated_reason) VALUES (%s, %s, %s, %s, %s)",
        #             (stm_bus_stop_cancelled_moved_relocated_id, stm_bus_stop_id, stop_code, time_of_cancellation, reason)
        #         )
        # stm_bus_stop_cancelled_moved_relocated_id += 1


# if stmServiceStatusResponseV2.status_code == 200:
#     stmResponseV2 = stmServiceStatusResponseV2.json()
#     with open('stm_response_v2.json', 'w') as json_file:
#         json.dump(stmResponseV2, json_file, indent=4)
#         print("Json response has been written to stm_response_v2.json")
# else:
#     print(f"Error: Received status code {stmServiceStatusResponseV2.status_code} for URL {serviceStatusApiUrlV2}")

# Fetch and save trip updates
stmTripUpdatesApiUrl = "https://api.stm.info/pub/od/gtfs-rt/ic/v2/tripUpdates"
stmTripUpdatesResponse = requests.get(stmTripUpdatesApiUrl, headers=stmHeaders)
if stmTripUpdatesResponse.status_code == 200:
    try:
        # Parse the Protobuf data from the response content
        trip_updates = gtfs_pb2.FeedMessage()
        trip_updates.ParseFromString(stmTripUpdatesResponse.content)
        
        # Convert the Protobuf message to JSON
        json_trip_updates = MessageToJson(trip_updates)
        
        # Write the JSON data to stm_response_trips.json
        with open('stm_response_trips.json', 'w') as json_file:
            json.dump(json.loads(json_trip_updates), json_file, indent=4)
        
        print("Protobuf response has been written to stm_response_trips.json")
    except Exception as e:
        print(f"Error: {e}")
else:
    print(f"Error: Received status code {stmTripUpdatesResponse.status_code} for URL {stmTripUpdatesApiUrl}")
    print(stmTripUpdatesResponse.text)


cursor.close()
connection.close()