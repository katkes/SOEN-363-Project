-- selects row where stm_bus_code is 54351
SELECT *
FROM stm_bus_stop_cancelled_moved_relocated
WHERE stm_bus_stop_code = 54351;

--total planned kilometerage for each metro line grouped by day of week
SELECT 
    stm_metro_line_id,
    day_of_week,
    SUM(planned_kilometerage) AS total_planned_kilometerage
FROM 
    stm_metro_planned_kilometerage
GROUP BY 
    stm_metro_line_id, day_of_week
ORDER BY 
    stm_metro_line_id, day_of_week;

-- Using simple JOIN
SELECT *
FROM stm_metro_realized_kilometrage rk JOIN stm_metro_line sl on rk.stm_metro_line_id = sl.stm_metro_line_id;
-- Using cartesian product and WHERE clause
SELECT *
FROM stm_metro_realized_kilometrage rk
CROSS JOIN stm_metro_line sl;
WHERE rk.stm_metro_line_id = sl.stm_metro_line_id;

--inner join
SELECT 
    b.stm_bus_stop_id, 
    b.stm_bus_stop_name, 
    c.stm_bus_stop_cancelled_moved_relocated_reason
FROM 
    stm_bus_stop b
INNER JOIN 
    stm_bus_stop_cancelled_moved_relocated c
ON 
    b.stm_bus_stop_code = c.stm_bus_stop_code;

--outer left join
SELECT 
    b.stm_bus_stop_id, 
    b.stm_bus_stop_name, 
    c.stm_bus_stop_cancelled_moved_relocated_reason
FROM 
    stm_bus_stop b
LEFT JOIN 
    stm_bus_stop_cancelled_moved_relocated c
ON 
    b.stm_bus_stop_code = c.stm_bus_stop_code;

--outer right join
SELECT 
    b.stm_bus_stop_id, 
    b.stm_bus_stop_name, 
    c.stm_bus_stop_cancelled_moved_relocated_reason
FROM 
    stm_bus_stop b
RIGHT JOIN 
    stm_bus_stop_cancelled_moved_relocated c
ON 
    b.stm_bus_stop_code = c.stm_bus_stop_code;

--full outer 
SELECT 
    b.stm_bus_stop_id, 
    b.stm_bus_stop_name, 
    c.stm_bus_stop_cancelled_moved_relocated_reason
FROM 
    stm_bus_stop b
FULL JOIN 
    stm_bus_stop_cancelled_moved_relocated c
ON 
    b.stm_bus_stop_code = c.stm_bus_stop_code;

--correlated queries
--above average kilometrage metro lines
SELECT 
    m.stm_metro_line_id,
    m.planned_kilometerage,
    m.day_of_week
FROM 
    stm_metro_planned_kilometerage m
WHERE 
    m.planned_kilometerage > (
        SELECT AVG(m2.planned_kilometerage)
        FROM stm_metro_planned_kilometerage m2
        WHERE m2.day_of_week = m.day_of_week
    );

--bus stops with more than one planned kilometerage entry
SELECT 
    p.stm_metro_line_id
FROM 
    stm_metro_planned_kilometerage p
WHERE 
    (SELECT COUNT(*)
     FROM stm_metro_planned_kilometerage p2
     WHERE p2.stm_metro_line_id = p.stm_metro_line_id) > 1;

--metro lines with planned kilometerage above the line average
SELECT 
    p.stm_metro_line_id,
    p.planned_kilometerage
FROM 
    stm_metro_planned_kilometerage p
WHERE 
    p.planned_kilometerage > (
        SELECT AVG(p2.planned_kilometerage)
        FROM stm_metro_planned_kilometerage p2
        WHERE p2.stm_metro_line_id = p.stm_metro_line_id
    );

--specific metro line incicents (green cuz its actually bad)
CREATE OR REPLACE VIEW green_line_incidents AS
SELECT 
    i.stm_incident_id,
    i.stm_incident_type,
    i.stm_incident_date_of_incident,
    i.stm_incident_location_of_incident
FROM 
    stm_incident i
JOIN 
    stm_metro_line m
ON 
    i.stm_metro_line_id = m.stm_metro_line_id
WHERE 
    m.line_colour = 'Green';

--bus stops with no cancellation or relocation (USING NOT IN)
SELECT stm_bus_stop_id
FROM stm_bus_stop
WHERE stm_bus_stop_id NOT IN (
    SELECT stm_bus_stop_id
    FROM stm_bus_stop_cancelled_moved_relocated
);

--using NOT EXISTS
SELECT stm_bus_stop_id
FROM stm_bus_stop bs
WHERE NOT EXISTS (
    SELECT 1
    FROM stm_bus_stop_cancelled_moved_relocated bsc
    WHERE bs.stm_bus_stop_id = bsc.stm_bus_stop_id
);

--using EXCEPT
SELECT stm_bus_stop_id
FROM stm_bus_stop
EXCEPT
SELECT stm_bus_stop_id
FROM stm_bus_stop_cancelled_moved_relocated;