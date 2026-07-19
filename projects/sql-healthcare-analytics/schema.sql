DROP TABLE IF EXISTS lab_results;
DROP TABLE IF EXISTS diagnoses;
DROP TABLE IF EXISTS admissions;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS patients;

CREATE TABLE patients (
    patient_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    gender TEXT NOT NULL
);

CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL,
    specialty TEXT NOT NULL
);

CREATE TABLE appointments (
    appointment_id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    appointment_date TEXT NOT NULL,
    status TEXT NOT NULL,
    wait_days INTEGER NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE admissions (
    admission_id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    admission_date TEXT NOT NULL,
    discharge_date TEXT NOT NULL,
    admission_type TEXT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE diagnoses (
    diagnosis_id INTEGER PRIMARY KEY,
    admission_id INTEGER NOT NULL,
    diagnosis_code TEXT NOT NULL,
    diagnosis_description TEXT NOT NULL,
    severity TEXT NOT NULL,
    FOREIGN KEY (admission_id) REFERENCES admissions(admission_id)
);

CREATE TABLE lab_results (
    result_id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    test_name TEXT NOT NULL,
    result_value REAL NOT NULL,
    result_unit TEXT NOT NULL,
    result_flag TEXT NOT NULL,
    result_date TEXT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);
