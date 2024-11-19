from datetime import datetime
from Creds import connection

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

