# Power BI Dashboard Plan

Power BI Desktop is Windows-only, so this project provides BI-ready CSV outputs that can be imported into Power BI on a Windows machine.

## Import These Files

- `data/processed/hourly_fraud_summary.csv`
- `data/processed/amount_bucket_risk.csv`
- `data/processed/high_value_fraud_sample.csv`
- `data/processed/fraud_kpis.json` for KPI values, or manually enter the KPI values shown in the README.

## Suggested Dashboard Layout

1. KPI Cards
   - Total transactions
   - Fraud transactions
   - Fraud rate
   - Fraud amount

2. Clustered Column Chart
   - Axis: `hour_of_day`
   - Values: `fraud_transactions`
   - Tooltip: `fraud_rate_percent`

3. Bar Chart
   - Axis: `amount_bucket`
   - Values: `fraud_rate_percent`

4. Table
   - Fields: `hour_of_day`, `amount`, `class`
   - Sort by: `amount` descending

## Example DAX Measures

```DAX
Fraud Rate % = DIVIDE(SUM(amount_bucket_risk[fraud_transactions]), SUM(amount_bucket_risk[transactions])) * 100

Total Fraud Transactions = SUM(amount_bucket_risk[fraud_transactions])

Total Transactions = SUM(amount_bucket_risk[transactions])

Total Fraud Amount = SUM(amount_bucket_risk[fraud_amount])
```
