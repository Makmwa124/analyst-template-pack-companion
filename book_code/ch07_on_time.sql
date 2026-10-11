-- Chapter 7: on-time delivery rate, agreed definition (card OTD-01)
-- Numerator: delivered on or before the promised date
-- Denominator: promised in the month, excluding cancellations
WITH unique_deliveries AS (
    SELECT DISTINCT * FROM deliveries
),
flagged AS (
    SELECT p.region,
           substr(u.promised_date, 1, 7) AS promised_month,
           CASE WHEN substr(u.delivered_at, 1, 10) <= u.promised_date
                THEN 1 ELSE 0 END        AS on_time
    FROM unique_deliveries u
    JOIN depots p ON p.depot_code = u.depot_code
    WHERE u.status <> 'Cancelled'
      AND p.region = 'Northern'
      AND u.promised_date BETWEEN '2026-01-01' AND '2026-06-30'
)
SELECT region,
       promised_month,
       COUNT(*)                                 AS due,
       SUM(on_time)                             AS on_time,
       ROUND(100.0 * SUM(on_time) / COUNT(*), 1) AS on_time_pct
FROM flagged
GROUP BY region, promised_month
ORDER BY promised_month;
