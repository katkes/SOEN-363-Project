import requests
import json
from google.protobuf.json_format import MessageToJson
import gtfs_pb2 
from Creds import connection, mtaBusApiKey

cursor = connection.cursor()

mtaTripUpdatesApiUrl = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace"
mtaBusTripPositionResponse = requests.get(mtaTripUpdatesApiUrl)
if mtaBusTripPositionResponse.status_code == 200:
    try:
        # Parse the Protobuf data from the response content
        trip_updates = gtfs_pb2.FeedMessage()
        trip_updates.ParseFromString(mtaBusTripPositionResponse.content)
        
        # Convert the Protobuf message to JSON
        json_trip_updates = MessageToJson(trip_updates)
        
        # Write the JSON data to mta_response_trips.json
        with open('mta_response_trips.json', 'w') as json_file:
            json.dump(json.loads(json_trip_updates), json_file, indent=4)
        
        print("Protobuf response has been written to mta_response_trips.json")
    except Exception as e:
        print(f"Error: {e}")
else:
    print(f"Error: Received status code {mtaBusTripPositionResponse.status_code} for URL {mtaBusTripPositionResponse}")
    print(mtaBusTripPositionResponse.text)

mtaBusTripPositionApiUrl = "https://gtfsrt.prod.obanyc.com/vehiclePositions?key=" + mtaBusApiKey
mtaBusTripPositionResponse = requests.get(mtaBusTripPositionApiUrl)
if mtaBusTripPositionResponse.status_code == 200:
    try:
        # Parse the Protobuf data from the response content
        trip_updates = gtfs_pb2.FeedMessage()
        trip_updates.ParseFromString(mtaBusTripPositionResponse.content)
        
        # Convert the Protobuf message to JSON
        json_trip_updates = MessageToJson(trip_updates)
        
        # Write the JSON data to mta_bus_position_response_trips.json
        with open('mta_bus_position_response_trips.json', 'w') as json_file:
            json.dump(json.loads(json_trip_updates), json_file, indent=4)
        
        print("Protobuf response has been written to mta_bus_position_response_trips.json")
    except Exception as e:
        print(f"Error: {e}")
else:
    print(f"Error: Received status code {mtaBusTripPositionResponse.status_code} for URL {mtaBusTripPositionResponse}")
    print(mtaBusTripPositionResponse.text)