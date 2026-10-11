-- Chapter 10: apply the logged fixes (decisions D01 to D04) in one view
DROP VIEW IF EXISTS deliveries_clean;

CREATE VIEW deliveries_clean AS
-- D01: DISTINCT drops the re-imported duplicates
SELECT DISTINCT
    consignment_id,
    customer_id,
    -- D02: PAU is a keying error for Port Augusta
    CASE WHEN depot_code = 'PAU' THEN 'PAG'
         ELSE depot_code END AS depot_code,
    service_level,
    booked_at,
    promised_date,
    delivered_at,
    status,
    -- D03: weights of zero or less become NULL
    CASE WHEN weight_kg > 0 THEN weight_kg END AS weight_kg,
    cartons,
    postcode,
    -- D04: clock errors are kept but flagged
    CASE WHEN delivered_at < booked_at THEN 1 ELSE 0 END
        AS exclude_from_otd
FROM deliveries;

SELECT COUNT(*) AS clean_rows, SUM(exclude_from_otd) AS flagged_rows
FROM deliveries_clean;
