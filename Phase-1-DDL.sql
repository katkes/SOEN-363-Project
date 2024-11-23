CREATE DOMAIN planned_kilometerage AS INT CHECK (VALUE >= 0);
CREATE DOMAIN realized_kilometerage AS INT CHECK (VALUE >= 0);

CREATE TYPE day_of_week AS ENUM ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');
CREATE TYPE metro_colour AS ENUM ('Green', 'Orange', 'Yellow', 'Blue');

CREATE TABLE IF NOT EXISTS stm_bus(
    stm_bus_id INT PRIMARY KEY,
    stm_bus_number INT NOT NULL CHECK (stm_bus_number > 0),
    stm_bus_capacity INT NOT NULL CHECK (stm_bus_capacity > 0)
);

CREATE TABLE IF NOT EXISTS stm_metro_route(
    stm_metro_route_id INT PRIMARY KEY,
    stm_metro_route_colour metro_colour NOT NULL,
    stm_route_number INT NOT NULL CHECK (stm_route_number > 0)
);

CREATE TABLE IF NOT EXISTS stm_bus_route(
    stm_bus_route_id INT PRIMARY KEY,
    stm_route_name VARCHAR(255) NOT NULL,
    stm_route_number INT NOT NULL CHECK (stm_route_number > 0)
);

CREATE TABLE IF NOT EXISTS stm_metro_trip(
    stm_metro_trip_id INT PRIMARY KEY,
    stm_metro_trip_route_id INT,
    stm_metro_trip_service_id VARCHAR(255) NOT NULL,
    stm_metro_trip_trip_headsign VARCHAR(255) NOT NULL,
    stm_metro_trip_direction_id INT NOT NULL CHECK (stm_metro_trip_direction_id = 0 OR stm_metro_trip_direction_id = 1),
    FOREIGN KEY (stm_metro_trip_route_id) REFERENCES stm_metro_route(stm_metro_route_id)
);

CREATE TABLE IF NOT EXISTS stm_bus_trip(
    stm_bus_trip_id INT PRIMARY KEY,
    stm_bus_trip_route_id INT,
    stm_bus_trip_service_id VARCHAR(255) NOT NULL,
    stm_bus_trip_headsign VARCHAR(255) NOT NULL,
    stm_bus_trip_direction_id INT NOT NULL CHECK (stm_bus_trip_direction_id = 0 OR stm_bus_trip_direction_id = 1),
    FOREIGN KEY (stm_bus_trip_route_id) REFERENCES stm_bus_route(stm_bus_route_id)
);

CREATE TABLE IF NOT EXISTS stm_bus_stop(
    stm_bus_stop_id VARCHAR(15) PRIMARY KEY,
    stm_bus_stop_name VARCHAR(255) NOT NULL,
    stm_bus_stop_code INT NOT NULL CHECK (stm_bus_stop_code > 0),
    stm_bus_stop_location_type VARCHAR(255) NOT NULL,
    stm_bus_stop_latitude DECIMAL(9, 6) NOT NULL,
    stm_bus_stop_longitude DECIMAL(9, 6) NOT NULL,
    stm_bus_stop_is_wheelchair_accessible BOOLEAN DEFAULT FALSE,
    stm_bus_stop_is_active BOOLEAN DEFAULT TRUE,
);

CREATE TABLE IF NOT EXISTS stm_metro_stop(
    stm_metro_stop_id VARCHAR(15) PRIMARY KEY,
    stm_metro_stop_name VARCHAR(255) NOT NULL,
    stm_metro_stop_code INT NOT NULL CHECK (stm_metro_stop_code > 0),
    stm_metro_stop_location_type VARCHAR(255) NOT NULL,
    stm_metro_stop_latitude DECIMAL(9, 6) NOT NULL,
    stm_metro_stop_longitude DECIMAL(9, 6) NOT NULL,
    stm_metro_stop_is_wheelchair_accessible BOOLEAN DEFAULT FALSE
);

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

CREATE TABLE IF NOT EXISTS stm_bus_stop_cancelled_moved_relocated(
    stm_bus_stop_cancelled_moved_relocated_id INT PRIMARY KEY,
    stm_bus_stop_id VARCHAR(15) NOT NULL,
    stm_bus_stop_code INT NOT NULL CHECK (stm_bus_stop_code > 0),
    stm_bus_stop_cancelled_moved_relocated_date DATE NOT NULL,
    stm_bus_stop_cancelled_moved_relocated_reason TEXT NOT NULL,
    FOREIGN KEY (stm_bus_stop_id) REFERENCES stm_bus_stop(stm_bus_stop_id) ON DELETE CASCADE
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

-- Create a trigger function to enforce referential integrity: Updating the bus stop's active status to false if it is placed in the stm_bus_stop_cancelled_moved_relocated table
CREATE FUNCTION update_bus_stop_inactive()
BEGIN
    -- Update the associated bus stop's active status to false
    UPDATE stm_bus_stop
    SET stm_bus_stop_is_active = FALSE
    WHERE stm_bus_stop_code = NEW.stm_bus_stop_code;

    RETURN NEW;
END;

-- Create a trigger to call the function before insert
CREATE TRIGGER trg_update_bus_stop_inactive
    AFTER INSERT ON stm_bus_stop_cancelled_moved_relocated
    FOR EACH ROW
    EXECUTE FUNCTION update_bus_stop_inactive();