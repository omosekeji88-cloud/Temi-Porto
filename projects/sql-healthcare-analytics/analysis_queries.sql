-- 1. Appointment no-show rate by department
SELECT
    d.department_name,
    COUNT(*) AS total_appointments,
    SUM(CASE WHEN a.status = 'No-show' THEN 1 ELSE 0 END) AS no_shows,
    ROUND(100.0 * SUM(CASE WHEN a.status = 'No-show' THEN 1 ELSE 0 END) / COUNT(*), 1) AS no_show_rate_percent
FROM appointments AS a
JOIN departments AS d
    ON a.department_id = d.department_id
GROUP BY d.department_name
ORDER BY no_show_rate_percent DESC;

-- 2. Average waiting time by department
SELECT
    d.department_name,
    ROUND(AVG(a.wait_days), 1) AS average_wait_days,
    MAX(a.wait_days) AS longest_wait_days
FROM appointments AS a
JOIN departments AS d
    ON a.department_id = d.department_id
GROUP BY d.department_name
ORDER BY average_wait_days DESC;

-- 3. Average length of stay by admission department
SELECT
    d.department_name,
    COUNT(*) AS admission_count,
    ROUND(AVG(julianday(ad.discharge_date) - julianday(ad.admission_date)), 1) AS average_length_of_stay_days
FROM admissions AS ad
JOIN departments AS d
    ON ad.department_id = d.department_id
GROUP BY d.department_name
ORDER BY average_length_of_stay_days DESC;

-- 4. Possible 30-day readmissions
WITH admission_sequence AS (
    SELECT
        patient_id,
        admission_id,
        admission_date,
        discharge_date,
        LEAD(admission_date) OVER (
            PARTITION BY patient_id
            ORDER BY admission_date
        ) AS next_admission_date
    FROM admissions
)
SELECT
    p.first_name || ' ' || p.last_name AS patient_name,
    admission_id,
    discharge_date,
    next_admission_date,
    CAST(julianday(next_admission_date) - julianday(discharge_date) AS INTEGER) AS days_until_readmission
FROM admission_sequence AS seq
JOIN patients AS p
    ON seq.patient_id = p.patient_id
WHERE next_admission_date IS NOT NULL
  AND julianday(next_admission_date) - julianday(discharge_date) <= 30
ORDER BY days_until_readmission;

-- 5. Abnormal lab-result rate by test
SELECT
    test_name,
    COUNT(*) AS total_tests,
    SUM(CASE WHEN result_flag != 'Normal' THEN 1 ELSE 0 END) AS abnormal_results,
    ROUND(100.0 * SUM(CASE WHEN result_flag != 'Normal' THEN 1 ELSE 0 END) / COUNT(*), 1) AS abnormal_rate_percent
FROM lab_results
GROUP BY test_name
ORDER BY abnormal_rate_percent DESC, total_tests DESC;

-- 6. Monthly appointment demand
SELECT
    strftime('%Y-%m', appointment_date) AS appointment_month,
    COUNT(*) AS appointment_count,
    SUM(CASE WHEN status = 'Attended' THEN 1 ELSE 0 END) AS attended_count
FROM appointments
GROUP BY strftime('%Y-%m', appointment_date)
ORDER BY appointment_month;

-- 7. High-priority follow-up list
SELECT
    p.first_name || ' ' || p.last_name AS patient_name,
    d.department_name,
    dx.diagnosis_description,
    dx.severity,
    lr.test_name,
    lr.result_value,
    lr.result_unit,
    lr.result_flag
FROM diagnoses AS dx
JOIN admissions AS ad
    ON dx.admission_id = ad.admission_id
JOIN patients AS p
    ON ad.patient_id = p.patient_id
JOIN departments AS d
    ON ad.department_id = d.department_id
LEFT JOIN lab_results AS lr
    ON p.patient_id = lr.patient_id
WHERE dx.severity = 'High'
   OR lr.result_flag = 'High'
ORDER BY dx.severity DESC, patient_name;
