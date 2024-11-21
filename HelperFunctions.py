from datetime import datetime
from Creds import connection, stmHeaders
from google.protobuf.json_format import MessageToJson
import csv
import requests
import json
import gtfs_pb2

day_of_week_mapping = {
    "Lundi": "Monday",
    "Mardi": "Tuesday",
    "Mercredi": "Wednesday",
    "Jeudi": "Thursday",
    "Vendredi": "Friday",
    "Samedi": "Saturday",
    "Dimanche": "Sunday"
}

french_english_color_mapping = {
    "Verte": "Green",
    "Orange": "Orange",
    "Jaune": "Yellow",
    "Bleue": "Blue"
}

stm_metro_line = {
    "Ligne verte": 1, 
    "Ligne orange": 2, 
    "Ligne jaune":4, 
    "Ligne bleue":5
}

def table_creation():
    cursor = connection.cursor()
    create_table_query = """
    CREATE DOMAIN planned_kilometerage AS INT CHECK (VALUE >= 0);
    CREATE DOMAIN realized_kilometerage AS INT CHECK (VALUE >= 0);

    CREATE TYPE day_of_week AS ENUM ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');
    CREATE TYPE metro_colour AS ENUM ('Green', 'Orange', 'Yellow', 'Blue');

    CREATE TABLE IF NOT EXISTS stm_metro_line(
        stm_metro_line_id INT PRIMARY KEY,
        line_colour metro_colour NOT NULL,
        line_number INT NOT NULL CHECK (line_number > 0)
    );

    CREATE TABLE IF NOT EXISTS stm_bus_line(
        stm_bus_line_id INT PRIMARY KEY,
        line_name VARCHAR(255) NOT NULL,
        line_number INT NOT NULL CHECK (line_number > 0)
    );

    CREATE TABLE IF NOT EXISTS stm_bus_stop(
        stm_bus_stop_id VARCHAR(15) PRIMARY KEY,
        stm_bus_stop_name VARCHAR(255) NOT NULL,
        stm_bus_stop_code INT NOT NULL CHECK (stm_bus_stop_code > 0),
        is_active BOOLEAN DEFAULT TRUE
    );

    CREATE TABLE IF NOT EXISTS stm_bus_stop_cancelled_moved_relocated(
        stm_bus_stop_cancelled_moved_relocated_id INT PRIMARY KEY,
        stm_bus_stop_id VARCHAR(15) NOT NULL,
        stm_bus_stop_code INT NOT NULL CHECK (stm_bus_stop_code > 0),
        stm_bus_stop_cancelled_moved_relocated_date DATE NOT NULL,
        stm_bus_stop_cancelled_moved_relocated_reason VARCHAR(255) NOT NULL,
        FOREIGN KEY (stm_bus_stop_id) REFERENCES stm_bus_stop(stm_bus_stop_id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS stm_metro_stop(
        stm_metro_stop_id VARCHAR(15) PRIMARY KEY,
        stm_metro_stop_name VARCHAR(255) NOT NULL,
        stm_metro_stop_code INT NOT NULL CHECK (stm_metro_stop_code > 0)
    );

    CREATE TABLE IF NOT EXISTS stm_metro_planned_kilometerage (
        stm_metro_planned_kilometerage_id INT PRIMARY KEY,
        stm_metro_line_id INT NOT NULL,
        planned_kilometerage planned_kilometerage NOT NULL,
        day_of_week day_of_week NOT NULL,
        stm_metro_planned_kilometerage_date DATE NOT NULL,
        FOREIGN KEY (stm_metro_line_id) REFERENCES stm_metro_line(stm_metro_line_id)
    );

    CREATE TABLE IF NOT EXISTS stm_metro_realized_kilometrage (
        stm_metro_realized_kilometrage_id INT PRIMARY KEY,
        stm_metro_line_id INT NOT NULL,
        realized_kilometerage realized_kilometerage NOT NULL,
        day_of_week_or_type_of_day VARCHAR(25) NOT NULL,
        stm_metro_realized_kilometrage_date DATE NOT NULL,
        FOREIGN KEY (stm_metro_line_id) REFERENCES stm_metro_line(stm_metro_line_id)
    );

    CREATE TABLE IF NOT EXISTS stm_incident(
        stm_incident_id INT PRIMARY KEY,
        stm_incident_type VARCHAR(255) NOT NULL,
        stm_incident_primary_cause VARCHAR(255) NOT NULL,
        stm_incident_secondary_cause VARCHAR(255),
        stm_incident_time_of_incident TIME NOT NULL,
        stm_incident_time_of_resolution TIME,
        stm_incident_date_of_incident DATE NOT NULL,
        stm_incident_location_of_incident VARCHAR(255) NOT NULL,
        stm_metro_line_id INT NOT NULL,
        FOREIGN KEY (stm_metro_line_id) REFERENCES stm_metro_line(stm_metro_line_id)
    );

    -- View for a low key access to the stm_incident table, only showing incidents from the last year
    CREATE VIEW low_key_access_stm_incident AS
    SELECT stm_incident_id, stm_incident_type, stm_incident_date_of_incident, stm_incident_location_of_incident
    FROM stm_incident
    WHERE stm_incident_date_of_incident >= CURRENT_DATE - INTERVAL '1 year';
    """

    cursor.execute(create_table_query)
    connection.commit()

