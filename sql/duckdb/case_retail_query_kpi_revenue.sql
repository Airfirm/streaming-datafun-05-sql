-- sql/duckdb/case_retail_kpi_revenue.sql
-- ============================================================
-- PURPOSE
-- ============================================================
-- Calculate a Key Performance Indicator (KPI) for the retail domain using DuckDB SQL.
--
-- KPI DRIVES THE WORK:
-- In analytics, we do not start with "write a query."
-- We start with a KPI that supports an actionable decision.
--
-- ACTIONABLE OUTCOME (EXAMPLE):
-- We want to identify which stores are generating the most revenue so we can:
-- - allocate staffing during high-performing periods,
-- - increase inventory for top categories,
-- - investigate why low-performing stores are underperforming,
-- - target promotions where they will have the biggest impact.
--
-- In this example, our KPI is store revenue (total sales amount) by store.
--
-- ANALYST RESPONSIBILITY:
-- Analysts are responsible for determining HOW to get the information
-- that informs the KPI and supports action.
-- That means:
-- - identifying the needed tables,
-- - joining them correctly,
-- - selecting the right measures,
-- - aggregating at the correct level (store),
-- - and presenting results in a way that supports decision-making.
--
-- ASSUMPTION:
-- We always run all commands from the project root directory.
--
-- EXPECTED PROJECT PATHS (relative to repo root):
--   SQL:  sql/duckdb/case_retail_kpi_revenue.sql
--   DB:   artifacts/duckdb/retail.duckdb
--
--
-- ============================================================
-- TOPIC DOMAINS + 1:M RELATIONSHIPS
-- ============================================================
-- OUR DOMAIN: RETAIL
-- Two tables in a 1-to-many relationship (1:M):
-- - store (1): independent/parent table
-- - sale  (M): dependent/child table
--
-- HOW THIS RELATES TO OUR KPI:
-- - The store table tells us "which store" (store_id, store_name, location).
-- - The sale table contains the measurable activity (amount, quantity, category, date).
-- - To compute revenue by store, we must:
--   1) connect each sale to its store (JOIN on store_id),
--   2) aggregate sales amounts at the store level (GROUP BY store).
--
--
-- ============================================================
-- KPI DEFINITION
-- ============================================================
-- KPI NAME: Total Revenue by Store
--
-- KPI QUESTION:
-- "How much revenue did each store generate?"
--
-- MEASURE:
-- - revenue = SUM(sale.amount)
--
-- GRAIN (LEVEL OF DETAIL):
-- - one row per store
--
-- OUTPUT (WHAT DECISION-MAKERS NEED):
-- - store identifier and name
-- - total revenue
-- - optionally: number of sales and average sale amount
--
--
-- ============================================================
-- EXECUTION: GET THE INFORMATION THAT INFORMS THE KPI
-- ============================================================
-- Strategy:
-- - JOIN store (1) to sale (M)
-- - GROUP BY store
-- - SUM amounts to compute revenue
-- - ORDER results so we can quickly see top stores
--
SELECT
  s.store_id,
  s.store_name,
  s.city,
  s.region,
  COUNT(sa.sale_id) AS sale_count,
  ROUND(SUM(sa.amount), 2) AS total_revenue,
  ROUND(AVG(sa.amount), 2) AS avg_sale_amount
FROM store AS s
JOIN sale AS sa
  ON sa.store_id = s.store_id
GROUP BY
  s.store_id,
  s.store_name,
  s.city,
  s.region
ORDER BY total_revenue DESC;
