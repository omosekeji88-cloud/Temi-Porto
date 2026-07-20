# Finance Fraud Analytics Dashboard

This portfolio project uses the Kaggle credit card fraud dataset to create a finance-focused BI dashboard.

The raw dataset is intentionally not committed to GitHub because it is large. Instead, this project includes processed dashboard outputs and a reproducible build script.

## Dataset

- Source: Kaggle `mlg-ulb/creditcardfraud`
- Dataset page: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- License: DbCL-1.0
- Raw records analysed: 284,807
- Confirmed fraud records: 492
- Fraud rate: 0.173%

## What This Project Shows

- Finance analytics and fraud monitoring
- Working with an imbalanced classification dataset
- Building BI-ready summary tables
- Creating dashboard KPIs
- Segmenting risk by transaction amount and time of day
- Communicating insights clearly for stakeholders

## Files

- `dashboard.html` is the finished dashboard.
- `data/processed/fraud_kpis.json` contains the KPI values.
- `data/processed/hourly_fraud_summary.csv` is ready for Power BI, Excel or Tableau.
- `data/processed/amount_bucket_risk.csv` is ready for dashboard visuals.
- `data/processed/high_value_fraud_sample.csv` contains a small fraud sample for review tables.
- `sql/analysis_queries.sql` contains SQL-style analysis queries for the processed data.
- `scripts/build_dashboard.py` rebuilds the dashboard from the Kaggle raw file.
- `power_bi_dashboard_plan.md` explains how to recreate the dashboard in Power BI.

## How To Rebuild

Download the raw Kaggle dataset into `data/raw/creditcard.csv`, then run:

```bash
python scripts/build_dashboard.py
```

The script creates the processed CSVs and dashboard HTML.

## Portfolio Summary

Built a finance fraud analytics dashboard using the Kaggle credit-card fraud dataset. The project transforms raw transaction records into BI-ready summaries and dashboard visuals covering fraud rate, transaction volume, amount-based risk and high-value fraud cases.
