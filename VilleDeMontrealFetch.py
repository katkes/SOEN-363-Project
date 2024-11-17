import requests
import psycopg2
import json
from datetime import datetime, timedelta

connection = psycopg2.connect(
    host="localhost",
    dbname="SOEN-363-Project",
    user="postgres",
    password="1234",
    port=5432
)
cursor = connection.cursor()

ville_de_montreal_base_url = "https://donnees.montreal.ca/api/3/action/datastore_search"
incidents_reseau_du_metro_resource_id = "518d9c92-89a3-408a-8ac4-04ee43e2ac9e"
kilometrage_metro_planifie_resource_id = "534cdfd9-41e5-4e11-8675-738485509cce"
kilometrage_metro_realise_resource_id = "c35e14b7-31b7-410d-9773-158bc30749df"

incidents_reseau_du_metro_data, kilometrage_metro_planifie_data, kilometrage_metro_realise_data = [], [], []

number_of_records_per_request = 100  # Number of records to fetch per request
incidents_reseau_offset, kilometrage_metro_planifie_offset, kilometrage_metro_realise_offset = 0, 0, 0
incidents_reseau_limit, kilometrage_metro_planifie_limit, kilometrage_metro_realise_limit = 17200, 5400, 31000

stm_metro_line = {"Ligne verte": 1, "Ligne orange": 2, "Ligne jaune":4, "Ligne bleue":5}

create_table_query = """
CREATE TABLE IF NOT EXISTS stm_incident(
    stm_incident_id INT PRIMARY KEY,
    stm_incident_type VARCHAR(255),
    stm_incident_primary_cause VARCHAR(255),
    stm_incident_secondary_cause VARCHAR(255),
    stm_incident_time_of_incident TIME,
    stm_incident_time_of_resolution TIME,
    stm_incident_date_of_incident DATE,
    stm_incident_location_of_incident VARCHAR(255),
    stm_metro_line_id INT,
    FOREIGN KEY (stm_metro_line_id) REFERENCES stm_metro_line(stm_metro_line_id)
);

CREATE TABLE IF NOT EXISTS stm_metro_planned_kilometerage (
    stm_metro_planned_kilometerage_id INT PRIMARY KEY,
    stm_metro_line_id INT,
    planned_kilometerage INT,
    day_of_week VARCHAR(25),
    stm_metro_planned_kilometerage_date DATE,
    FOREIGN KEY (stm_metro_line_id) REFERENCES stm_metro_line(stm_metro_line_id)
);
"""

cursor.execute(create_table_query)
connection.commit()

def normalize_time(time_str):
    try:
        # Convert the time string to a datetime object
        time_obj = datetime.strptime(time_str, "%H:%M")
        # If the hour is 24 or more, normalize it to 00:00 of the next day
        if time_obj.hour >= 24:
            time_obj -= timedelta(hours=24)
        return time_obj.strftime("%H:%M")
    except ValueError:
        # Handle invalid time format
        return None


# while incidents_reseau_offset != incidents_reseau_limit:  # Limiting to 17200 records out of the available records
#     response = requests.get(f"{ville_de_montreal_base_url}?resource_id={incidents_reseau_du_metro_resource_id}&limit={number_of_records_per_request}&offset={incidents_reseau_offset}")
#     if response.status_code == 200:
#         data = response.json()
#         records = data.get("result", {}).get("records", [])
#         incidents_reseau_du_metro_data.extend(records)
#         incidents_reseau_offset += number_of_records_per_request  # Move to the next set of results
#     else:
#         print(f"Error: Received status code {response.status_code}")
#         break

