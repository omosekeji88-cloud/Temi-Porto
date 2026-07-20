-- These queries are written for the processed dashboard CSVs after importing them into a SQL database.

-- 1. Highest fraud-rate hours
SELECT
    hour_of_day,
    transactions,
    fraud_transactions,
    fraud_rate_percent
FROM hourly_fraud_summary
ORDER BY fraud_rate_percent DESC
LIMIT 10;

-- 2. Fraud risk by transaction amount bucket
SELECT
    amount_bucket,
    transactions,
    fraud_transactions,
    fraud_rate_percent,
    fraud_amount
FROM amount_bucket_risk
ORDER BY fraud_rate_percent DESC;

-- 3. Share of fraud value by amount bucket
SELECT
    amount_bucket,
    fraud_amount,
    ROUND(100.0 * fraud_amount / SUM(fraud_amount) OVER (), 2) AS share_of_fraud_value_percent
FROM amount_bucket_risk
ORDER BY share_of_fraud_value_percent DESC;

-- 4. High-value fraud transactions for investigation
SELECT
    hour_of_day,
    amount,
    class
FROM high_value_fraud_sample
ORDER BY amount DESC;
