import psycopg
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
POSTGRES_PASS = os.getenv("POSTGRES_PASS")

# Define the project folder and CSV directory
project_folder = os.getcwd()  # This will set the current working directory as the project folder
csv_directory = os.path.join(project_folder, "CSVforNeo4j")

# Create the CSVforNeo4j folder if it doesn't exist
if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)

# PostgreSQL connection details
pg_conn = psycopg.connect(
    host="localhost",
    dbname="SOEN-363-Project",
    user="postgres",
    password=POSTGRES_PASS,
    port=5432
)
pg_cursor = pg_conn.cursor()
conn_engine = "postgresql+psycopg://postgres:YSU-1231@localhost:5432/SOEN-363-Project"

# Export table to CSV from PostgreSQL
def export_to_csv(query, output_file):
    with open(output_file, "w") as f:
        pg_cursor.copy_expert(f"COPY ({query}) TO STDOUT WITH CSV HEADER", f)

# NOTE: This is for middy to export the db to csv files since psycopg2 doesn't work on my machine and psycopg does not have a .copy_expert() method
# def export_to_csv(query, output_file):
#     df = pd.read_sql_query(query, conn_engine, index_col=None)
#     df.to_csv(output_file)
#     print(f"{os.path.basename(output_file)} succefully populated.")

# Main function to export data
def migrate_data():
    # PostgreSQL queries to export data into CSV files
    stm_route_query = "SELECT * FROM stm_route"
    stm_route_file = os.path.join(csv_directory, "stm_route.csv")
    export_to_csv(stm_route_query, stm_route_file)

    stm_metro_route_query = "SELECT * FROM stm_metro_route"
    stm_metro_route_file = os.path.join(csv_directory, "stm_metro_route.csv")
    export_to_csv(stm_metro_route_query, stm_metro_route_file)

    stm_bus_route_query = "SELECT * FROM stm_bus_route"
    stm_bus_route_file = os.path.join(csv_directory, "stm_bus_route.csv")
    export_to_csv(stm_bus_route_query, stm_bus_route_file)

    stm_bus_stop_query = "SELECT * FROM stm_bus_stop"
    stm_bus_stop_file = os.path.join(csv_directory, "stm_bus_stop.csv")
    export_to_csv(stm_bus_stop_query, stm_bus_stop_file)

    stm_metro_stop_query = "SELECT * FROM stm_metro_stop"
    stm_metro_stop_file = os.path.join(csv_directory, "stm_metro_stop.csv")
    export_to_csv(stm_metro_stop_query, stm_metro_stop_file)

    stm_metro_trip_query = "SELECT * FROM stm_metro_trip"
    stm_metro_trip_file = os.path.join(csv_directory, "stm_metro_trip.csv")
    export_to_csv(stm_metro_trip_query, stm_metro_trip_file)

    stm_bus_trip_query = "SELECT * FROM stm_bus_trip"
    stm_bus_trip_file = os.path.join(csv_directory, "stm_bus_trip.csv")
    export_to_csv(stm_bus_trip_query, stm_bus_trip_file)

    stm_metro_stop_time_query = "SELECT * FROM stm_metro_stop_time"
    stm_metro_stop_time_file = os.path.join(csv_directory, "stm_metro_stop_time.csv")
    export_to_csv(stm_metro_stop_time_query, stm_metro_stop_time_file)

    # NOTE: This exports all the rows, for the load_to_neo4j script, only keep the first 50 000 rows and delete the rest
    stm_bus_stop_time_query = "SELECT * FROM stm_bus_stop_time"
    stm_bus_stop_time_file = os.path.join(csv_directory, "stm_bus_stop_time.csv")
    export_to_csv(stm_bus_stop_time_query, stm_bus_stop_time_file)

    stm_bus_stop_cancelled_moved_relocated_query = "SELECT * FROM stm_bus_stop_cancelled_moved_relocated"
    stm_bus_stop_cancelled_moved_relocated_file = os.path.join(csv_directory, "stm_bus_stop_cancelled_moved_relocated.csv")
    export_to_csv(stm_bus_stop_cancelled_moved_relocated_query, stm_bus_stop_cancelled_moved_relocated_file)

    stm_metro_planned_kilometerage_query = "SELECT * FROM stm_metro_planned_kilometerage"
    stm_metro_planned_kilometerage_file = os.path.join(csv_directory, "stm_metro_planned_kilometerage.csv")
    export_to_csv(stm_metro_planned_kilometerage_query, stm_metro_planned_kilometerage_file)

    stm_metro_realized_kilometerage_query = "SELECT * FROM stm_metro_realized_kilometerage"
    stm_metro_realized_kilometerage_file = os.path.join(csv_directory, "stm_metro_realized_kilometerage.csv")
    export_to_csv(stm_metro_realized_kilometerage_query, stm_metro_realized_kilometerage_file)

    stm_incident_query = "SELECT * FROM stm_incident"
    stm_incident_file = os.path.join(csv_directory, "stm_incident.csv")
    export_to_csv(stm_incident_query, stm_incident_file)

    live_stm_bus_trip_query = "SELECT * FROM live_stm_bus_trip"
    live_stm_bus_trip_file = os.path.join(csv_directory, "live_stm_bus_trip.csv")
    export_to_csv(live_stm_bus_trip_query, live_stm_bus_trip_file)

    live_stm_bus_trip_stop_query = "SELECT * FROM live_stm_bus_trip_stop"
    live_stm_bus_trip_stop_file = os.path.join(csv_directory, "live_stm_bus_trip_stop.csv")
    export_to_csv(live_stm_bus_trip_stop_query, live_stm_bus_trip_stop_file)

    mta_metro_route_query = "SELECT * FROM mta_metro_route"
    mta_metro_route_file = os.path.join(csv_directory, "mta_metro_route.csv")
    export_to_csv(mta_metro_route_query, mta_metro_route_file)

    mta_metro_stop_query = "SELECT * FROM mta_metro_stop"
    mta_metro_stop_file = os.path.join(csv_directory, "mta_metro_stop.csv")
    export_to_csv(mta_metro_stop_query, mta_metro_stop_file)

    mta_metro_trip_query = "SELECT * FROM mta_metro_trip"
    mta_metro_trip_file = os.path.join(csv_directory, "mta_metro_trip.csv")
    export_to_csv(mta_metro_trip_query, mta_metro_trip_file)

    # NOTE: This export only takes the first 50 000
    mta_metro_stop_time_query = "SELECT * FROM mta_metro_stop_time LIMIT 50000"
    mta_metro_stop_time_file = os.path.join(csv_directory, "mta_metro_stop_time.csv")
    export_to_csv(mta_metro_stop_time_query, mta_metro_stop_time_file)

    print("Data migration complete!")

# Close PostgreSQL connection
def close_connections():
    pg_cursor.close()
    pg_conn.close()

# Run the migration
if __name__ == "__main__":
    try:
        migrate_data()
    except Exception as e:
        print(f"Error during migration: {e}")
    finally:
        close_connections()
