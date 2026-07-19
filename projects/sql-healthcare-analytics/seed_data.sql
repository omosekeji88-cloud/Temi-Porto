INSERT INTO patients VALUES
(1, 'Aisha', 'Williams', '1997-04-18', 'Female'),
(2, 'Daniel', 'Smith', '1989-09-02', 'Male'),
(3, 'Maya', 'Patel', '2001-12-11', 'Female'),
(4, 'James', 'Brown', '1978-03-29', 'Male'),
(5, 'Leah', 'Johnson', '1994-06-07', 'Female'),
(6, 'Samuel', 'Okafor', '1982-11-15', 'Male'),
(7, 'Grace', 'Taylor', '1969-08-21', 'Female'),
(8, 'Omar', 'Ali', '1999-01-30', 'Male');

INSERT INTO departments VALUES
(1, 'Ophthalmology', 'Eye care'),
(2, 'Cardiology', 'Heart and circulation'),
(3, 'Emergency', 'Urgent care'),
(4, 'General Medicine', 'Medical assessment');

INSERT INTO appointments VALUES
(1, 1, 1, '2026-01-05', 'Attended', 12),
(2, 2, 2, '2026-01-08', 'Attended', 20),
(3, 3, 1, '2026-01-18', 'No-show', 15),
(4, 4, 3, '2026-02-02', 'Attended', 2),
(5, 5, 4, '2026-02-12', 'Cancelled', 9),
(6, 6, 2, '2026-02-18', 'No-show', 25),
(7, 7, 3, '2026-03-01', 'Attended', 1),
(8, 8, 1, '2026-03-09', 'Attended', 18),
(9, 1, 1, '2026-03-21', 'Attended', 10),
(10, 3, 4, '2026-04-04', 'Attended', 8),
(11, 5, 2, '2026-04-18', 'No-show', 22),
(12, 8, 3, '2026-05-02', 'Attended', 3);

INSERT INTO admissions VALUES
(1, 4, 3, '2026-02-02', '2026-02-04', 'Emergency'),
(2, 7, 3, '2026-03-01', '2026-03-06', 'Emergency'),
(3, 2, 2, '2026-03-14', '2026-03-18', 'Planned'),
(4, 7, 4, '2026-03-25', '2026-03-29', 'Emergency'),
(5, 1, 1, '2026-04-10', '2026-04-11', 'Planned'),
(6, 6, 2, '2026-05-05', '2026-05-12', 'Emergency'),
(7, 3, 4, '2026-05-20', '2026-05-23', 'Planned');

INSERT INTO diagnoses VALUES
(1, 1, 'R07', 'Chest pain assessment', 'Medium'),
(2, 2, 'H16', 'Keratitis observation', 'High'),
(3, 3, 'I10', 'Hypertension management', 'Medium'),
(4, 4, 'R53', 'Weakness and fatigue', 'Medium'),
(5, 5, 'H18', 'Corneal assessment', 'Low'),
(6, 6, 'I50', 'Heart failure monitoring', 'High'),
(7, 7, 'E86', 'Dehydration', 'Low');

INSERT INTO lab_results VALUES
(1, 1, 'CRP', 4.2, 'mg/L', 'Normal', '2026-04-10'),
(2, 2, 'Troponin', 18.5, 'ng/L', 'High', '2026-03-14'),
(3, 3, 'Creatinine', 91.0, 'umol/L', 'Normal', '2026-05-20'),
(4, 4, 'CRP', 22.0, 'mg/L', 'High', '2026-02-02'),
(5, 5, 'HbA1c', 42.0, 'mmol/mol', 'Normal', '2026-04-18'),
(6, 6, 'BNP', 480.0, 'pg/mL', 'High', '2026-05-05'),
(7, 7, 'CRP', 31.0, 'mg/L', 'High', '2026-03-01'),
(8, 7, 'Creatinine', 128.0, 'umol/L', 'High', '2026-03-25'),
(9, 8, 'CRP', 3.8, 'mg/L', 'Normal', '2026-05-02'),
(10, 2, 'BNP', 120.0, 'pg/mL', 'Normal', '2026-03-18');
