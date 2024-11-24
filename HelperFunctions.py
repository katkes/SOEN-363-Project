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

stm_metro_line_mapping = {
    "Ligne verte": 1, 
    "Ligne orange": 2, 
    "Ligne jaune":4, 
    "Ligne bleue":5
}

location_type_mapping = {
    0: "Stop",
    1: "Station",
    2: "Station entrance",
    3: "Generic node",
    4: "Boarding area"
}

def table_creation():
    cursor = connection.cursor()
    create_table_query = """
    CREATE DOMAIN planned_kilometerage AS INT CHECK (VALUE >= 0);
    CREATE DOMAIN realized_kilometerage AS INT CHECK (VALUE >= 0);

    CREATE TYPE day_of_week AS ENUM ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');
    CREATE TYPE metro_colour AS ENUM ('Green', 'Orange', 'Yellow', 'Blue');

    -- The stm_route table represents a stm_route entity
    -- A stm_route entity is a representation of a route, like the 123 Dollard bus or the Green line
    -- This table is populated with the content of the routes.txt files from the publically available STM gtfs information
    CREATE TABLE IF NOT EXISTS stm_route(
        stm_route_id INT PRIMARY KEY,
        stm_route_number INT NOT NULL CHECK (stm_route_number > 0)
    );

    -- The stm_metro_route table represents a stm_metro_route entity
    -- A stm_metro_route entity is a representation of a metro route, like the Green line, and is a stm_route
    -- Note: A stm_metro_route entity does NOT have direction cardinality, as a metro route can have multiple directions
    -- This table is populated with the content of the routes.txt files from the publically available STM gtfs information
    CREATE TABLE IF NOT EXISTS stm_metro_route(
        stm_metro_route_id INT PRIMARY KEY,
        stm_metro_route_colour metro_colour NOT NULL,
        FOREIGN KEY (stm_metro_route_id) REFERENCES stm_route(stm_route_id)
    );

    -- The stm_bus_route table represents a stm_bus_route entity
    -- A stm_bus_route entity is a representation of a bus route, like the 123 Dollard bus, and is a stm_route
    -- Note: A stm_bus_route entity does NOT have direction cardinality, as a bus route can have multiple directions
    -- This table is populated with the content of the routes.txt files from the publically available STM gtfs information
    CREATE TABLE IF NOT EXISTS stm_bus_route(
        stm_bus_route_id INT PRIMARY KEY,
        stm_route_name VARCHAR(255) NOT NULL,
        FOREIGN KEY (stm_bus_route_id) REFERENCES stm_route(stm_route_id)
    );

    -- The stm_metro_trip table represents a stm_metro_trip entity
    -- A metro trip is an instance of a metro vehicle that's travelling on a route
    -- The metro trip visits the same sequence of stops at the same time of the day, this shows that a stm_metro_trip is a scheduled instance of a stm_metro_route
    -- Note: A stm_metro_trip entity does have direction cardinality, a trip differs to a stm_metro_route entity by its direction among other things
    -- This table is populated with the content of the trips.txt files from the publically available STM gtfs information
    CREATE TABLE IF NOT EXISTS stm_metro_trip(
        stm_metro_trip_id INT PRIMARY KEY,
        stm_metro_trip_route_id INT,
        stm_metro_trip_service_id VARCHAR(255) NOT NULL,
        stm_metro_trip_headsign VARCHAR(255) NOT NULL,
        stm_metro_trip_direction_id INT NOT NULL CHECK (stm_metro_trip_direction_id = 0 OR stm_metro_trip_direction_id = 1),
        FOREIGN KEY (stm_metro_trip_route_id) REFERENCES stm_metro_route(stm_metro_route_id)
    );

    -- The stm_bus_trip table represents a stm_bus_trip entity
    -- A bus trip is an instance of a bus vehicle that's travelling on a route
    -- The bus trip visits the same sequence of stops at the same time of the day, this shows that a stm_bus_trip is a scheduled instance of a stm_bus_route
    -- Note: A stm_bus_trip entity does have direction cardinality, a trip differs to a stm_bus_route entity by its direction among other things
    -- This table is populated with the content of the trips.txt files from the publically available STM gtfs information
    CREATE TABLE IF NOT EXISTS stm_bus_trip(
        stm_bus_trip_id INT PRIMARY KEY,
        stm_bus_trip_route_id INT,
        stm_bus_trip_service_id VARCHAR(255) NOT NULL,
        stm_bus_trip_headsign VARCHAR(255) NOT NULL,
        stm_bus_trip_direction_id INT NOT NULL CHECK (stm_bus_trip_direction_id = 0 OR stm_bus_trip_direction_id = 1),
        FOREIGN KEY (stm_bus_trip_route_id) REFERENCES stm_bus_route(stm_bus_route_id)
    );

    -- The stm_bus_stop table represents a stm_bus_stop entity
    -- A stm_bus_stop entity is a representation of a physical bus stop
    -- This table is populated with the content of the stops.txt files from the publically available STM gtfs information
    CREATE TABLE IF NOT EXISTS stm_bus_stop(
        stm_bus_stop_id VARCHAR(15) PRIMARY KEY,
        stm_bus_stop_name VARCHAR(255) NOT NULL,
        stm_bus_stop_code INT NOT NULL CHECK (stm_bus_stop_code > 0),
        stm_bus_stop_location_type VARCHAR(255) NOT NULL,
        stm_bus_stop_latitude DECIMAL(9, 6) NOT NULL,
        stm_bus_stop_longitude DECIMAL(9, 6) NOT NULL,
        stm_bus_stop_is_wheelchair_accessible BOOLEAN DEFAULT FALSE,
        stm_bus_stop_is_active BOOLEAN DEFAULT TRUE
    );

    -- The stm_metro_stop table represents a stm_metro_stop entity
    -- A stm_metro_stop entity is a representation of a physical metro stop
    -- This table is populated with the content of the stops.txt files from the publically available STM gtfs information
    CREATE TABLE IF NOT EXISTS stm_metro_stop(
        stm_metro_stop_id VARCHAR(15) PRIMARY KEY,
        stm_metro_stop_name VARCHAR(255) NOT NULL,
        stm_metro_stop_code INT NOT NULL CHECK (stm_metro_stop_code > 0),
        stm_metro_stop_location_type VARCHAR(255) NOT NULL,
        stm_metro_stop_latitude DECIMAL(9, 6) NOT NULL,
        stm_metro_stop_longitude DECIMAL(9, 6) NOT NULL,
        stm_metro_stop_is_wheelchair_accessible BOOLEAN DEFAULT FALSE
    );

    -- The stm_metro_stop_time table represents a relationship between stm_metro_trip and stm_metro_stop
    -- A stm_metro_stop_time entity that defines "visited" relationship between a stm_metro_trip entity and a stm_metro_stop entity
    -- This relationship is a many-to-many relationship, as a metro trip can visit multiple stops and a stop can be visited by multiple trips
    -- This table is populated with the content of the stop_times.txt files from the publically available STM gtfs information
    CREATE TABLE IF NOT EXISTS stm_metro_stop_time(
        stm_metro_stop_time_id INT PRIMARY KEY,
        stm_metro_stop_time_trip_id INT NOT NULL,
        stm_metro_stop_time_stop_id VARCHAR(15) NOT NULL,
        stm_metro_stop_time_stop_sequence INT NOT NULL,
        stm_metro_stop_arrival_time TIME NOT NULL,
        stm_metro_stop_departure_time TIME NOT NULL,
        FOREIGN KEY (stm_metro_stop_time_trip_id) REFERENCES stm_metro_trip(stm_metro_trip_id),
        FOREIGN KEY (stm_metro_stop_time_stop_id) REFERENCES stm_metro_stop(stm_metro_stop_id)
    );

    -- The stm_bus_stop_time table represents a relationship between stm_bus_trip and stm_bus_stop
    -- A stm_bus_stop_time entity that defines "visited" relationship between a stm_bus_trip entity and a stm_bus_stop entity
    -- This relationship is a many-to-many relationship, as a bus trip can have multiple stops and a stop can be visited by multiple trips
    -- This table is populated with the content of the stop_times.txt files from the publically available STM gtfs information
    CREATE TABLE IF NOT EXISTS stm_bus_stop_time(
        stm_bus_stop_time_id INT PRIMARY KEY,
        stm_bus_stop_time_trip_id INT NOT NULL,
        stm_bus_stop_time_stop_id VARCHAR(15) NOT NULL,
        stm_bus_stop_time_stop_sequence INT NOT NULL,
        stm_bus_stop_arrival_time TIME NOT NULL,
        stm_bus_stop_departure_time TIME NOT NULL,
        FOREIGN KEY (stm_bus_stop_time_trip_id) REFERENCES stm_bus_trip(stm_bus_trip_id),
        FOREIGN KEY (stm_bus_stop_time_stop_id) REFERENCES stm_bus_stop(stm_bus_stop_id)
    );

    -- The stm_bus_stop_cancelled_moved_relocated table represents a stm_bus_stop_cancelled_moved_relocated entity
    -- A stm_bus_stop_cancelled_moved_relocated entity IS A stm_bus_stop entity that is denoted as cancelled, moved or relocated
    -- Along with having the tag that it's cancelled, moved or relocated, it also has a reason and a date
    -- This table is populated with the content of the etatservice (v2) API provided publicly by the STM
    CREATE TABLE IF NOT EXISTS stm_bus_stop_cancelled_moved_relocated(
        stm_bus_stop_cancelled_moved_relocated_id INT PRIMARY KEY,
        stm_bus_stop_id VARCHAR(15) NOT NULL,
        stm_bus_stop_code INT NOT NULL CHECK (stm_bus_stop_code > 0),
        stm_bus_stop_cancelled_moved_relocated_date DATE NOT NULL,
        stm_bus_stop_cancelled_moved_relocated_reason TEXT NOT NULL,
        FOREIGN KEY (stm_bus_stop_id) REFERENCES stm_bus_stop(stm_bus_stop_id) ON DELETE CASCADE
    );

    -- The stm_metro_planned_kilometerage table represents a stm_metro_planned_kilometerage entity
    -- A stm_metro_planned_kilometerage entity is a representation of the planned kilometerage of a metro route on a specific date
    -- This table is populated with the content of the Kilométrage du budget d'exploitation du métro API provided publicly by the Ville de Montréal
    CREATE TABLE IF NOT EXISTS stm_metro_planned_kilometerage (
        stm_metro_planned_kilometerage_id INT PRIMARY KEY,
        stm_metro_route_id INT NOT NULL,
        planned_kilometerage planned_kilometerage NOT NULL,
        day_of_week day_of_week NOT NULL,
        stm_metro_planned_kilometerage_date DATE NOT NULL,
        FOREIGN KEY (stm_metro_route_id) REFERENCES stm_metro_route(stm_metro_route_id)
    );

    -- The stm_metro_realized_kilometerage table represents a stm_metro_realized_kilometerage entity
    -- A stm_metro_realized_kilometerage entity is a representation of the realized kilometerage of a metro route on a specific date
    -- This table is populated with the content of the Kilométrage réalisé par les voitures de métro API provided publicly by the Ville de Montréal
    CREATE TABLE IF NOT EXISTS stm_metro_realized_kilometerage (
        stm_metro_realized_kilometerage_id INT PRIMARY KEY,
        stm_metro_route_id INT NOT NULL,
        realized_kilometerage realized_kilometerage NOT NULL,
        day_of_week_or_type_of_day VARCHAR(25) NOT NULL,
        stm_metro_realized_kilometerage_date DATE NOT NULL,
        FOREIGN KEY (stm_metro_route_id) REFERENCES stm_metro_route(stm_metro_route_id)
    );


    -- The stm_incident table represents a stm_incident entity
    -- A stm_incident entity is a representation of an incident that has occurred on the STM metro network
    -- This table is populated with the content of the Incidents du réseau du métro API provided publicly by the Ville de Montréal
    CREATE TABLE IF NOT EXISTS stm_incident(
        stm_incident_id INT PRIMARY KEY,
        stm_incident_type VARCHAR(255) NOT NULL,
        stm_incident_primary_cause VARCHAR(255) NOT NULL,
        stm_incident_secondary_cause VARCHAR(255),
        stm_incident_time_of_incident TIME NOT NULL,
        stm_incident_time_of_resolution TIME,
        stm_incident_date_of_incident DATE NOT NULL,
        stm_incident_location_of_incident VARCHAR(255) NOT NULL,
        stm_metro_route_id INT NOT NULL,
        FOREIGN KEY (stm_metro_route_id) REFERENCES stm_metro_route(stm_metro_route_id)
    );

    -- The live_stm_bus_trip table represents a live_stm_bus_trip entity
    -- A live_stm_bus_trip entity is a representation of a bus trip that is currently in progress
    -- This table is populated with the content of the GTFS-Realtime API provided publicly by the STM
    CREATE TABLE IF NOT EXISTS live_stm_bus_trip(
        live_stm_bus_trip_id INT PRIMARY KEY,
        stm_bus_trip_id INT NOT NULL,
        live_stm_bus_trip_date TIMESTAMP NOT NULL,
        FOREIGN KEY (stm_bus_trip_id) REFERENCES stm_bus_trip(stm_bus_trip_id)
    );

    -- The live_stm_bus_trip table represents a live_stm_bus_trip_stop entity
    -- A live_stm_bus_trip_stop entity is a representation of a bus stop that a bus trip has visited, is currently at or is scheduled to visit
    -- A live_stm_bus_trip_stop entity has a weak entity relationship with live_stm_bus_trip, where the relationship is "composed of"
    -- This table is populated with the content of the GTFS-Realtime API provided publicly by the STM
    CREATE TABLE IF NOT EXISTS live_stm_bus_trip_stop(
        live_stm_bus_trip_stop_id INT,
        live_stm_bus_trip_id INT NOT NULL,
        stm_bus_stop_id VARCHAR(15) NOT NULL,
        live_stm_bus_stop_arrival_time TIMESTAMP NOT NULL,
        live_stm_bus_stop_departure_time TIMESTAMP NOT NULL,
        live_stm_bus_trip_stop_sequence INT NOT NULL,
        live_stm_bus_trip_stop_schedule_relationship VARCHAR(255),
        PRIMARY KEY (live_stm_bus_trip_stop_id, live_stm_bus_trip_id, stm_bus_stop_id),
        FOREIGN KEY (live_stm_bus_trip_id) REFERENCES live_stm_bus_trip(live_stm_bus_trip_id),
        FOREIGN KEY (stm_bus_stop_id) REFERENCES stm_bus_stop(stm_bus_stop_id)
    );

    -- View for a low key access to the stm_incident table, only showing incidents from the last year
    CREATE OR REPLACE VIEW low_key_access_stm_incident AS
    SELECT stm_incident_id, stm_incident_type, stm_incident_date_of_incident, stm_incident_location_of_incident
    FROM stm_incident
    WHERE stm_incident_date_of_incident >= CURRENT_DATE - INTERVAL '1 year';

    -- Create a trigger function to enforce referential integrity: Updating the bus stop's active status to false if it is placed in the stm_bus_stop_cancelled_moved_relocated table
    CREATE OR REPLACE FUNCTION update_bus_stop_inactive()
    RETURNS TRIGGER AS $$
    BEGIN
        -- Update the associated bus stop's active status to false
        UPDATE stm_bus_stop
        SET stm_bus_stop_is_active = FALSE
        WHERE stm_bus_stop_code = NEW.stm_bus_stop_code;
    
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- Create a trigger to call the function after insert
    CREATE TRIGGER trg_update_bus_stop_inactive
    AFTER INSERT ON stm_bus_stop_cancelled_moved_relocated
    FOR EACH ROW
    EXECUTE FUNCTION update_bus_stop_inactive();
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
    epoch = int(epoch)
    return datetime.fromtimestamp(epoch).strftime('%d-%m-%Y')

def epoch_to_timestamp(epoch):
    try:
        epoch = int(epoch)
        return datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return None


def insert_into_stm_stop_line_tables(cursor):
    # Insert data into the stm_metro_line and stm_bus_line tables
    with open('ConstantInformation/gtfs_stm/routes.txt', mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            route_id = row['route_id']
            stm_route_number = row['route_id']
            insert_query = "INSERT INTO stm_route (stm_route_id, stm_route_number) VALUES (%s, %s);"
            cursor.execute(insert_query, (route_id, stm_route_number))

            line_name = extract_line_name(row['route_long_name'])
            if "Ligne" in row['route_long_name']:
                color_name = french_english_color_mapping.get(line_name, line_name)
                insert_query = "INSERT INTO stm_metro_route (stm_metro_route_id, stm_metro_route_colour) VALUES (%s, %s);"
                cursor.execute(insert_query, (route_id, color_name))
            else:
                insert_query = "INSERT INTO stm_bus_route (stm_bus_route_id, stm_route_name) VALUES (%s, %s);"
                cursor.execute(insert_query, (route_id, line_name))

    print("Data inserted into stm_metro_line and stm_bus_line tables")
    
    # Insert data into the stm_metro_stop and stm_bus_stop tables
    with open('ConstantInformation/gtfs_stm/stops.txt', mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            stop_id = row['stop_id']
            stop_name = row['stop_name']
            stop_code = row['stop_code']
            stop_location_type = location_type_mapping.get(int(row['location_type']))
            stop_latitude = row['stop_lat']
            stop_longitude = row['stop_lon']
            is_wheelchair_accessible = row['wheelchair_boarding'] == '1'
            
            if stop_location_type == "Stop" or stop_location_type == "Generic Node"  or stop_location_type == "Boarding area":
                insert_query = "INSERT INTO stm_bus_stop (stm_bus_stop_id, stm_bus_stop_name, stm_bus_stop_code, stm_bus_stop_location_type, stm_bus_stop_latitude, stm_bus_stop_longitude, stm_bus_stop_is_wheelchair_accessible) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            else:
                insert_query = "INSERT INTO stm_metro_stop (stm_metro_stop_id, stm_metro_stop_name, stm_metro_stop_code, stm_metro_stop_location_type, stm_metro_stop_latitude, stm_metro_stop_longitude, stm_metro_stop_is_wheelchair_accessible) VALUES (%s, %s, %s, %s, %s, %s, %s);"
           
            cursor.execute(insert_query, (stop_id, stop_name, stop_code, stop_location_type, stop_latitude, stop_longitude, is_wheelchair_accessible))

    print("Data inserted into stm_metro_stop and stm_bus_stop tables")

    # Insert data into the stm_metro_trip and stm_bus_trip tables
    with open('ConstantInformation/gtfs_stm/trips.txt', mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            trip_id = row['trip_id']
            route_id = row['route_id']
            service_id = row['service_id']
            trip_headsign = row['trip_headsign']
            direction_id = row['direction_id']

            cursor.execute("SELECT stm_bus_route_id FROM stm_bus_route WHERE stm_bus_route_id = %s", (route_id,))
            result_route_id = cursor.fetchone()
            
            if result_route_id:
                insert_query = "INSERT INTO stm_bus_trip (stm_bus_trip_id, stm_bus_trip_route_id, stm_bus_trip_service_id, stm_bus_trip_headsign, stm_bus_trip_direction_id) VALUES (%s, %s, %s, %s, %s);"
            else:
                insert_query = "INSERT INTO stm_metro_trip (stm_metro_trip_id, stm_metro_trip_route_id, stm_metro_trip_service_id, stm_metro_trip_headsign, stm_metro_trip_direction_id) VALUES (%s, %s, %s, %s, %s);"
            cursor.execute(insert_query, (trip_id, route_id, service_id, trip_headsign, direction_id))
    
    print("Data inserted into stm_metro_trip and stm_bus_trip tables")

    # Insert data into the stm_metro_stop_time and stm_bus_stop_time tables
    with open('ConstantInformation/gtfs_stm/stop_times.txt', mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        stop_time_id = 1
        for row in csv_reader:
            trip_id = row['trip_id']
            stop_id = row['stop_id']
            stop_sequence = row['stop_sequence']
            arrival_time = normalize_time(row['arrival_time'])
            departure_time = normalize_time(row['departure_time'])
            if arrival_time is None or departure_time is None:
                continue # TODO: fix overflow of time, currently ignoring invalid time entries

            cursor.execute("SELECT stm_bus_trip_id FROM stm_bus_trip WHERE stm_bus_trip_id = %s", (trip_id, ))
            result_trip = cursor.fetchone()
            
            cursor.execute("SELECT stm_bus_stop_id FROM stm_bus_stop WHERE stm_bus_stop_code = %s", (stop_id, ))
            result_stop = cursor.fetchone()

            if result_trip and result_stop:
                insert_query = "INSERT INTO stm_bus_stop_time (stm_bus_stop_time_id, stm_bus_stop_time_trip_id, stm_bus_stop_time_stop_id, stm_bus_stop_time_stop_sequence, stm_bus_stop_arrival_time, stm_bus_stop_departure_time) VALUES (%s, %s, %s, %s, %s, %s);"
            else:
                insert_query = "INSERT INTO stm_metro_stop_time (stm_metro_stop_time_id, stm_metro_stop_time_trip_id, stm_metro_stop_time_stop_id, stm_metro_stop_time_stop_sequence, stm_metro_stop_arrival_time, stm_metro_stop_departure_time) VALUES (%s, %s, %s, %s, %s, %s);"

            cursor.execute(insert_query, (stop_time_id, trip_id, stop_id, stop_sequence, arrival_time, departure_time))
            stop_time_id += 1
        
    connection.commit()

    print("Data inserted into stm_metro_stop_time and stm_bus_stop_time tables")

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

def fetch_and_create_ville_de_montreal_json(resource_id):
    number_of_records_per_request = 100
    offset = 0
    ville_de_montreal_base_url = "https://donnees.montreal.ca/api/3/action/datastore_search"
    ville_de_montreal_data = []

    if "518d9c92-89a3-408a-8ac4-04ee43e2ac9e" in resource_id:
        limit = 17200
        file_name = "incidents_reseau_du_metro_all.json"
    elif "534cdfd9-41e5-4e11-8675-738485509cce" in resource_id: 
        limit = 5400
        file_name = "kilometrage_metro_planifie_all.json"
    elif "c35e14b7-31b7-410d-9773-158bc30749df" in resource_id:
        limit = 31000
        file_name = "kilometrage_metro_realise_all.json"
    else:
        print("Error: Invalid URL")
        return
    
    while offset != limit:
        ville_de_montreal_response = requests.get(f"{ville_de_montreal_base_url}?resource_id={resource_id}&limit={number_of_records_per_request}&offset={offset}")
        if ville_de_montreal_response.status_code == 200:
            data = ville_de_montreal_response.json()
            records = data.get("result", {}).get("records", [])
            ville_de_montreal_data.extend(records)
            offset += number_of_records_per_request

    if ville_de_montreal_data:
        with open(file_name, 'w') as json_file:
            json.dump(ville_de_montreal_data, json_file, indent=4)
            print(f"All data has been written to {file_name}")
