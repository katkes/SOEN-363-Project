CREATE DOMAIN planned_kilometerage AS INT CHECK (VALUE >= 0);
CREATE DOMAIN realized_kilometerage AS INT CHECK (VALUE >= 0);

CREATE TYPE day_of_week AS ENUM ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');
CREATE TYPE metro_colour AS ENUM ('Grean', 'Orange', 'Yellow', 'Blue');

CREATE TABLE IF NOT EXISTS stm_metro_line(
    stm_metro_line_id INT PRIMARY KEY,
    line_colour metro_colour,
    line_number INT
);

CREATE TABLE IF NOT EXISTS stm_bus_line(
    stm_bus_line_id INT PRIMARY KEY,
    line_name VARCHAR(255),
    line_number INT
);

CREATE TABLE IF NOT EXISTS stm_bus_stop(
    stm_bus_stop_id VARCHAR(15) PRIMARY KEY,
    stm_bus_top_name VARCHAR(255),
    stm_bus_stop_code INT,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS stm_bus_stop_cancelled_moved_relocated(
    stm_bus_stop_cancelled_moved_relocated_id INT,
    stm_bus_stop_id VARCHAR(15),
    stm_bus_stop_name VARCHAR(255),
    stm_bus_stop_code INT,
    stm_bus_stop_cancelled_moved_relocated_date DATE,
    stm_bus_stop_cancelled_moved_relocated_reason VARCHAR(255),
    PRIMARY KEY (stm_bus_stop_id, stm_bus_stop_cancelled_moved_relocated_date),
    FOREIGN KEY (stm_bus_stop_id) REFERENCES stm_bus_stop(stm_bus_stop_id) ON DELETE CASCADE
)

CREATE TABLE IF NOT EXISTS stm_metro_stop(
    stm_metro_stop_id VARCHAR(15) PRIMARY KEY,
    stm_metro_stop_name VARCHAR(255),
    stm_metro_stop_code INT
);

CREATE TABLE IF NOT EXISTS stm_metro_planned_kilometerage (
    stm_metro_planned_kilometerage_id INT PRIMARY KEY,
    stm_metro_line_id INT,
    planned_kilometerage INT,
    day_of_week day_of_week,
    stm_metro_planned_kilometerage_date DATE,
    FOREIGN KEY (stm_metro_line_id) REFERENCES stm_metro_line(stm_metro_line_id)
);

CREATE TABLE IF NOT EXISTS stm_metro_realized_kilometrage (
    stm_metro_realized_kilometrage_id INT PRIMARY KEY,
    stm_metro_line_id INT,
    realized_kilometerage INT,
    day_of_week_or_type_of_day VARCHAR(25),
    stm_metro_realized_kilometrage_date DATE,
    FOREIGN KEY (stm_metro_line_id) REFERENCES stm_metro_line(stm_metro_line_id)
);

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
    SET is_active = FALSE
    WHERE stm_bus_stop_id = NEW.stm_bus_stop_id;

    RETURN NEW;
END;

-- Create a trigger to call the function before insert
CREATE TRIGGER trg_update_bus_stop_inactive
    AFTER INSERT ON stm_bus_stop_cancelled_moved_relocated
    FOR EACH ROW
    EXECUTE FUNCTION update_bus_stop_inactive();