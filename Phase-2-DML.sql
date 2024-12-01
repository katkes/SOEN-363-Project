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

-- Creating index for the first query (A basic search query on an attribute value.)
-- execution time without index: 52 ms
-- execution time with index: 1 ms
CREATE INDEX busStopNameIndex FOR (bs:BusStop) ON (bs.name);

-- Creating index for the second query [A query that provides some aggregate data (i.e. number of entities satisfying a criteria)]
-- execution time without index: 19 ms
-- execution time with index: 1 ms
CREATE INDEX StmMetroTripIdIndex FOR (mt:StmMetroTrip) ON (mt.id);

-- Creating index for the third query (Find top n entities satisfying a criteria, sorted by an attribute.)
-- execution time without index: 61 ms
-- execution time with index: 2 ms
CREATE INDEX busRouteIdIndex FOR (br:BusRoute) ON (br.id) -- index for the bus route id
CREATE INDEX busRouteNameIndex FOR (br:BusRoute) ON (br.name) -- index for the bus route name

-- Demonstrate a full text search. Show the performance improvement by using indexes.
-- execution time without indexes: 19 ms
-- execution time with indexes: 10 ms
MATCH (n:Incident) 
where n.secondary_cause contains 'Nuisance'
RETURN n
-- Index creation
CREATE FULLTEXT INDEX incidentSecondaryCauseIndex FOR (n:Incident) ON EACH [n.secondary_cause]
-- Fulltext search
CALL db.index.fulltext.queryNodes('incidentSecondaryCauseIndex', 'Nuisance') YIELD node, score
RETURN node.secondary_cause AS secondary_cause, score
ORDER BY score DESC;
