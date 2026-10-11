-- Chapter 10, check P01: does the join to depots lose rows?
WITH u AS (SELECT DISTINCT * FROM deliveries)
SELECT
    (SELECT COUNT(*) FROM u)                       AS before_join,
    (SELECT COUNT(*) FROM u
       JOIN depots p ON p.depot_code = u.depot_code) AS after_join;

-- The same check on the cleaned view
SELECT
    (SELECT COUNT(*) FROM deliveries_clean)        AS before_join,
    (SELECT COUNT(*) FROM deliveries_clean c
       JOIN depots p ON p.depot_code = c.depot_code) AS after_join;