# if incidents_reseau_du_metro_data:
#     for record in incidents_reseau_du_metro_data:
#         print(stm_metro_line.get(record.get("Ligne")))
#         line_name = record.get("Ligne", "").strip().lower()
#         line_id = stm_metro_line.get(line_name.capitalize())
#         print(f"Line name: {line_name}, Line ID: {line_id}")
#         print(record)
#         cursor.execute("INSERT INTO stm_incident (stm_incident_id, stm_incident_type, stm_incident_primary_cause, stm_incident_secondary_cause, stm_incident_time_of_incident, stm_incident_time_of_resolution, stm_incident_date_of_incident, stm_incident_location_of_incident, stm_metro_line_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
#                         (record.get("_id"), 
#                         record.get("Type d'incident"), 
#                         record.get("Cause primaire"), 
#                         record.get("Cause secondaire"), 
#                         normalize_time(record.get("Heure de l'incident")), 
#                         normalize_time(record.get("Heure de reprise")), 
#                         record.get("Jour calendaire"), 
#                         record.get("Code de lieu"), 
#                         line_id))
#         connection.commit()

        
# # Save all data to a JSON file
# if incidents_reseau_du_metro_data:
#     with open('incidents_reseau_du_metro_all.json', 'w') as json_file:
#         json.dump(incidents_reseau_du_metro_data, json_file, indent=4)
#         print("All data has been written to incidents_reseau_du_metro_all.json")
# else:
#     print("No data retrieved.")

while kilometrage_metro_planifie_offset != kilometrage_metro_planifie_limit:  # Limiting to 5400 records out of the 5432 available records
    response = requests.get(f"{ville_de_montreal_base_url}?resource_id={kilometrage_metro_planifie_resource_id}&limit={number_of_records_per_request}&offset={kilometrage_metro_planifie_offset}")
    if response.status_code == 200:
        data = response.json()
        records = data.get("result", {}).get("records", [])
        kilometrage_metro_planifie_data.extend(records)
        kilometrage_metro_planifie_offset += number_of_records_per_request  # Move to the next set of results
    else:
        print(f"Error: Received status code {response.status_code}")
        break


if kilometrage_metro_planifie_data:
    for record in kilometrage_metro_planifie_data:
        print(record)
        planned_kilometerage_str = record.get("KM planifié", "0").replace(",", ".")
        planned_kilometerage = round(float(planned_kilometerage_str))
        cursor.execute("INSERT INTO stm_metro_planned_kilometerage (stm_metro_planned_kilometerage_id, stm_metro_line_id, planned_kilometerage, day_of_week, stm_metro_planned_kilometerage_date) VALUES (%s, %s, %s, %s, %s)", 
                        (record.get("_id"), 
                        stm_metro_line.get(record.get("Ligne")), 
                        planned_kilometerage, 
                        record.get("Jour de la semaine"),
                        record.get("Jour calendaire")))
        connection.commit()
        
# # Save all data to a JSON file
# if kilometrage_metro_planifie_data:
#     with open('kilometrage_metro_planifie_all.json', 'w') as json_file:
#         json.dump(kilometrage_metro_planifie_data, json_file, indent=4)
#         print("All data has been written to kilometrage_metro_planifie_all.json")
# else:
#     print("No data retrieved.")



# while kilometrage_metro_realise_offset != kilometrage_metro_realise_limit:  # Limiting to 310000 records out of the 316652 available records for now
#     response = requests.get(f"{ville_de_montreal_base_url}?resource_id={kilometrage_metro_realise_resource_id}&limit={number_of_records_per_request}&offset={kilometrage_metro_realise_offset}")
#     if response.status_code == 200:
#         data = response.json()
#         print(kilometrage_metro_realise_offset)
#         records = data.get("result", {}).get("records", [])
#         kilometrage_metro_realise_data.extend(records)
#         kilometrage_metro_realise_offset += number_of_records_per_request  # Move to the next set of results
#     else:
#         print(f"Error: Received status code {response.status_code}")
#         break

# # Save all data to a JSON file
# if kilometrage_metro_realise_data:
#     with open('kilometrage_metro_realise_all.json', 'w') as json_file:
#         json.dump(kilometrage_metro_realise_data, json_file, indent=4)
#         print("All data has been written to kilometrage_metro_realise_all.json")
# else:
#     print("No data retrieved.")




connection.commit()
cursor.close()
connection.close()