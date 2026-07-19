# Healthcare Appointment and Admissions SQL Analytics

This project uses SQL to explore a small healthcare dataset containing patients, departments, appointments, hospital admissions, diagnoses and lab results.

It was designed as a portfolio project to demonstrate data analyst skills in a healthcare context, including:

- Writing SQL joins across related tables
- Aggregating and grouping operational healthcare data
- Using common table expressions (CTEs)
- Calculating appointment no-show rates
- Measuring hospital length of stay
- Flagging possible 30-day readmissions
- Analysing abnormal lab results
- Turning raw records into useful business and clinical insights

## Project Question

How can appointment, admission and lab-result data be queried to identify service demand, patient follow-up priorities and operational patterns?

## Files

- `schema.sql` creates the database tables.
- `seed_data.sql` inserts a realistic sample dataset.
- `analysis_queries.sql` contains the main SQL analysis queries.
- `run_analysis.py` runs the SQL analysis using Python's built-in SQLite support.

## How To Run

From this folder:

```bash
python run_analysis.py
```

No extra packages are required because the project uses Python's built-in `sqlite3` module.

## Key Insights Demonstrated

The queries show how SQL can help answer practical analyst questions, such as:

- Which departments have the highest appointment no-show rates?
- Which hospital departments have the longest average stays?
- Which patients may need follow-up after a possible 30-day readmission?
- Which lab tests are producing the highest rate of abnormal results?
- How does appointment demand change month by month?
