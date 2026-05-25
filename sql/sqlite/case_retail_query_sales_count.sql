-- sql/sqlite/case_retail_query_sales_count.sql
-- ============================================================
-- PURPOSE
-- ============================================================
-- Answer a basic activity question:
-- "How many sales events have occurred?"
--
-- This query operates on the dependent/child table.
--
-- WHY:
-- - Volume and revenue are different signals
-- - A store may have many small sales or few large ones
-- - Analysts often start by understanding event counts
--   before analyzing monetary impact

SELECT
  COUNT(*) AS sale_count
FROM sale;
