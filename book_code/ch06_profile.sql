-- Chapter 6: profile one column in SQL
SELECT
    COUNT(*)                          AS total_rows,
    COUNT(postcode)                   AS filled,
    COUNT(*) - COUNT(postcode)        AS missing,
    COUNT(DISTINCT postcode)          AS distinct_values,
    MIN(postcode)                     AS min_value,
    MAX(postcode)                     AS max_value
FROM deliveries;

-- The most common values: a quick way to spot unexpected codes
SELECT depot_code, COUNT(*) AS n_rows
FROM deliveries
GROUP BY depot_code
ORDER BY n_rows DESC;
