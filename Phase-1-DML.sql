-- Task : Basic select with simple where clause.
-- Done : Selects row where stm_bus_code is 54351
SELECT *
FROM stm_bus_stop_cancelled_moved_relocated
WHERE stm_bus_stop_code = 54351;

-- Task : Basic select with simple group by clause (with and without having clause).
-- Done : Total planned kilometerage for each metro line grouped by day of week
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

-- Task: A simple join query as well as its equivalent implementation using cartesian product and where clause.
-- Done: Using simple JOIN
SELECT *
FROM stm_metro_realized_kilometrage rk JOIN stm_metro_line sl on rk.stm_metro_line_id = sl.stm_metro_line_id;

-- Task: A simple join query as well as its equivalent implementation using cartesian product and where clause.
-- Done: Using cartesian product and WHERE clause
SELECT *
FROM stm_metro_realized_kilometrage rk
CROSS JOIN stm_metro_line sl;
WHERE rk.stm_metro_line_id = sl.stm_metro_line_id;

-- Task: A few queries to demonstrate various join types on the same tables: inner vs. outer (left and right) vs. full join. Use of null values in the database to show the differences is required.
-- Done: Inner join
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

-- Task: A few queries to demonstrate various join types on the same tables: inner vs. outer (left and right) vs. full join. Use of null values in the database to show the differences is required.
-- Done: Outer left join
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

-- Task: A few queries to demonstrate various join types on the same tables: inner vs. outer (left and right) vs. full join. Use of null values in the database to show the differences is required.
-- Done: Outer right join
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
    
-- Task: A few queries to demonstrate various join types on the same tables: inner vs. outer (left and right) vs. full join. Use of null values in the database to show the differences is required.
-- Done: Full outer 
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


-- Task: A few queries to demonstrate use of Null values for undefined / non-applicable.
-- Done:



-- Task: A couple of examples to demonstrate correlated queries.
-- Done: Display above average kilometrage metro lines using correlated queries
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


-- Task: One example per set operations: intersect, union, and difference vs. their equivalences
-- Done:



-- Task: An example of a view that has a hard-coded criteria, by which the content of the view may change upon changing the hard-coded value.
-- Done: View the incidents on a specific line (Green line) 
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


-- Task: Two implementations of the division operator using a) a regular nested query using NOT IN and b) a correlated nested query using NOT EXISTS and EXCEPT
-- Done: Bus stops with no cancellation or relocation (USING NOT IN)
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

-- demonstrating use of null values for undefined / non-applicable
SELECT * 
FROM stm_bus_stop sbs LEFT JOIN stm_bus_stop_cancelled_moved_relocated sbsc ON sbs.stm_bus_stop_id = sbsc.stm_bus_stop_id;

-- Using INTERSECT
SELECT stm_metro_line_id
FROM stm_incident
WHERE stm_incident_primary_cause = 'Clientèle'
INTERSECT
SELECT stm_metro_line_id
FROM stm_metro_realized_kilometrage
WHERE realized_kilometerage > 160;

-- Achieving INTERSECT without using set operations
SELECT stm_metro_line_id
FROM stm_incident
WHERE stm_incident_primary_cause = 'Clientèle'
AND stm_metro_line_id IN
(SELECT stm_metro_line_id
FROM stm_metro_realized_kilometrage
WHERE realized_kilometerage > 160)
GROUP BY stm_metro_line_id;

-- Using UNION
SELECT stm_metro_line_id
FROM stm_incident
WHERE stm_incident_primary_cause = 'Clientèle'
UNION
SELECT stm_metro_line_id
FROM stm_metro_realized_kilometrage
WHERE realized_kilometerage > 160;

-- Achieving UNION without using set operations
SELECT stm_metro_line_id
FROM stm_incident
WHERE stm_incident_primary_cause = 'Clientèle'
OR stm_metro_line_id IN
(SELECT stm_metro_line_id
FROM stm_metro_realized_kilometrage
WHERE realized_kilometerage > 160)
GROUP BY stm_metro_line_id
ORDER BY stm_metro_line_id DESC;

-- Using Differences (EXCEPT)
SELECT stm_metro_line_id
FROM stm_incident
WHERE stm_incident_primary_cause = 'Clientèle'
EXCEPT
SELECT stm_metro_line_id
FROM stm_metro_line
WHERE line_colour = 'Green';

-- Achieving EXCEPT without using set operations
SELECT stm_metro_line_id
FROM stm_incident
WHERE stm_incident_primary_cause = 'Clientèle'
AND stm_metro_line_id NOT IN
(SELECT stm_metro_line_id
FROM stm_metro_line
WHERE line_colour = 'Green')
GROUP BY stm_metro_line_id
ORDER BY stm_metro_line_id DESC;

-- Task: Two queries that demonstrate the overlap and covering constraints.
-- Done: Query to demonstrate overlap constraint
SELECT 
    bs.stm_bus_stop_id, 
    bs.stm_bus_stop_name, 
    c.stm_bus_stop_cancelled_moved_relocated_date, 
    c.stm_bus_stop_cancelled_moved_relocated_reason
FROM 
    stm_bus_stop bs
JOIN 
    stm_bus_stop_cancelled_moved_relocated c
ON 
    b.stm_bus_stop_id = c.stm_bus_stop_id;

-- Task: Two queries that demonstrate the overlap and covering constraints.
-- Done: Query to demonstrate covering constraint
SELECT 
    bs.stm_bus_stop_id, 
    bs.stm_bus_stop_name
FROM 
    stm_bus_stop b
LEFT JOIN 
    stm_bus_stop_cancelled_moved_relocated c
ON 
    b.stm_bus_stop_id = c.stm_bus_stop_id
WHERE 
    c.stm_bus_stop_id IS NULL;