def normalize_time(time_str):
    try:
        # Split the time string into hours and minutes
        hours, minutes = map(int, time_str.split(':'))
        # Normalize the hours if they are 24 or more
        if hours >= 24:
            hours -= 24
        # Create a datetime object with the normalized time
        time_obj = datetime.strptime(f"{hours:02}:{minutes:02}", "%H:%M")
        return time_obj.strftime("%H:%M")
    except ValueError:
        # Handle invalid time format
        return None

def extract_line_name(line_string):
    parts = line_string.split(" - ")
    if len(parts) > 1:
        return parts[1]
    else:
        return parts[0]
    
def epoch_to_date(epoch):
    return datetime.fromtimestamp(epoch).strftime('%Y-%m-%d')

def insert_into_bus_metro_stop_line_tables(cursor):
    # Insert data into the stm_metro_line and stm_bus_line tables
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
    
    # Insert data into the stm_metro_stop and stm_bus_stop tables
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

def fetch_and_create_json_stm_response_json(url):
    stm_response = requests.get(url, headers=stmHeaders)
    if "gtfs-rt" in url:
       if stm_response.status_code == 200:
            try:
               # Parse the Protobuf data from the response content
                trip_updates = gtfs_pb2.FeedMessage()
                trip_updates.ParseFromString(stm_response.content)
                
                # Convert the Protobuf message to JSON
                json_trip_updates = MessageToJson(trip_updates)
                
                # Write the JSON data to stm_response_trips.json
                with open('stm_response_trips.json', 'w') as json_file:
                    json.dump(json.loads(json_trip_updates), json_file, indent=4)
                
                print("Protobuf response has been written to stm_response_trips.json")
            except Exception as e:
                print(f"Error: {e}")
    else:
        if stm_response.status_code == 200:
            stm_response_json = stm_response.json()
            with open('stm_response_v1.json', 'w') as json_file:
                json.dump(stm_response, json_file, indent=4)
                print("Json response has been written to stm_response_v1.json")
            if "v1" in url:
                file_name = "stm_response_v1.json"
            elif "v2" in url:
                file_name = "stm_response_v2.json"
            else:
                print("Error: Invalid URL")
                return
            with open(file_name, 'w') as json_file:
                json.dump(stm_response_json, json_file, indent=4)
                print(f"Json response has been written to {file_name}")
            
        else:
            print(f"Error: Received status code {stm_response.status_code} for URL {url}")

def fetch_and_create_ville_de_montreal_json(url):
    number_of_records_per_request = 100
    offset = 0
    ville_de_montreal_base_url = "https://donnees.montreal.ca/api/3/action/datastore_search"
    ville_de_montreal_data = []

    if "518d9c92-89a3-408a-8ac4-04ee43e2ac9e" in url:
        limit = 17200
        file_name = "incidents_reseau_du_metro_all.json"
    elif "534cdfd9-41e5-4e11-8675-738485509cce" in url: 
        limit = 5400
        file_name = "kilometrage_metro_planifie_all.json"
    elif "c35e14b7-31b7-410d-9773-158bc30749df" in url:
        limit = 31000
        file_name = "kilometrage_metro_realise_all.json"
    else:
        print("Error: Invalid URL")
        return
    
    while offset != limit:
        ville_de_montreal_response = requests.get(f"{ville_de_montreal_base_url}?resource_id={url}&limit={number_of_records_per_request}&offset={offset}")
        if ville_de_montreal_response.status_code == 200:
            data = ville_de_montreal_response.json()
            records = data.get("result", {}).get("records", [])
            ville_de_montreal_data.extend(records)
            offset += number_of_records_per_request

    if ville_de_montreal_data:
        with open(file_name, 'w') as json_file:
            json.dump(ville_de_montreal_data, json_file, indent=4)
            print(f"All data has been written to {file_name}")
