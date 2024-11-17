CREATE TABLE IF NOT EXISTS stm_metro_line(
    stm_metro_line_id INT PRIMARY KEY,
    line_name VARCHAR(255),
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
    stm_bus_stop_code INT
);

CREATE TABLE IF NOT EXISTS stm_metro_stop(
    stm_metro_stop_id VARCHAR(15) PRIMARY KEY,
    stm_metro_stop_name VARCHAR(255),
    stm_metro_stop_code INT
);

CREATE TABLE IF NOT EXISTS stm_metro_planned_kilometerage (
    stm_metro_planned_kilometerage_id INT PRIMARY KEY,
    stm_metro_line_id INT,
    planned_kilometerage INT,
    day_of_week VARCHAR(25),
    stm_metro_planned_kilometerage_date DATE,
    FOREIGN KEY (stm_metro_line_id) REFERENCES stm_metro_line(stm_metro_line_id)
);

CREATE TABLE IF NOT EXISTS stm_metro_realized_kilometrage (
    stm_metro_realized_kilometrage_id INT PRIMARY KEY,
    stm_metro_line_id INT,
    realized_kilometerage INT,
    day_of_week VARCHAR(25),
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
