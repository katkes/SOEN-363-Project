from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()
NEO4J_PASS = os.getenv("NEO4J_PASS")

# Neo4j connection details
neo4j_uri = "bolt://localhost:7687"
neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=("neo4j", NEO4J_PASS))

# Function to load CSV data into Neo4j
def load_csv_to_neo4j(driver, file_name, cypher_query):
    with driver.session() as session:
        session.run(cypher_query, file=file_name)

# Main function to load data from CSV to Neo4j
def load_data():

    load_metro_route_query = """
    LOAD CSV WITH HEADERS FROM 'file:///stm_metro_route.csv' AS row
    CREATE (mr:MetroRoute {id: toInteger(row.stm_metro_route_id), colour: row.stm_metro_route_colour})
    """
    print("stm_metro_route.csv import started")
    load_csv_to_neo4j(neo4j_driver, "./stm_metro_route.csv", load_metro_route_query)
    print("stm_metro_route.csv import completed")

    load_bus_route_query = """
    LOAD CSV WITH HEADERS FROM 'file:///stm_bus_route.csv' AS row
    CREATE (br:BusRoute {id: toInteger(row.stm_bus_route_id), name: row.stm_route_name})
    """
    print("stm_bus_route.csv import started")
    load_csv_to_neo4j(neo4j_driver, "./stm_bus_route.csv", load_bus_route_query)
    print("stm_bus_route.csv import completed")

    load_bus_stop_query = """
    LOAD CSV WITH HEADERS FROM 'file:///stm_bus_stop.csv' AS row
    CREATE (bs:BusStop {id: toInteger(row.stm_bus_stop_id), name: row.stm_bus_stop_name, lat: toFloat(row.stm_bus_stop_latitude), lon: toFloat(row.stm_bus_stop_longitude)})
    """
    print("stm_bus_stop.csv import started")
    load_csv_to_neo4j(neo4j_driver, "./stm_bus_stop.csv", load_bus_stop_query)
    print("stm_bus_stop.csv import completed")

    load_metro_stop_query = """
    LOAD CSV WITH HEADERS FROM 'file:///stm_metro_stop.csv' AS row
    CREATE (ms:MetroStop {id: toInteger(row.stm_metro_stop_id), name: row.stm_metro_stop_name, lat: toFloat(row.stm_metro_stop_latitude), lon: toFloat(row.stm_metro_stop_longitude)})
    """
    print("stm_metro_stop.csv import started")
    load_csv_to_neo4j(neo4j_driver, "./stm_metro_stop.csv", load_metro_stop_query)
    print("stm_metro_stop.csv import completed")

    load_stm_metro_trip_query = """
    LOAD CSV WITH HEADERS FROM 'file:///stm_metro_trip.csv' AS row
    CREATE (mt:StmMetroTrip {id: toInteger(row.stm_metro_trip_id), headsign: row.stm_metro_trip_headsign, direction_id: toInteger(row.stm_metro_trip_direction_id)})
    WITH mt, row
    MATCH (mr:MetroRoute {id: toInteger(row.stm_metro_trip_route_id)})
    CREATE (mt)-[:FOLLOWS]->(mr)
    """
    print("stm_metro_trip.csv import started")
    load_csv_to_neo4j(neo4j_driver, "stm_metro_trip.csv", load_stm_metro_trip_query)
    print("stm_metro_trip.csv import completed")

    load_bus_trip_query = """
    LOAD CSV WITH HEADERS FROM 'file:///stm_bus_trip.csv' AS row
    CREATE (bt:BusTrip {id: toInteger(row.stm_bus_trip_id), headsign: row.stm_bus_trip_headsign, direction_id: toInteger(row.stm_bus_trip_direction_id)})
    WITH bt, row
    MATCH (br:BusRoute {id: toInteger(row.stm_bus_trip_route_id)})
    CREATE (bt)-[:FOLLOWS]->(br)
    """
    print("stm_bus_trip.csv import started")
    load_csv_to_neo4j(neo4j_driver, "stm_bus_trip.csv", load_bus_trip_query)
    print("stm_bus_trip.csv import completed")

    load_stm_metro_stop_time_query = """
    LOAD CSV WITH HEADERS FROM 'file:///stm_metro_stop_time.csv' AS row
    MATCH (mt:StmMetroTrip {id: toInteger(row.stm_metro_stop_time_trip_id)}), (ms:MetroStop {id: row.stm_metro_stop_time_stop_id})
    CREATE (mt)-[:VISITS {sequence: toInteger(row.stm_metro_stop_time_stop_sequence), arrival_time: row.stm_metro_stop_arrival_time, departure_time: row.stm_metro_stop_departure_time}]->(ms)
    """
    print("stm_metro_stop_time.csv import started")
    load_csv_to_neo4j(neo4j_driver, "./stm_metro_stop_time.csv", load_stm_metro_stop_time_query)
    print("stm_metro_stop_time.csv import completed")

    load_bus_stop_time_query = """
    LOAD CSV WITH HEADERS FROM 'file:///stm_bus_stop_time.csv' AS row
    MATCH (bt:BusTrip {id: toInteger(row.stm_bus_stop_time_trip_id)}), (bs:BusStop {id: toInteger(row.stm_bus_stop_time_stop_id)})
    CREATE (bt)-[:VISITS {sequence: toInteger(row.stm_bus_stop_time_stop_sequence), arrival_time: row.stm_bus_stop_arrival_time, departure_time: row.stm_bus_stop_departure_time}]->(bs)
    """
    print("stm_bus_stop_time.csv import started")
    load_csv_to_neo4j(neo4j_driver, "./stm_bus_stop_time.csv", load_bus_stop_time_query)
    print("stm_bus_stop_time.csv import completed")

    load_bus_stop_cancelled_moved_relocated_query = """
    LOAD CSV WITH HEADERS FROM 'file:///stm_bus_stop_cancelled_moved_relocated.csv' AS row
    MATCH (bs:BusStop {id: toInteger(row.stm_bus_stop_id)})
    SET bs.status = row.stm_bus_stop_cancelled_moved_relocated_reason, bs.date = row.stm_bus_stop_cancelled_moved_relocated_date
    """
    print("stm_bus_stop_cancelled_moved_relocated.csv import started")
    load_csv_to_neo4j(neo4j_driver, "./stm_bus_stop_cancelled_moved_relocated.csv", load_bus_stop_cancelled_moved_relocated_query)
    print("stm_bus_stop_cancelled_moved_relocated.csv import completed")

    load_metro_planned_kilometerage_query = """
    LOAD CSV WITH HEADERS FROM 'file:///stm_metro_planned_kilometerage.csv' AS row
    CREATE (mpk:MetroPlannedKilometerage {id: toInteger(row.stm_metro_planned_kilometerage_id), km: toInteger(row.planned_kilometerage), date: row.stm_metro_planned_kilometerage_date})
    WITH mpk, row
    MATCH (mr:MetroRoute {id: toInteger(row.stm_metro_route_id)})
    CREATE (mpk)-[:BELONGS_TO]->(mr)
    """
    print("stm_metro_planned_kilometerage.csv import started")
    load_csv_to_neo4j(neo4j_driver, "./stm_metro_planned_kilometerage.csv", load_metro_planned_kilometerage_query)
    print("stm_metro_planned_kilometerage.csv import completed")

    load_metro_realized_kilometerage_query = """
    LOAD CSV WITH HEADERS FROM 'file:///stm_metro_realized_kilometerage.csv' AS row
    CREATE (mrk:MetroRealizedKilometerage {id: toInteger(row.stm_metro_realized_kilometerage_id), km: toInteger(row.realized_kilometerage), date: row.stm_metro_realized_kilometerage_date})
    WITH mrk, row
    MATCH (mr:MetroRoute {id: toInteger(row.stm_metro_route_id)})
    CREATE (mrk)-[:BELONGS_TO]->(mr)
    """
    print("stm_metro_realized_kilometerage.csv import started")
    load_csv_to_neo4j(neo4j_driver, "./stm_metro_realized_kilometerage.csv", load_metro_realized_kilometerage_query)
    print("stm_metro_realized_kilometerage.csv import completed")

    load_incident_query = """
    LOAD CSV WITH HEADERS FROM 'file:///stm_incident.csv' AS row
    CREATE (i:Incident {id: toInteger(row.stm_incident_id), type: row.stm_incident_type, primary_cause: row.stm_incident_primary_cause, secondary_cause: row.stm_incident_secondary_cause, time_of_incident: row.stm_incident_time_of_incident, location_of_incident: row.stm_incident_location_of_incident})
    WITH i, row
    MATCH (mr:MetroRoute {id: toInteger(row.stm_metro_route_id)})
    CREATE (i)-[:AFFECTS]->(mr)
    """
    print("stm_incident.csv import started")
    load_csv_to_neo4j(neo4j_driver, "./stm_incident.csv", load_incident_query)
    print("stm_incident.csv import completed")

    load_live_bus_trip_query = """
    LOAD CSV WITH HEADERS FROM 'file:///live_stm_bus_trip.csv' AS row
    CREATE (lbt:LiveBusTrip {id: toInteger(row.live_stm_bus_trip_id), date: row.live_stm_bus_trip_date})
    WITH lbt, row
    MATCH (bt:BusTrip {id: toInteger(row.stm_bus_trip_id)})
    CREATE (lbt)-[:IS_LIVE]->(bt)
    """
    print("live_stm_bus_trip.csv import started")
    load_csv_to_neo4j(neo4j_driver, "./live_stm_bus_trip.csv", load_live_bus_trip_query)
    print("live_stm_bus_trip.csv import completed")

    load_live_bus_trip_stop_query = """
    LOAD CSV WITH HEADERS FROM 'file:///live_stm_bus_trip_stop.csv' AS row
    MATCH (lbt:LiveBusTrip {id: toInteger(row.live_stm_bus_trip_id)}), (bs:BusStop {id: row.stm_bus_stop_id})
    CREATE (lbt)-[:VISITS {arrival_time: row.live_stm_bus_stop_arrival_time, departure_time: row.live_stm_bus_stop_departure_time}]->(bs)
    """
    print("live_stm_bus_trip_stop.csv import started")
    load_csv_to_neo4j(neo4j_driver, "./live_stm_bus_trip_stop.csv", load_live_bus_trip_stop_query)
    print("live_stm_bus_trip_stop.csv import completed")

    load_mta_metro_route_query = """
    LOAD CSV WITH HEADERS FROM 'file:///mta_metro_route.csv' AS row
    CREATE (mr:MTA_MetroRoute {id: row.mta_metro_route_id, short_name: row.mta_metro_short_name, long_name: row.mta_metro_long_name, route_type: toInteger(row.mta_metro_route_type)})
    """
    print("mta_metro_route.csv import started")
    load_csv_to_neo4j(neo4j_driver, "./mta_metro_route.csv", load_mta_metro_route_query)
    print("mta_metro_route.csv import completed")

    load_mta_metro_stop_query = """
    LOAD CSV WITH HEADERS FROM 'file:///mta_metro_stop.csv' AS row
    CREATE (ms:MTA_MetroStop {id: toInteger(row.mta_metro_stop_id), name: row.mta_metro_stop_name, lat: toFloat(row.mta_metro_stop_latitude), lon: toFloat(row.mta_metro_stop_longitude)})
    """
    print("mta_metro_stop.csv import started")
    load_csv_to_neo4j(neo4j_driver, "./mta_metro_stop.csv", load_mta_metro_stop_query)
    print("mta_metro_stop.csv import completed")

    load_mta_metro_trip_query = """
    LOAD CSV WITH HEADERS FROM 'file:///mta_metro_trip.csv' AS row
    CREATE (mt:MTA_MetroTrip {id: toInteger(row.mta_metro_trip_id), headsign: row.mta_metro_trip_headsign, direction_id: toInteger(row.mta_metro_direction_id)})
    WITH mt, row
    MATCH (mr:MTA_MetroRoute {id: toInteger(row.mta_metro_route_id)})
    CREATE (mt)-[:FOLLOWS]->(mr)
    """
    print("mta_metro_trip.csv import started")
    load_csv_to_neo4j(neo4j_driver, "./mta_metro_trip.csv", load_mta_metro_trip_query)
    print("mta_metro_trip.csv import completed")

    load_mta_metro_stop_time_query = """
    LOAD CSV WITH HEADERS FROM 'file:///mta_metro_stop_time.csv' AS row
    MATCH (mt:MTA_MetroTrip {id: toInteger(row.mta_metro_stop_time_trip_id)}), (ms:MTA_MetroStop {id: toInteger(row.mta_metro_stop_time_stop_id)})
    CREATE (mt)-[:VISITS {sequence: toInteger(row.mta_metro_stop_time_stop_sequence), arrival_time: row.mta_metro_stop_arrival_time, departure_time: row.mta_metro_stop_departure_time}]->(ms)
    """
    print("mta_metro_stop_time.csv import started")
    load_csv_to_neo4j(neo4j_driver, "./mta_metro_stop_time.csv", load_mta_metro_stop_time_query)
    print("mta_metro_stop_time.csv import completed")

    print("Data loaded into Neo4j complete!")

# Run the load operation
if __name__ == "__main__":
    try:
        load_data()
    except Exception as e:
        print(f"Error during data loading: {e}")
