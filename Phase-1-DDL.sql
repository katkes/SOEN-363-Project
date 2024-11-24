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
)

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