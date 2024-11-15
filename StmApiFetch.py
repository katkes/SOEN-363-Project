import requests
import psycopg2
import json
from google.protobuf.json_format import MessageToJson
import gtfs_pb2 

connection = psycopg2.connect(host="localhost", dbname="SOEN-363-Project", user="postgres", password="1234", port=5432)
cursor = connection.cursor()

stmHeaders = {
    "accept": "application/json",
    "apiKey": "l78e91cc66e0c54b5cbddbf53eefc45120"
}

# Fetch and save response for version 1
serviceStatusApiUrlV1 = "https://api.stm.info/pub/od/i3/v1/messages/etatservice"
stmServiceStatusResponseV1 = requests.get(serviceStatusApiUrlV1, headers=stmHeaders)
if stmServiceStatusResponseV1.status_code == 200:
    stmResponseV1 = stmServiceStatusResponseV1.json()
    with open('stm_response_v1.json', 'w') as json_file:
        json.dump(stmResponseV1, json_file, indent=4)
        print("Json response has been written to stm_response_v1.json")
else:
    print(f"Error: Received status code {stmServiceStatusResponseV1.status_code} for URL {serviceStatusApiUrlV1}")

# Fetch and save response for version 2
serviceStatusApiUrlV2 = "https://api.stm.info/pub/od/i3/v2/messages/etatservice"
stmServiceStatusResponseV2 = requests.get(serviceStatusApiUrlV2, headers=stmHeaders)
if stmServiceStatusResponseV2.status_code == 200:
    stmResponseV2 = stmServiceStatusResponseV2.json()
    with open('stm_response_v2.json', 'w') as json_file:
        json.dump(stmResponseV2, json_file, indent=4)
        print("Json response has been written to stm_response_v2.json")
else:
    print(f"Error: Received status code {stmServiceStatusResponseV2.status_code} for URL {serviceStatusApiUrlV2}")

stmMetroNumbers = {1: "Green", 2: "Orange", 4: "Yellow", 5: "Blue"}

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