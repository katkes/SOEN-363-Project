import requests
import psycopg2
import json
from google.protobuf.json_format import MessageToJson
import gtfs_pb2 
import csv

connection = psycopg2.connect(
    host="localhost",
    dbname="SOEN-363-Project",
    user="postgres",
    password="1234",
    port=5432
)
cursor = connection.cursor()

stmHeaders = {
    "accept": "application/json",
    "apiKey": "l78e91cc66e0c54b5cbddbf53eefc45120"
}



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

for record in stmServiceStatusResponseV2.json():
    print(record)

if stmServiceStatusResponseV2.status_code == 200:
    stmResponseV2 = stmServiceStatusResponseV2.json()
    with open('stm_response_v2.json', 'w') as json_file:
        json.dump(stmResponseV2, json_file, indent=4)
        print("Json response has been written to stm_response_v2.json")
else:
    print(f"Error: Received status code {stmServiceStatusResponseV2.status_code} for URL {serviceStatusApiUrlV2}")

# stmMetroNumbers = {1: "Green", 2: "Orange", 4: "Yellow", 5: "Blue"}

# # Fetch and save trip updates
# stmTripUpdatesApiUrl = "https://api.stm.info/pub/od/gtfs-rt/ic/v2/tripUpdates"
# stmTripUpdatesResponse = requests.get(stmTripUpdatesApiUrl, headers=stmHeaders)
# if stmTripUpdatesResponse.status_code == 200:
#     try:
#         # Parse the Protobuf data from the response content
#         trip_updates = gtfs_pb2.FeedMessage()
#         trip_updates.ParseFromString(stmTripUpdatesResponse.content)
        
#         # Convert the Protobuf message to JSON
#         json_trip_updates = MessageToJson(trip_updates)
        
#         # Write the JSON data to stm_response_trips.json
#         with open('stm_response_trips.json', 'w') as json_file:
#             json.dump(json.loads(json_trip_updates), json_file, indent=4)
        
#         print("Protobuf response has been written to stm_response_trips.json")
#     except Exception as e:
#         print(f"Error: {e}")
# else:
#     print(f"Error: Received status code {stmTripUpdatesResponse.status_code} for URL {stmTripUpdatesApiUrl}")
#     print(stmTripUpdatesResponse.text)



# Create table for routes
create_table_query = """
CREATE TABLE IF NOT EXISTS stm_metro_line(
    stm_metro_line_id INT PRIMARY KEY,
    line_name VARCHAR(255),
    line_number INT
);

CREATE TABLE IF NOT EXISTS stm_bus_line(
    stm_bus_line_id INT PRIMARY KEY,
    line_name VARCHAR(255),
    line_number INT
);

CREATE TABLE IF NOT EXISTS stm_bus_stop(
    stm_bus_stop_id VARCHAR(15) PRIMARY KEY,
    stm_bus_top_name VARCHAR(255),
    stm_bus_stop_code INT
);

CREATE TABLE IF NOT EXISTS stm_metro_stop(
    stm_metro_stop_id VARCHAR(15) PRIMARY KEY,
    stm_metro_stop_name VARCHAR(255),
    stm_metro_stop_code INT
);
"""
cursor.execute(create_table_query)
connection.commit()

def extract_line_name(line_string):
    parts = line_string.split(" - ")
    if len(parts) > 1:
        return parts[1]
    else:
        return parts[0]

# Insert data into stm_metro_line and stm_bus_line tables
with open('gtfs_stm/routes.txt', mode='r', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        line_name = extract_line_name(row['route_long_name'])
        if "Ligne" in row['route_long_name']:
            insert_query = "INSERT INTO stm_metro_line (stm_metro_line_id, line_name, line_number) VALUES (%s, %s, %s);"
            cursor.execute(insert_query, (row['route_id'], line_name, row['route_id']))
        else:
            insert_query = "INSERT INTO stm_bus_line (stm_bus_line_id, line_name, line_number) VALUES (%s, %s, %s);"
            cursor.execute(insert_query, (row['route_id'], line_name, row['route_id']))

#Insert data into stm_metro_stop and stm_bus_stop tables
with open('gtfs_stm/stops.txt', mode='r', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        print(row['stop_id'])
        if "STATION" in row['stop_name']:
            insert_query = "INSERT INTO stm_metro_stop (stm_metro_stop_id, stm_metro_stop_name, stm_metro_stop_code) VALUES (%s, %s, %s);"
            cursor.execute(insert_query, (row['stop_id'], row['stop_name'], row['stop_code']))
        else: 
            insert_query = "INSERT INTO stm_bus_stop (stm_bus_stop_id, stm_bus_top_name, stm_bus_stop_code) VALUES (%s, %s, %s);"
            cursor.execute(insert_query, (row['stop_id'], row['stop_name'], row['stop_code']))

connection.commit()



cursor.close()
connection.close()