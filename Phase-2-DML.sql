-- A basic search query on an attribute value.
MATCH (bs:BusStop {name: 'Station Guy-Concordia'})
RETURN bs;

-- A query that provides some aggregate data (i.e. number of entities satisfying a criteria)
MATCH (mt:StmMetroTrip)
RETURN COUNT(mt) AS TotalMetroTrips;

-- Find top n entities satisfying a criteria, sorted by an attribute.
MATCH (br:BusRoute)
WHERE br.id > 100 
RETURN br
ORDER BY br.name ASC  
LIMIT 5;