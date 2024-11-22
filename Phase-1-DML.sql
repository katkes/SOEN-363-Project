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