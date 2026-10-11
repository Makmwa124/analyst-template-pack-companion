-- Appendix B, example 1: failed first attempts, South East, June
-- Reads the cleaned view (run ch10_clean_view.sql first)
SELECT
    p.depot_name,
    COUNT(*)                                            AS consignments,
    SUM(c.status = 'Failed attempt')                    AS failed,
    ROUND(100.0 * SUM(c.status = 'Failed attempt')
          / COUNT(*), 1)                                AS failed_pct
FROM deliveries_clean c
JOIN depots p ON p.depot_code = c.depot_code
WHERE p.region = 'South East'
  AND c.status <> 'Cancelled'
  AND c.promised_date BETWEEN '2026-06-01' AND '2026-06-30'
GROUP BY p.depot_name
ORDER BY failed_pct DESC;
