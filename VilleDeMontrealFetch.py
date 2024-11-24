import json
from HelperFunctions import normalize_time, fetch_and_create_ville_de_montreal_json, day_of_week_mapping, stm_metro_line_mapping
from Creds import connection

cursor = connection.cursor()

incidents_reseau_du_metro_resource_id = "518d9c92-89a3-408a-8ac4-04ee43e2ac9e"
kilometrage_metro_planifie_resource_id = "534cdfd9-41e5-4e11-8675-738485509cce"
kilometrage_metro_realise_resource_id = "c35e14b7-31b7-410d-9773-158bc30749df"
jour_calendaire = "Jour calendaire"

# fetch_and_create_ville_de_montreal_json(incidents_reseau_du_metro_resource_id)
# fetch_and_create_ville_de_montreal_json(kilometrage_metro_planifie_resource_id)
# fetch_and_create_ville_de_montreal_json(kilometrage_metro_realise_resource_id)  --> Commented out as it would take too long to run

# Load the realized kilometrage data from made incidents_reseau_du_metro_all.json file
with open('incidents_reseau_du_metro_all.json', 'r') as file:
    incidents_reseau_du_metro_data = json.load(file)

    for record in incidents_reseau_du_metro_data:
        line_name = record.get("Ligne", "").strip()
        if line_name not in stm_metro_line_mapping:
            continue
        line_id = stm_metro_line_mapping.get(line_name.capitalize())
        incident_time = normalize_time(record.get("Heure de l'incident"))
        incident_resolution_time = normalize_time(record.get("Heure de reprise"))
        cursor.execute("INSERT INTO stm_incident (stm_incident_id, stm_incident_type, stm_incident_primary_cause, stm_incident_secondary_cause, stm_incident_time_of_incident, stm_incident_time_of_resolution, stm_incident_date_of_incident, stm_incident_location_of_incident, stm_metro_route_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                        (record.get("_id"), 
                        record.get("Type d'incident"), 
                        record.get("Cause primaire"), 
                        record.get("Cause secondaire"), 
                        normalize_time(record.get("Heure de l'incident")), 
                        normalize_time(record.get("Heure de reprise")), 
                        record.get(jour_calendaire), 
                        record.get("Code de lieu"), 
                        line_id))
        connection.commit()

# Load the realized kilometrage data from made kilometrage_metro_planifie_all.json file
with open('kilometrage_metro_planifie_all.json', 'r') as file:
    kilometrage_metro_planifie_data = json.load(file)

    for record in kilometrage_metro_planifie_data:
        day_of_week = day_of_week_mapping.get(record.get("Jour de la semaine"))
        line_name = record.get("Ligne", "").strip().lower()
        line_id = stm_metro_line_mapping.get(line_name.capitalize())
        if line_id is None:
            continue
        planned_kilometerage_str = record.get("KM planifié", "0").replace(",", ".")
        planned_kilometerage = round(float(planned_kilometerage_str))
        cursor.execute("INSERT INTO stm_metro_planned_kilometerage (stm_metro_planned_kilometerage_id, stm_metro_route_id, planned_kilometerage, day_of_week, stm_metro_planned_kilometerage_date) VALUES (%s, %s, %s, %s, %s)", 
                        (record.get("_id"), 
                        stm_metro_line_mapping.get(record.get("Ligne")), 
                        planned_kilometerage, 
                        day_of_week,
                        record.get(jour_calendaire)))
        connection.commit()

# Load the realized kilometrage data from downloaded kilometrage_metro_realise_all.json file
with open('ConstantInformation/kilometrage_metro_realise_all.json', 'r', encoding='utf-8') as json_file:
    kilometrage_metro_realise_data = json.load(json_file)

for record in kilometrage_metro_realise_data:
    realized_kilometerage_str = record.get("Km voiture", "0").replace(",", ".")
    realized_kilometerage = round(float(realized_kilometerage_str))
    cursor.execute("INSERT INTO stm_metro_realized_kilometerage (stm_metro_realized_kilometerage_id, stm_metro_route_id, realized_kilometerage, day_of_week_or_type_of_day, stm_metro_realized_kilometerage_date) VALUES (%s, %s, %s, %s, %s)", 
                    (record.get("_id"), 
                    stm_metro_line_mapping.get(record.get("Ligne")), 
                    realized_kilometerage, 
                    record.get("Type de jour"),
                    record.get(jour_calendaire)))
    connection.commit()

connection.commit()
cursor.close()
connection.close()